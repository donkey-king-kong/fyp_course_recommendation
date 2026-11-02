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
from run_recommendation_benchmark_predictions import post_json
from run_counterfactual_sensitivity import check_invariants, slot_fits_code

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
    """Build a recommendation request payload for an audit cell."""
    slots = build_slots(slot_types)
    return {
        "careerGoal": career,
        "preferredRecommendationTags": preferred_tags,
        "completedCourseCodes": completed,
        "excludedCourseCodes": curriculum,
        "choiceSlots": slots,
        "limit": limit,
        "majorCode": "CSC",
        "year": 3,
    }


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

    slots = build_slots(slot_types)
    inv_failures = check_invariants(recs, completed, slots, label=f"{career}/{slot_label}/{progress_label}/{pref_mode}")

    empty_slots = []
    filled_slot_ids = {r.get("matchedChoiceSlotId") or r.get("slotId") or r.get("choiceSlotId") for r in recs}
    for s in slots:
        if s["slotId"] not in filled_slot_ids:
            empty_slots.append(s["slotId"])

    return {
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
        "invariantViolations": inv_failures,
        "recommendedCodes": [r.get("courseCode", "") for r in recs],
    }


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
                        flag = "✓" if fill >= 1.0 and viol == 0 else "✗"
                        marker = ""
                        if interest > 0:
                            marker += f"i{interest}"
                        if low > 0:
                            marker += f"l{low}"
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
    return parser.parse_args()


def main() -> None:
    args = parse_args()

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
    if all_violations:
        print()
        print(f"AUDIT FAILED: {len(all_violations)} invariant violation(s). See above.")
        sys.exit(1)
    else:
        print("Audit complete. No invariant violations.")


if __name__ == "__main__":
    main()
