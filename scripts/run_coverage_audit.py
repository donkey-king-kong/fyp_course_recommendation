"""Coverage audit for the deterministic recommendation engine.

Tests whether every career goal x slot-type combination fills all expected slots.
Synthetic profiles are built from existing benchmark case data to keep the audit
consistent with the real evaluation inputs.

Run the FastAPI backend separately before using this script.

Exit code 0 = no invariant violations (empty slots are reported, not failed).
Exit code 1 = one or more invariant violations found.

Faculty note: CSC faculty only. Non-CSC faculties (EEE, CE, etc.) are a known
limitation and are not covered here.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any
from urllib.error import HTTPError, URLError

# Reuse helpers from existing scripts to stay consistent.
from run_recommendation_benchmark_predictions import (
    REPO_ROOT,
    add_provenance_args,
    build_recommendation_request,
    capture_provenance,
    post_json,
    write_json,
)
from run_counterfactual_sensitivity import check_invariants, slot_fits_code
from evaluate_recommendation_benchmark import validate_response

CAREERS = [
    "software-engineer",
    "ai-ml-engineer",
    "data-engineer",
    "cloud-platform-engineer",
    "cybersecurity-engineer",
    "data-scientist",
]

# First aligned tag for each career (from career_skill_mappings.py — used as the
# "aligned" preference mode so we can test whether aligned preferences raise fill rate).
CAREER_ALIGNED_TAGS: dict[str, list[str]] = {
    "software-engineer": ["software-engineering", "backend-engineering"],
    "ai-ml-engineer": ["artificial-intelligence", "machine-learning"],
    "data-engineer": ["data-engineering", "database"],
    "cloud-platform-engineer": ["cloud-computing", "distributed-systems"],
    "cybersecurity-engineer": ["computer-security", "cybersecurity"],
    "data-scientist": ["data-science", "machine-learning"],
}

# Conflicting tags (from a different career domain) for the "conflicting" preference mode.
CAREER_CONFLICTING_TAGS: dict[str, list[str]] = {
    "software-engineer": ["data-science", "machine-learning"],
    "ai-ml-engineer": ["computer-security", "web-development"],
    "data-engineer": ["computer-security", "operating-systems"],
    "cloud-platform-engineer": ["data-science", "computer-security"],
    "cybersecurity-engineer": ["machine-learning", "web-development"],
    "data-scientist": ["cloud-computing", "web-development"],
}

# Slot configurations to audit: each entry is a list of slot descriptors (courseCode field).
SLOT_CONFIGS: list[tuple[str, list[str]]] = [
    ("SC3xxx-only", ["SC3xxx"]),
    ("SC4xxx-only", ["SC4xxx"]),
    ("SC3-and-SC4", ["SC3xxx", "SC4xxx"]),
    ("SC4-BDE-BDE", ["SC4xxx", "BDE", "BDE"]),
    ("BDE-only", ["BDE", "BDE"]),
]

# Progress stages: (label, completed_courses, curriculum_courses).
# Borrowed from benchmark cases to keep inputs realistic.
# Y2-end: data-scientist-csc-001 (15 completed, prereqs for SC3/4 met).
# Y4-end: software-engineer-csc-001 (35 completed, most SC3/4 prereqs cleared).
PROGRESS_STAGES: list[tuple[str, list[str], list[str]]] = [
    (
        "Y2-end",
        ["SC1003", "SC1004", "SC1005", "SC1006", "SC1007", "SC1015",
         "SC2000", "SC2001", "SC2002", "SC2005", "SC2006", "SC2008",
         "SC2207", "MH1810", "MH1812"],
        ["SC1003", "SC1004", "SC1005", "SC1006", "SC1007", "SC1015",
         "SC2000", "SC2001", "SC2002", "SC2005", "SC2006", "SC2008",
         "SC2207", "MH1810", "MH1812"],
    ),
    (
        "Y4-end",
        ["SC1003", "SC1013", "MH1810", "MH1812", "CC0003", "CC0005",
         "AB1201", "AB1501", "AD1102", "CC0001", "CC0002", "EG1001",
         "SC1004", "SC1005", "SC1007", "SC1015", "CC0007", "SC1006",
         "SC2000", "SC2001", "SC2002", "SC2006", "AB1601", "CC0006",
         "ML0004", "SC2005", "SC2008", "SC2207", "SC3000", "SC3920",
         "AD2102", "BE1402", "SC3010", "SC4000", "SC4002"],
        ["SC1003", "SC1013", "MH1810", "MH1812", "CC0003", "CC0005",
         "SC1005", "SC1007", "SC1015", "EG1001", "CC0001", "CC0002",
         "SC1004", "SC1006", "SC2001", "SC2002", "CC0007", "SC2000",
         "SC2005", "SC2006", "SC2207", "CC0006", "ML0004", "SC2008",
         "SC2079", "SC3000", "SC3010", "HW0288", "SC4079", "SC3920"],
    ),
]

PREFERENCE_MODES: list[tuple[str, str]] = [
    ("none", "no preferences"),
    ("aligned", "aligned with career"),
    ("conflicting", "conflicting with career"),
]

DEFAULT_API_URL = "http://127.0.0.1:8000/recommendations"
DEFAULT_LIMIT = 5

def build_slots(slot_types: list[str]) -> list[dict[str, Any]]:
    """Build choiceSlots list from a list of slot type codes."""
    return [
        {"slotId": f"audit-slot-{i + 1}", "courseCode": slot_type}
        for i, slot_type in enumerate(slot_types)
    ]

def build_request(
    career: str,
    slot_types: list[str],
    completed: list[str],
    curriculum: list[str],
    preferred_tags: list[str],
    limit: int,
) -> dict[str, Any]:
    """Build a recommendation request payload for an audit cell.

    Delegates to build_recommendation_request() via a synthetic case dict so
    the audit is always in sync with the benchmark runner's request shape. This
    prevents the audit from accidentally omitting fields such as studentFaculty
    or choiceSlotCodes that affect scoring (e.g. the CSC faculty boost).
    """
    slots = build_slots(slot_types)
    # curriculumCourses as dicts so normalise_curriculum_courses passes them through.
    curriculum_dicts = [{"courseCode": c} for c in curriculum]
    synthetic_case: dict[str, Any] = {
        "careerGoal": career,
        "preferredRecommendationTags": preferred_tags,
        "studentFaculty": "CSC",
        "completedCourseCodes": completed,
        "choiceSlots": slots,
        "curriculumCourses": curriculum_dicts,
    }
    return build_recommendation_request(synthetic_case, limit_override=limit)

def run_audit_cell(
    career: str,
    slot_label: str,
    slot_types: list[str],
    progress_label: str,
    completed: list[str],
    curriculum: list[str],
    pref_mode: str,
    preferred_tags: list[str],
    api_url: str,
    limit: int,
) -> dict[str, Any]:
    """Run one audit cell and return a result dict."""
    payload = build_request(career, slot_types, completed, curriculum, preferred_tags, limit)
    response = post_json(api_url, payload, timeout=15.0)
    recs = response.get("recommendations", [])

    expected_slots = len(slot_types)
    assigned_slots = len(recs)
    slot_fill_rate = min(assigned_slots, expected_slots) / expected_slots if expected_slots > 0 else 0.0

    interest_picks = sum(1 for r in recs if r.get("recommendationSource") == "interest")
    low_confidence = sum(1 for r in recs if r.get("recommendationConfidence") == "low")

    # Weak fit: slot filled only by faculty/non-career signal.  Flags picks where
    # the career skill score is low and no direct career tag matched, so a reviewer
    # can spot "filled but poorly matched" cases without treating them as empty slots.
    def is_weak_fit(rec: dict[str, Any]) -> bool:
        bd = rec.get("scoreBreakdown") or {}
        career_skill = bd.get("careerSkillScore", 0) or 0
        career_tag = bd.get("careerTagScore", 0) or 0
        return career_skill < 5 and career_tag == 0

    weak_fit_picks = sum(1 for r in recs if is_weak_fit(r))
    weak_fit_codes = [r.get("courseCode", "") for r in recs if is_weak_fit(r)]

    slots = build_slots(slot_types)
    inv_failures = check_invariants(recs, completed, slots, label=f"{career}/{slot_label}/{progress_label}/{pref_mode}")

    empty_slots = []
    filled_slot_ids = {r.get("matchedChoiceSlotId") or r.get("slotId") or r.get("choiceSlotId") for r in recs}
    for s in slots:
        if s["slotId"] not in filled_slot_ids:
            empty_slots.append(s["slotId"])

    return {
        "request": payload,
        "response": response,
        "supplementaryValidation": validate_response(payload, response),
        "career": career,
        "slotConfig": slot_label,
        "progressStage": progress_label,
        "preferenceMode": pref_mode,
        "expectedSlots": expected_slots,
        "assignedSlots": assigned_slots,
        "slotFillRate": round(slot_fill_rate, 4),
        "emptySlots": empty_slots,
        "interestPicks": interest_picks,
        "lowConfidencePicks": low_confidence,
        "weakFitPicks": weak_fit_picks,
        "weakFitCodes": weak_fit_codes,
        "invariantViolations": inv_failures,
        "recommendedCodes": [r.get("courseCode", "") for r in recs],
    }

# These deliberately constrained catalog fixtures exercise contracts, not recommendation quality.
def build_positioned_scenarios() -> list[dict[str, Any]]:
    with (REPO_ROOT / "data/modules.json").open() as file:
        modules = {module["code"]: module for module in json.load(file)["modules"]}
    with (REPO_ROOT / "data/course_catalog.json").open() as file:
        catalog = {module["code"]: module for module in json.load(file)}
    with (REPO_ROOT / "data/ntu_prerequisite_unlock_graph.json").open() as file:
        prerequisite_graph = json.load(file)
    required_codes = {"SC4052", "SC1004", "MH2802", "SC2002", "SC4012", "CC0001", "SC4051", "SC3020", "EE4791", "SC3060"}
    missing = required_codes - modules.keys()
    if missing:
        raise ValueError(f"Positioned scenario fixtures missing from local catalog: {sorted(missing)}")
    if "MH2802" not in prerequisite_graph.get("SC4052", {}).get("prerequisites", []):
        raise ValueError("SC4052 planning fixture no longer has graph prerequisite MH2802.")
    if "computer-graphics" not in modules["SC3060"].get("recommendationTags", []):
        raise ValueError("SC3060 interest fixture no longer carries computer-graphics.")
    all_codes = set(modules) | set(catalog)

    def curriculum(code: str, year: int, semester: int) -> dict[str, Any]:
        return {
            "nodeId": f"fixed-{code.lower()}", "courseCode": code,
            "title": modules[code]["title"], "year": year, "semester": semester,
        }

    def slot(code: str, year: int, semester: int, name: str = "target") -> dict[str, Any]:
        return {"slotId": name, "courseCode": code, "year": year, "semester": semester}

    def scenario(
        name: str, allowed: list[str], slots: list[dict[str, Any]],
        fixed: list[dict[str, Any]], completed: list[str], career: str,
        preferences: list[str], expectation: dict[str, Any],
    ) -> dict[str, Any]:
        case = {
            "careerGoal": career, "studentFaculty": "CSC", "choiceSlots": slots,
            "curriculumCourses": [*fixed, *[
                {
                    "nodeId": item["slotId"], "courseCode": item["courseCode"],
                    "title": "Choice slot", "isChoiceSlot": True,
                    "year": item["year"], "semester": item["semester"],
                }
                for item in slots
            ]],
            "completedCourseCodes": completed, "preferredRecommendationTags": preferences,
            "excludedCourseCodes": sorted(all_codes - set(allowed)),
        }
        return {
            "name": name, "request": build_recommendation_request(case, None),
            "expectation": expectation,
            "localCatalogRequirements": {code: catalog.get(code, {}).get("prerequisites") for code in allowed},
        }

    return [
        scenario(
            "completed-cloud-alternative", ["SC4052"], [slot("SC4xxx", 4, 1)], [],
            ["SC1004"], "software-engineer", ["cloud-computing"],
            {"courseCode": "SC4052", "readinessStatus": "ready", "plannedPrerequisiteCount": 0},
        ),
        scenario(
            "earlier-fixed-prerequisite", ["SC4052"], [slot("SC4xxx", 4, 1)],
            [curriculum("MH2802", 2, 1)], [], "software-engineer", ["cloud-computing"],
            {"courseCode": "SC4052", "existingPrerequisite": "MH2802"},
        ),
        scenario(
            "earlier-open-prerequisite-plan", ["SC4052", "SC1004", "MH2802"],
            [slot("BDE", 2, 2, "earlier"), slot("SC4xxx", 4, 1)], [], ["SC1003", "MH1810"],
            "software-engineer", ["cloud-computing"],
            {"courseCode": "SC4052", "plannedPrerequisiteAlternatives": ["SC1004", "MH2802"]},
        ),
        scenario(
            "reviewed-supplementary-prerequisite-plan", ["SC4012", "SC2002"],
            [slot("SC4xxx", 4, 1)], [curriculum("CC0001", 3, 1)],
            ["SC1003", "SC2005"], "software-engineer", ["software-security"],
            {"courseCode": "SC4012", "plannedPrerequisite": "SC2002", "generatedNode": "SC2002"},
        ),
        scenario(
            "no-earlier-placement", ["SC4052", "MH2802"], [slot("SC4xxx", 4, 1)], [], [],
            "software-engineer", ["cloud-computing"],
            {"absentCourseCode": "SC4052", "requiredControl": "completed-cloud-alternative"},
        ),
        scenario(
            "bde-year-level", ["SC2002", "SC4051"], [slot("BDE", 2, 1)], [],
            ["SC1003", "SC1007", "SC1005", "SC2005", "SC2006", "SC2008"], "software-engineer",
            ["software-engineering"], {"requiredLevel": 2},
        ),
        scenario(
            "title-equivalence-control", ["SC3020"], [slot("SC3xxx", 3, 2)], [],
            ["SC2207"], "software-engineer", ["database"], {"courseCode": "SC3020"},
        ),
        scenario(
            "fixed-title-equivalence", ["SC3020"], [slot("SC3xxx", 3, 2)],
            [curriculum("EE4791", 3, 1)], ["SC2207"], "software-engineer",
            ["database"], {"absentCourseCode": "SC3020", "requiredControl": "title-equivalence-control"},
        ),
        scenario(
            "interest-fallback-graphics", ["SC3060"], [slot("SC3xxx", 3, 1)], [], [],
            "cybersecurity-engineer", ["computer-graphics"],
            {"courseCode": "SC3060", "recommendationSource": "interest"},
        ),
    ]

def check_scenario_observation(scenario: dict[str, Any], response: dict[str, Any]) -> dict[str, Any]:
    recs, expectation = response.get("recommendations", []), scenario["expectation"]
    failures = []
    absent = expectation.get("absentCourseCode")
    if absent and any(rec.get("courseCode") == absent for rec in recs):
        failures.append(f"{absent} should be excluded in this scenario.")
    if "requiredLevel" in expectation:
        if not recs:
            return {"status": "inconclusive", "messages": ["No recommendation returned; year-level behavior was not exercised."]}
        if any(rec.get("level") != expectation["requiredLevel"] for rec in recs):
            failures.append("Returned BDE recommendation does not match the requested year-level.")
    if expectation.get("courseCode"):
        matches = [rec for rec in recs if rec.get("courseCode") == expectation["courseCode"]]
        if not matches:
            return {"status": "inconclusive", "messages": [f"Expected catalog fixture {expectation['courseCode']} was not returned; serving catalog/eligibility is unverified."]}
        for rec in matches:
            if expectation.get("generatedNode"):
                node_ids = {
                    node["id"] for node in rec.get("plannedRoadmapNodes", [])
                    if node.get("courseCode") == expectation["generatedNode"] and node.get("id")
                }
                if not node_ids:
                    failures.append(f"Expected supplementary node {expectation['generatedNode']} was not generated.")
                if not any(edge.get("source") in node_ids and edge.get("target") == rec.get("matchedChoiceSlotId") for edge in rec.get("plannedRoadmapEdges", [])):
                    failures.append("Expected generated prerequisite edge to the assigned slot was not returned.")
            if expectation.get("plannedPrerequisiteAlternatives") and not set(expectation["plannedPrerequisiteAlternatives"]).intersection(rec.get("plannedPrerequisiteCourseCodes", [])):
                failures.append("No supported SC1004/MH2802 prerequisite alternative was planned.")
            if expectation.get("readinessStatus") and rec.get("readinessStatus") != expectation["readinessStatus"]:
                failures.append(f"Expected readinessStatus {expectation['readinessStatus']} was not returned.")
            if "plannedPrerequisiteCount" in expectation and len(rec.get("plannedPrerequisiteCourseCodes", [])) != expectation["plannedPrerequisiteCount"]:
                failures.append("The completed prerequisite alternative should not need extra planning.")
            if expectation.get("recommendationSource") and rec.get("recommendationSource") != expectation["recommendationSource"]:
                failures.append("The intended pass-2 interest path did not fire.")
            for key, field in (("existingPrerequisite", "existingPrerequisiteCourseCodes"), ("plannedPrerequisite", "plannedPrerequisiteCourseCodes")):
                if expectation.get(key) and expectation[key] not in rec.get(field, []):
                    failures.append(f"Expected {key} {expectation[key]} is absent from response metadata.")
    return {"status": "fail" if failures else "pass", "messages": failures}

def run_positioned_scenarios(api_url: str) -> list[dict[str, Any]]:
    results = []
    for scenario in build_positioned_scenarios():
        response = post_json(api_url, scenario["request"], timeout=15.0)
        results.append({
            **scenario, "response": response,
            "supplementaryValidation": validate_response(scenario["request"], response),
            "observation": check_scenario_observation(scenario, response),
        })
    by_name = {result["name"]: result for result in results}
    for result in results:
        control = result["expectation"].get("requiredControl")
        if control and result["observation"]["status"] == "pass" and by_name[control]["observation"]["status"] != "pass":
            result["observation"] = {"status": "inconclusive", "messages": [f"Control {control} did not return the candidate; its exclusion cannot be attributed to this scenario."]}
    return results

def print_summary_table(results: list[dict[str, Any]]) -> None:
    """Print a compact table of fill rates grouped by career x slot config."""
    print()
    print("Coverage audit summary (slotFillRate by career × slot config × progress × pref mode)")
    print()

    # Build a lookup
    def key(r: dict[str, Any]) -> tuple[str, str, str, str]:
        return (r["career"], r["slotConfig"], r["progressStage"], r["preferenceMode"])

    lookup = {key(r): r for r in results}
    careers = list(dict.fromkeys(r["career"] for r in results))
    slot_configs = list(dict.fromkeys(r["slotConfig"] for r in results))
    progress_stages = list(dict.fromkeys(r["progressStage"] for r in results))
    pref_modes_list = list(dict.fromkeys(r["preferenceMode"] for r in results))

    for progress in progress_stages:
        print(f"  Progress stage: {progress}")
        header = f"  {'Career':<30}" + "".join(f" {sc:<16}" for sc in slot_configs)
        print(header)
        print("  " + "-" * (len(header) - 2))

        for career in careers:
            for pref in pref_modes_list:
                row_label = f"{career} [{pref}]"
                row = f"  {row_label:<30}"
                any_miss = False
                for sc in slot_configs:
                    cell = lookup.get((career, sc, progress, pref))
                    if cell:
                        fill = cell["slotFillRate"]
                        interest = cell["interestPicks"]
                        low = cell["lowConfidencePicks"]
                        viol = len(cell["invariantViolations"])
                        weak = cell.get("weakFitPicks", 0)
                        flag = "✓" if fill >= 1.0 and viol == 0 else "✗"
                        marker = ""
                        if interest > 0:
                            marker += f"i{interest}"
                        if low > 0:
                            marker += f"l{low}"
                        if weak > 0:
                            marker += f"w{weak}"
                        if viol > 0:
                            marker += f"!{viol}"
                        cell_str = f"{flag}{fill:.2f}{(' '+marker) if marker else ''}"
                        row += f" {cell_str:<16}"
                        if fill < 1.0:
                            any_miss = True
                    else:
                        row += f" {'?':<16}"
                print(row)
        print()

    # Invariant violations summary
    all_violations = [v for r in results for v in r["invariantViolations"]]
    if all_violations:
        print(f"  !! {len(all_violations)} INVARIANT VIOLATION(S):")
        for v in all_violations:
            print(f"     {v}")
    else:
        print("  Invariant violations: 0")
    print()

    # Empty slot findings
    empty_findings = [r for r in results if r["emptySlots"]]
    if empty_findings:
        print(f"  Empty slot findings ({len(empty_findings)} cells with unfilled slots):")
        for r in empty_findings:
            print(
                f"     {r['career']}/{r['slotConfig']}/{r['progressStage']}/{r['preferenceMode']}: "
                f"empty={r['emptySlots']} assigned={r['assignedSlots']}/{r['expectedSlots']}"
            )
    else:
        print("  No empty slot findings.")
    print()

    # Interest picks summary
    interest_findings = [r for r in results if r["interestPicks"] > 0]
    if interest_findings:
        print(f"  Pass-2 interest picks fired in {len(interest_findings)} cell(s):")
        for r in interest_findings:
            print(
                f"     {r['career']}/{r['slotConfig']}/{r['progressStage']}/{r['preferenceMode']}: "
                f"interest={r['interestPicks']}"
            )
    else:
        print("  Pass-2 interest picks: none fired (all slots filled by career picks).")
    print()

    # Weak-fit picks summary (filled but low career signal — slot not empty, but poor quality match).
    weak_findings = [r for r in results if r.get("weakFitPicks", 0) > 0]
    if weak_findings:
        print(f"  Weak-fit picks (careerSkillScore < 5 and careerTagScore == 0) in {len(weak_findings)} cell(s):")
        # Deduplicate by code across cells for a concise view.
        seen_codes: set[str] = set()
        for r in weak_findings:
            codes = r.get("weakFitCodes", [])
            new_codes = [c for c in codes if c not in seen_codes]
            seen_codes.update(new_codes)
            if new_codes:
                print(
                    f"     {r['career']}/{r['slotConfig']}/{r['progressStage']}/{r['preferenceMode']}: "
                    f"{new_codes}"
                )
    else:
        print("  Weak-fit picks: none (all filled slots have adequate career signal).")
    print()

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Coverage audit: measure slot-fill rate across career x slot-type combinations."
    )
    parser.add_argument(
        "--api-url",
        default=DEFAULT_API_URL,
        help=f"Recommendation endpoint URL (default: {DEFAULT_API_URL})",
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=DEFAULT_LIMIT,
        help=f"Max recommendations per request (default: {DEFAULT_LIMIT})",
    )
    parser.add_argument(
        "--output",
        default=None,
        help="Optional path to write results JSON.",
    )
    parser.add_argument("--mode", choices=["historical-grid", "positioned-scenarios"], default="historical-grid", help="Run separate positioned/titled contract scenarios without mixing historical grid metrics.")
    add_provenance_args(parser)
    return parser.parse_args()

def main() -> None:
    args = parse_args()
    if args.mode == "positioned-scenarios":
        try:
            scenarios = run_positioned_scenarios(args.api_url)
        except (HTTPError, URLError, ValueError) as error:
            raise SystemExit(f"Positioned scenarios could not run: {error}") from error
        for scenario in scenarios:
            print(f"{scenario['name']}: {scenario['observation']['status']}, contract violations={len(scenario['supplementaryValidation']['violations'])}")
        output = {
            "mode": args.mode, "apiUrl": args.api_url, "provenance": capture_provenance(args.serving_revision, args.database_fingerprint),
            "scope": "Catalog-constrained positioned/titled scenarios; separate from historical coverage and relevance metrics. Raw standing and non-course requirements are not independently validated by the script.",
            "scenarios": scenarios,
        }
        if args.output:
            write_json(Path(args.output), output)
        if any(scenario["supplementaryValidation"]["violations"] or scenario["observation"]["status"] == "fail" for scenario in scenarios):
            raise SystemExit(1)
        return

    total_cells = len(CAREERS) * len(SLOT_CONFIGS) * len(PROGRESS_STAGES) * len(PREFERENCE_MODES)
    print(f"Running coverage audit against {args.api_url}...")
    print(f"Grid: {len(CAREERS)} careers × {len(SLOT_CONFIGS)} slot configs × "
          f"{len(PROGRESS_STAGES)} progress stages × {len(PREFERENCE_MODES)} pref modes "
          f"= {total_cells} cells")
    print()

    results: list[dict[str, Any]] = []
    cell_count = 0

    try:
        for career in CAREERS:
            for slot_label, slot_types in SLOT_CONFIGS:
                for progress_label, completed, curriculum in PROGRESS_STAGES:
                    for pref_mode, _pref_desc in PREFERENCE_MODES:
                        if pref_mode == "none":
                            preferred_tags: list[str] = []
                        elif pref_mode == "aligned":
                            preferred_tags = CAREER_ALIGNED_TAGS.get(career, [])
                        else:
                            preferred_tags = CAREER_CONFLICTING_TAGS.get(career, [])

                        cell = run_audit_cell(
                            career=career,
                            slot_label=slot_label,
                            slot_types=slot_types,
                            progress_label=progress_label,
                            completed=completed,
                            curriculum=curriculum,
                            pref_mode=pref_mode,
                            preferred_tags=preferred_tags,
                            api_url=args.api_url,
                            limit=args.limit,
                        )
                        results.append(cell)
                        cell_count += 1

                        # Show progress for long runs
                        if cell_count % 30 == 0:
                            print(f"  ... {cell_count}/{total_cells} cells done")

    except (HTTPError, URLError) as e:
        print(f"ERROR: Could not reach backend at {args.api_url}. Start the FastAPI backend first.")
        print(f"Details: {e}")
        sys.exit(1)

    print_summary_table(results)

    if args.output:
        output_path = Path(args.output)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with output_path.open("w") as f:
            json.dump(
                {
                    "mode": args.mode,
                    "apiUrl": args.api_url,
                    "provenance": capture_provenance(args.serving_revision, args.database_fingerprint),
                    "historicalInvariantNote": "Original limited checks retained; supplementary request/response checks are reported separately.",
                    "supplementaryViolationCount": sum(len(cell["supplementaryValidation"]["violations"]) for cell in results),
                    "totalCells": len(results),
                    "careers": CAREERS,
                    "slotConfigs": [sl for sl, _ in SLOT_CONFIGS],
                    "progressStages": [p for p, _, _ in PROGRESS_STAGES],
                    "preferenceModes": [m for m, _ in PREFERENCE_MODES],
                    "cells": results,
                },
                f,
                indent=2,
            )
            f.write("\n")
        print(f"Results written to {args.output}")

    # Exit nonzero only on invariant violations.
    all_violations = [v for r in results for v in r["invariantViolations"]]
    supplementary_failures = [message for cell in results for message in cell["supplementaryValidation"]["violations"]]
    for message in supplementary_failures:
        print(f"  [CONTRACT FAIL] {message}")
    all_violations += supplementary_failures
    if all_violations:
        print()
        print(f"AUDIT FAILED: {len(all_violations)} invariant violation(s). See above.")
        sys.exit(1)
    else:
        print("Audit complete. No invariant violations.")

if __name__ == "__main__":
    main()
