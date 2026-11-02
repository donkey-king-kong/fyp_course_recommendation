"""Counterfactual sensitivity checks for the deterministic recommendation engine.

Tests that the recommender responds in the expected direction to controlled input changes.
Run the FastAPI backend separately before using this script.

Exit code 0 = all checks passed.
Exit code 1 = one or more checks failed (findings are printed to stdout for review).

Do not tune scoring weights based solely on failures here. Record findings and fix
separately so the benchmark history stays readable.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Optional
from urllib.error import HTTPError, URLError

# Reuse request helpers from the benchmark runner to stay consistent.
from run_recommendation_benchmark_predictions import (
    build_recommendation_request,
    post_json,
)

OLD_CODE_PREFIXES = ("CE", "CPE", "CSC", "CZ")
DEFAULT_BENCHMARK_PATH = "data/recommendation_benchmark_cases.json"
DEFAULT_API_URL = "http://127.0.0.1:8000/recommendations"


def load_benchmark(path: Path) -> dict[str, Any]:
    with path.open() as f:
        return json.load(f)


def case_by_id(benchmark: dict[str, Any], case_id: str) -> dict[str, Any]:
    for case in benchmark.get("cases", []):
        if case["caseId"] == case_id:
            return case
    raise KeyError(f"Case '{case_id}' not found in benchmark file")


def get_recommendations(
    case: dict[str, Any],
    api_url: str,
    overrides: Optional[dict[str, Any]] = None,
    limit: int = 5,
) -> list[dict[str, Any]]:
    """Post a recommendation request for case, applying overrides to the payload."""
    payload = build_recommendation_request(case, limit_override=limit)
    if overrides:
        payload.update(overrides)
    response = post_json(api_url, payload, timeout=10.0)
    return response.get("recommendations", [])


def course_codes(recs: list[dict[str, Any]]) -> list[str]:
    return [r.get("courseCode", "") for r in recs]


def is_old_code(code: str) -> bool:
    return any(code.upper().startswith(p) for p in OLD_CODE_PREFIXES)


def slot_fits_code(course_code: str, slot_code: str) -> bool:
    if slot_code == "BDE":
        return True
    if slot_code.startswith("SC") and course_code.startswith("SC"):
        return course_code[2] == slot_code[2]
    return course_code == slot_code


def check_invariants(
    recs: list[dict[str, Any]],
    completed_codes: list[str],
    choice_slots: list[dict[str, Any]],
    label: str,
) -> list[str]:
    """Return a list of invariant violation messages (empty = all pass)."""
    failures: list[str] = []
    completed_upper = {c.upper() for c in completed_codes}
    for rec in recs:
        code = rec.get("courseCode", "")
        slot_id = rec.get("matchedChoiceSlotId") or rec.get("slotId") or rec.get("choiceSlotId")
        slot = next((s for s in choice_slots if s["slotId"] == slot_id), None)

        if is_old_code(code):
            failures.append(f"[{label}] Old code in recommendations: {code}")
        if code.upper() in completed_upper:
            failures.append(f"[{label}] Completed module in recommendations: {code}")
        if slot and not slot_fits_code(code, slot["courseCode"]):
            failures.append(f"[{label}] Slot mismatch: {code} assigned to {slot_id} (slot type {slot['courseCode']})")
    return failures


class CheckResult:
    def __init__(self, name: str) -> None:
        self.name = name
        self.passed = False
        self.messages: list[str] = []

    def fail(self, msg: str) -> None:
        self.messages.append(msg)
        self.passed = False

    def ok(self) -> None:
        if not self.messages:
            self.passed = True


def run_career_swap_check(
    benchmark: dict[str, Any],
    api_url: str,
    base_case_id: str,
    swap_career: str,
) -> CheckResult:
    """Changing career goal should produce a different recommendation set."""
    name = f"career-swap: {base_case_id} -> {swap_career}"
    result = CheckResult(name)

    base_case = case_by_id(benchmark, base_case_id)
    base_recs = get_recommendations(base_case, api_url)
    swap_recs = get_recommendations(base_case, api_url, overrides={"careerGoal": swap_career})

    base_codes = set(course_codes(base_recs))
    swap_codes = set(course_codes(swap_recs))

    if base_codes == swap_codes:
        result.fail(
            f"Recommendation sets are identical after career swap to '{swap_career}': {sorted(base_codes)}"
        )

    # At least one swapped recommendation should show the new career goal in its score evidence.
    # The career goal lives in scoreBreakdown.careerSkillEvidence.careerGoal.
    swap_career_found = any(
        (rec.get("scoreBreakdown") or {}).get("careerSkillEvidence", {}).get("careerGoal") == swap_career
        for rec in swap_recs
    )
    if not swap_career_found:
        evidences = [
            (rec.get("scoreBreakdown") or {}).get("careerSkillEvidence", {}).get("careerGoal")
            for rec in swap_recs
        ]
        result.fail(
            f"No recommendation after career swap to '{swap_career}' has careerSkillEvidence.careerGoal == '{swap_career}'. "
            f"Got careerGoals in evidence: {evidences}"
        )

    # Invariant checks on swapped result.
    inv_failures = check_invariants(
        swap_recs,
        base_case.get("completedCourseCodes", []),
        base_case.get("choiceSlots", []),
        label=name,
    )
    for msg in inv_failures:
        result.fail(msg)

    result.ok()
    return result


def run_preference_swap_check(
    benchmark: dict[str, Any],
    api_url: str,
    base_case_id: str,
    added_tag: str,
) -> CheckResult:
    """Adding a tag to preferredRecommendationTags should surface that tag in the top result."""
    name = f"preference-swap: {base_case_id} + tag '{added_tag}'"
    result = CheckResult(name)

    base_case = case_by_id(benchmark, base_case_id)
    original_tags = list(base_case.get("preferredRecommendationTags", []))
    new_tags = original_tags + ([added_tag] if added_tag not in original_tags else [])

    base_recs = get_recommendations(base_case, api_url)
    swap_recs = get_recommendations(
        base_case, api_url, overrides={"preferredRecommendationTags": new_tags}
    )

    # The tag should appear in at least one recommendation's matchedKeywords (direct or via alias).
    # Aliases from RECOMMENDATION_TAG_ALIASES in recommendation_service.py.
    tag_aliases = {
        "ai-ml": ("artificial-intelligence", "machine-learning"),
        "computer-network": ("networks",),
        "computer-security": ("cybersecurity",),
        "hardware-embedded": ("embedded-systems",),
    }
    tag_variants = {added_tag} | set(tag_aliases.get(added_tag, ()))
    # matchedKeywords entries with a tag look like "tag:<tagname>" or "skill:<area>:<tagname>".
    tag_appeared = any(
        any(
            any(variant in kw for kw in (rec.get("matchedKeywords") or []))
            for variant in tag_variants
        )
        for rec in swap_recs
    )
    if not tag_appeared:
        all_keywords = [rec.get("matchedKeywords", []) for rec in swap_recs]
        result.fail(
            f"Tag '{added_tag}' (or aliases {tag_variants}) does not appear in matchedKeywords of any "
            f"recommendation after being added to preferences. "
            f"Got recommendations: {[r.get('courseCode') for r in swap_recs]}. "
            f"matchedKeywords: {all_keywords}"
        )

    # Invariants on swapped result.
    inv_failures = check_invariants(
        swap_recs,
        base_case.get("completedCourseCodes", []),
        base_case.get("choiceSlots", []),
        label=name,
    )
    for msg in inv_failures:
        result.fail(msg)

    result.ok()
    return result


def run_completion_change_check(
    benchmark: dict[str, Any],
    api_url: str,
    base_case_id: str,
) -> CheckResult:
    """Marking the top recommended module as completed should remove it from recommendations."""
    name = f"completion-change: {base_case_id}"
    result = CheckResult(name)

    base_case = case_by_id(benchmark, base_case_id)
    base_recs = get_recommendations(base_case, api_url)

    if not base_recs:
        result.fail("Base case returned no recommendations — cannot test completion change.")
        return result

    top_code = base_recs[0].get("courseCode", "")
    if not top_code:
        result.fail("Top recommendation has no courseCode.")
        return result

    new_completed = list(base_case.get("completedCourseCodes", [])) + [top_code]
    new_curriculum = list(base_case.get("curriculumCourses", [])) + [top_code]
    swap_recs = get_recommendations(
        base_case,
        api_url,
        overrides={
            "completedCourseCodes": new_completed,
            "excludedCourseCodes": new_curriculum,
        },
    )

    swap_codes = [r.get("courseCode", "") for r in swap_recs]
    if top_code in swap_codes:
        result.fail(
            f"Module {top_code} still appears in recommendations after being marked completed. "
            f"Recommendations: {swap_codes}"
        )

    # Slot should still be filled (same number of recommendations, or slots are still assigned).
    expected_slots = len(base_case.get("choiceSlots", []))
    if len(swap_recs) < expected_slots:
        result.fail(
            f"After removing {top_code}, only {len(swap_recs)} of {expected_slots} slots filled. "
            f"Recommendations: {swap_codes}"
        )

    # Invariants on swapped result.
    inv_failures = check_invariants(
        swap_recs,
        new_completed,
        base_case.get("choiceSlots", []),
        label=name,
    )
    for msg in inv_failures:
        result.fail(msg)

    result.ok()
    return result


def run_all_checks(benchmark: dict[str, Any], api_url: str) -> list[CheckResult]:
    results: list[CheckResult] = []

    # Career swap: base case uses software-engineer; swap to data-scientist and cybersecurity-engineer.
    results.append(run_career_swap_check(benchmark, api_url, "software-engineer-csc-007", "data-scientist"))
    results.append(run_career_swap_check(benchmark, api_url, "software-engineer-csc-007", "cybersecurity-engineer"))

    # Preference swap: add computer-security to a case that doesn't have it.
    results.append(run_preference_swap_check(benchmark, api_url, "software-engineer-csc-009", "computer-security"))

    # Preference swap: add computer-network to a cloud platform case that doesn't have it listed.
    results.append(run_preference_swap_check(benchmark, api_url, "cloud-platform-engineer-csc-001", "computer-network"))

    # Completion change: remove the top recommendation by marking it done.
    results.append(run_completion_change_check(benchmark, api_url, "software-engineer-csc-001"))
    results.append(run_completion_change_check(benchmark, api_url, "data-scientist-csc-001"))
    results.append(run_completion_change_check(benchmark, api_url, "cybersecurity-engineer-csc-001"))

    return results


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Run counterfactual sensitivity checks against the live recommendation backend."
    )
    parser.add_argument(
        "--api-url",
        default=DEFAULT_API_URL,
        help=f"Recommendation endpoint URL (default: {DEFAULT_API_URL})",
    )
    parser.add_argument(
        "--benchmark",
        default=DEFAULT_BENCHMARK_PATH,
        help=f"Benchmark cases JSON path (default: {DEFAULT_BENCHMARK_PATH})",
    )
    parser.add_argument(
        "--output",
        default=None,
        help="Optional path to write results JSON for reporting.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    benchmark = load_benchmark(Path(args.benchmark))

    print(f"Running counterfactual sensitivity checks against {args.api_url}...")

    try:
        results = run_all_checks(benchmark, args.api_url)
    except (HTTPError, URLError) as e:
        print(f"ERROR: Could not reach backend at {args.api_url}. Start the FastAPI backend first.")
        print(f"Details: {e}")
        sys.exit(1)

    passed = [r for r in results if r.passed]
    failed = [r for r in results if not r.passed]

    print()
    for r in results:
        status = "PASS" if r.passed else "FAIL"
        print(f"  [{status}] {r.name}")
        for msg in r.messages:
            print(f"         -> {msg}")

    print()
    print(f"Results: {len(passed)} passed, {len(failed)} failed out of {len(results)} checks.")

    if args.output:
        output = {
            "totalChecks": len(results),
            "passed": len(passed),
            "failed": len(failed),
            "results": [
                {
                    "name": r.name,
                    "passed": r.passed,
                    "messages": r.messages,
                }
                for r in results
            ],
        }
        Path(args.output).parent.mkdir(parents=True, exist_ok=True)
        with Path(args.output).open("w") as f:
            json.dump(output, f, indent=2)
            f.write("\n")
        print(f"Results written to {args.output}")

    if failed:
        print()
        print("Some checks FAILED. Record these as findings; do not tune scoring weights here.")
        sys.exit(1)


if __name__ == "__main__":
    main()
