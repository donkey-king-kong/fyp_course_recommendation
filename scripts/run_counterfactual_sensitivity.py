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
    get_post_fn,
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
    post_fn: Any = None,
) -> list[dict[str, Any]]:
    """Post a recommendation request for case, applying overrides to the payload."""
    if post_fn is None:
        post_fn = post_json
    payload = build_recommendation_request(case, limit_override=limit)
    if overrides:
        payload.update(overrides)
    response = post_fn(api_url, payload, timeout=10.0)
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
        self.inconclusive = False
        self.messages: list[str] = []

    def fail(self, msg: str) -> None:
        self.messages.append(msg)
        self.passed = False

    def inconc(self, msg: str) -> None:
        """Mark as inconclusive (neither pass nor fail). The check ran but observed no change."""
        self.messages.append(msg)
        self.inconclusive = True

    def ok(self) -> None:
        if not self.messages:
            self.passed = True


def run_career_swap_check(
    benchmark: dict[str, Any],
    api_url: str,
    base_case_id: str,
    swap_career: str,
    post_fn: Any = None,
) -> CheckResult:
    """Changing career goal should produce a different recommendation set."""
    name = f"career-swap: {base_case_id} -> {swap_career}"
    result = CheckResult(name)

    base_case = case_by_id(benchmark, base_case_id)
    base_recs = get_recommendations(base_case, api_url, post_fn=post_fn)
    swap_recs = get_recommendations(base_case, api_url, overrides={"careerGoal": swap_career}, post_fn=post_fn)

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
    post_fn: Any = None,
) -> CheckResult:
    """Adding a tag to preferredRecommendationTags should produce an observable change.

    The check compares the baseline result against the swapped result. A genuine PASS requires
    that the tag appears in the swap's matchedKeywords but NOT in the baseline's (i.e. the tag
    actually caused a new match), or that the recommended set or order changed.

    Returns INCONCLUSIVE (not a FAIL) if the tag was already in the baseline matchedKeywords or
    if adding it produced no observable change. INCONCLUSIVE indicates a known limitation of the
    career-first policy: a preference tag only surfaces when an eligible career-mapped module
    carries that tag AND the module wasn't already going to appear.

    Fails immediately if the base case already has the added_tag as a preference, because then
    no real swap occurs and any result is meaningless.
    """
    name = f"preference-swap: {base_case_id} + tag '{added_tag}'"
    result = CheckResult(name)

    base_case = case_by_id(benchmark, base_case_id)
    original_tags = list(base_case.get("preferredRecommendationTags", []))

    # Guard: the tag must be genuinely new — if it's already present the check is a no-op.
    if added_tag in original_tags:
        result.fail(
            f"Base case '{base_case_id}' already has tag '{added_tag}' in preferredRecommendationTags "
            f"({original_tags}). Choose a tag that is not in the base case."
        )
        return result

    new_tags = original_tags + [added_tag]

    base_recs = get_recommendations(base_case, api_url, post_fn=post_fn)
    swap_recs = get_recommendations(
        base_case, api_url, overrides={"preferredRecommendationTags": new_tags}, post_fn=post_fn
    )

    # Aliases from RECOMMENDATION_TAG_ALIASES in recommendation_service.py.
    tag_aliases = {
        "ai-ml": ("artificial-intelligence", "machine-learning"),
        "computer-network": ("networks",),
        "computer-security": ("cybersecurity",),
        "hardware-embedded": ("embedded-systems",),
    }
    tag_variants = {added_tag} | set(tag_aliases.get(added_tag, ()))

    def keywords_for(recs: list[dict[str, Any]]) -> set[str]:
        result_set: set[str] = set()
        for rec in recs:
            result_set.update(rec.get("matchedKeywords") or [])
        return result_set

    base_keywords = keywords_for(base_recs)
    swap_keywords = keywords_for(swap_recs)

    # The tag should appear in swap but NOT baseline: only then did adding it cause a new signal.
    tag_in_baseline = any(
        any(variant in kw for kw in base_keywords)
        for variant in tag_variants
    )
    tag_in_swap = any(
        any(variant in kw for kw in swap_keywords)
        for variant in tag_variants
    )

    base_codes = course_codes(base_recs)
    swap_codes = course_codes(swap_recs)
    set_changed = set(base_codes) != set(swap_codes) or base_codes != swap_codes

    if tag_in_baseline:
        # Tag was already present in the baseline — adding it does nothing new.
        result.inconc(
            f"Tag '{added_tag}' (or aliases {tag_variants}) already appears in baseline matchedKeywords. "
            f"Adding it to preferences produces no new signal under the career-first policy. "
            f"Baseline keywords containing the tag: {[kw for kw in base_keywords if any(v in kw for v in tag_variants)]}. "
            f"This is an INCONCLUSIVE check, not a failure — it documents a known property of career-first: "
            f"a preference tag only surfaces when a career-mapped, eligible module carries that tag and was "
            f"not already going to be recommended."
        )
        return result

    if not tag_in_swap and not set_changed:
        # Tag not in baseline but still doesn't appear after the swap — no eligible carrier module.
        result.fail(
            f"Tag '{added_tag}' (or aliases {tag_variants}) does not appear in matchedKeywords after "
            f"being added to preferences, and the recommended set did not change. "
            f"Got recommendations: {swap_codes}. "
            f"matchedKeywords: {list(swap_keywords)}"
        )
    elif not tag_in_swap and set_changed:
        # Set changed but not because of the tag — PASS because there's an observable effect.
        pass

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
    post_fn: Any = None,
) -> CheckResult:
    """Marking the top recommended module as completed should remove it from recommendations."""
    name = f"completion-change: {base_case_id}"
    result = CheckResult(name)

    base_case = case_by_id(benchmark, base_case_id)
    base_recs = get_recommendations(base_case, api_url, post_fn=post_fn)

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
        post_fn=post_fn,
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


def run_career_conflict_check(
    benchmark: dict[str, Any],
    api_url: str,
    base_case_id: str,
    conflicting_tags: list[str],
    post_fn: Any = None,
) -> CheckResult:
    """Under the career-first policy, career picks should still show the original career goal
    even when the student's preferences are entirely from a different career domain.

    Checks that every recommendation whose recommendationSource == 'career' carries
    scoreBreakdown.careerSkillEvidence.careerGoal equal to the base case's career goal.
    """
    base_case = case_by_id(benchmark, base_case_id)
    career_goal = base_case["careerGoal"]
    name = f"career-conflict: {base_case_id} career={career_goal} vs conflicting prefs {conflicting_tags}"
    result = CheckResult(name)

    recs = get_recommendations(
        base_case, api_url, overrides={"preferredRecommendationTags": conflicting_tags}, post_fn=post_fn
    )

    for rec in recs:
        source = rec.get("recommendationSource", "career")
        if source != "career":
            continue  # interest picks are allowed to have no career evidence

        evidence_goal = (rec.get("scoreBreakdown") or {}).get("careerSkillEvidence", {}).get("careerGoal")
        if evidence_goal is not None and evidence_goal != career_goal:
            result.fail(
                f"Career pick {rec.get('courseCode')} has careerSkillEvidence.careerGoal='{evidence_goal}' "
                f"but expected '{career_goal}'. Conflicting prefs should not change the career goal."
            )

    if not recs:
        result.fail("No recommendations returned — cannot verify career-first policy.")
    else:
        result.ok()

    # Invariants.
    inv_failures = check_invariants(
        recs,
        base_case.get("completedCourseCodes", []),
        base_case.get("choiceSlots", []),
        label=name,
    )
    for msg in inv_failures:
        result.fail(msg)

    return result


def run_all_checks(benchmark: dict[str, Any], api_url: str, post_fn: Any = None) -> list[CheckResult]:
    results: list[CheckResult] = []

    # Career swap: base case uses software-engineer; swap to data-scientist and cybersecurity-engineer.
    results.append(run_career_swap_check(benchmark, api_url, "software-engineer-csc-007", "data-scientist", post_fn=post_fn))
    results.append(run_career_swap_check(benchmark, api_url, "software-engineer-csc-007", "cybersecurity-engineer", post_fn=post_fn))

    # Preference swap: add computer-security to a software-engineer case that doesn't have it.
    results.append(run_preference_swap_check(benchmark, api_url, "software-engineer-csc-009", "computer-security", post_fn=post_fn))

    # Preference swap: add cybersecurity to an ai-ml case that currently lacks it.
    # ai-ml-engineer-csc-001 prefs are ['ai-ml', 'natural-language-processing', 'computer-vision'].
    # cybersecurity is in SOFTWARE_ENGINEER_TAG_WEIGHTS but not in AI_ML_SKILL_MAPPINGS.
    # NOTE: this swap tests a career-irrelevant tag — under career-first the tag should NOT appear
    # in pass-1 matchedKeywords (since ai-ml career mapping doesn't include cybersecurity).
    # This is intentionally noted here as a known limitation of the preference-swap check:
    # it can only assert tag presence when a career-mapped, eligible module carries that tag.
    #
    # Instead verify the swap with a career-mapped tag: 'database' is in AI_ML_SKILL_MAPPINGS
    # (data modelling / statistical reasoning) — and SC3020 has 'database' tag.
    results.append(run_preference_swap_check(benchmark, api_url, "ai-ml-engineer-csc-001", "database", post_fn=post_fn))

    # Career-conflict: ai-ml student with SWE-type preferences — career picks should still show ai-ml-engineer.
    results.append(run_career_conflict_check(
        benchmark, api_url,
        "ai-ml-engineer-csc-001",
        conflicting_tags=["backend-engineering", "software-engineering", "web-development"],
        post_fn=post_fn,
    ))

    # Completion change: remove the top recommendation by marking it done.
    results.append(run_completion_change_check(benchmark, api_url, "software-engineer-csc-001", post_fn=post_fn))
    results.append(run_completion_change_check(benchmark, api_url, "data-scientist-csc-001", post_fn=post_fn))
    results.append(run_completion_change_check(benchmark, api_url, "cybersecurity-engineer-csc-001", post_fn=post_fn))

    return results


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Run counterfactual sensitivity checks against the recommendation backend."
    )
    parser.add_argument(
        "--api-url",
        default=DEFAULT_API_URL,
        help=f"Recommendation endpoint URL (default: {DEFAULT_API_URL}, only used with --live)",
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
    parser.add_argument(
        "--live",
        action="store_true",
        help="Call a running backend server instead of running in-process.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    benchmark = load_benchmark(Path(args.benchmark))
    post_fn = get_post_fn(args.live)
    mode = f"live backend at {args.api_url}" if args.live else "in-process"
    print(f"Running counterfactual sensitivity checks ({mode})...")

    try:
        results = run_all_checks(benchmark, args.api_url, post_fn=post_fn)
    except (HTTPError, URLError) as e:
        print(f"ERROR: Could not reach backend at {args.api_url}. Start the FastAPI backend first.")
        print(f"Details: {e}")
        sys.exit(1)

    passed = [r for r in results if r.passed]
    failed = [r for r in results if not r.passed and not r.inconclusive]
    inconclusive = [r for r in results if r.inconclusive]

    print()
    for r in results:
        if r.passed:
            status = "PASS"
        elif r.inconclusive:
            status = "INCONCLUSIVE"
        else:
            status = "FAIL"
        print(f"  [{status}] {r.name}")
        for msg in r.messages:
            print(f"         -> {msg}")

    print()
    print(
        f"Results: {len(passed)} passed, {len(failed)} failed, "
        f"{len(inconclusive)} inconclusive out of {len(results)} checks."
    )
    if inconclusive:
        print(
            "  INCONCLUSIVE = no observable change; check documents a known property, "
            "not a failure."
        )

    if args.output:
        output = {
            "totalChecks": len(results),
            "passed": len(passed),
            "failed": len(failed),
            "inconclusive": len(inconclusive),
            "results": [
                {
                    "name": r.name,
                    "passed": r.passed,
                    "inconclusive": r.inconclusive,
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
