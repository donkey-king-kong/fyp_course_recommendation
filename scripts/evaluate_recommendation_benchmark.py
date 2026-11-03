"""Evaluate offline recommendation outputs against labelled benchmark cases.

The benchmark labels are still draft/manual-review data. This script does not
call the live recommender; it compares a saved predictions JSON file against
`data/recommendation_benchmark_cases.json`.
"""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path
from typing import Any

OLD_CODE_PREFIXES = ("CE", "CPE", "CSC", "CZ")
RELEVANCE_GAINS = {
    "highly-relevant": 3,
    "relevant": 2,
    "somewhat-relevant": 1,
    "irrelevant": 0,
}
RELEVANT_LABELS = {"highly-relevant", "relevant"}
METRIC_ORDER_NOTE = (
    "Rank-sensitive metrics sort predictions by backend score because "
    "recommendation responses are exact slot assignments for roadmap rendering."
)
LEGACY_VALIDITY_NOTE = (
    "Historical constraintValidity checks only nonempty/current codes, completed/fixed "
    "code exclusion and limited slot compatibility, over the score-ranked top K. "
    "Supplementary validation uses the complete response; it does not prove academic "
    "or programme eligibility. Missing evidence is reported as not-observable."
)
SCORE_COMPONENTS = (
    "careerTagScore", "careerSkillScore", "currentSemesterBonus", "preferenceBoost",
    "sameFacultyBoost", "mpeSpecialisationBoost", "legacyCodePenalty",
    "defaultProfileAdjustment", "prerequisitePlanningPenalty", "unlockContribution",
)

# Compact benchmark inputs may contain strings or positioned curriculum records.
def curriculum_code(item: Any) -> str:
    value = item.get("courseCode", "") if isinstance(item, dict) else item
    return str(value or "").strip().upper()

def fixed_curriculum_items(request: dict[str, Any]) -> list[Any]:
    return [
        item for item in request.get("curriculumCourses", [])
        if not (isinstance(item, dict) and item.get("isChoiceSlot"))
        and "XXX" not in curriculum_code(item)
        and curriculum_code(item) not in {"BDE", "MPE"}
    ]

def semester_position(item: dict[str, Any]) -> tuple[int, int] | None:
    year, semester = item.get("year"), item.get("semester")
    if isinstance(year, int) and not isinstance(year, bool) and year > 0 and semester in (1, 2):
        return year, semester
    return None

def is_number(value: Any) -> bool:
    return isinstance(value, (int, float)) and not isinstance(value, bool) and math.isfinite(value)

def validation_check(checked: int, failures: list[str], skipped: int = 0) -> dict[str, Any]:
    return {
        "status": "fail" if failures else "pass" if checked else "not-observable",
        "checked": checked,
        "skipped": skipped,
        "violations": failures,
    }

# This checker reads output contracts; it never reconstructs prerequisite or programme policy.
def validate_response(request: dict[str, Any], response: dict[str, Any]) -> dict[str, Any]:
    recommendations = response.get("recommendations", [])
    slots = request.get("choiceSlots", [])
    slots_by_id = {slot["slotId"]: slot for slot in slots if slot.get("slotId")}
    all_slots_identified = bool(slots) and len(slots_by_id) == len(slots)
    limit = request.get("limit")
    budget_failures = []
    if isinstance(limit, int) and len(recommendations) > limit:
        budget_failures.append(f"Returned {len(recommendations)} recommendations for limit={limit}.")
    checks = {"resultBudget": validation_check(int(isinstance(limit, int)), budget_failures)}

    slot_failures, duplicate_slot_failures, duplicate_code_failures = [], [], []
    seen_slots, seen_codes = set(), set()
    slot_checked = 0
    score_failures, score_skipped = [], 0
    nodes_by_id = {
        item["nodeId"]: item for item in request.get("curriculumCourses", [])
        if isinstance(item, dict) and item.get("nodeId")
    }
    nodes_by_id.update(slots_by_id)
    for rec in recommendations:
        for node in rec.get("plannedRoadmapNodes", []):
            if node.get("id"):
                nodes_by_id[node["id"]] = node

    for rec in recommendations:
        code, slot_id = prediction_course_code(rec), prediction_slot_id(rec)
        if slot_id and slot_id in seen_slots:
            duplicate_slot_failures.append(f"Slot {slot_id} is assigned more than once.")
        if slot_id:
            seen_slots.add(slot_id)
        if code in seen_codes:
            duplicate_code_failures.append(f"Module {code} is assigned more than once.")
        seen_codes.add(code)
        slot = slots_by_id.get(slot_id)
        if slot or all_slots_identified:
            slot_checked += 1
            if slot is None:
                slot_failures.append(f"{code} has unknown or missing exact slot ID {slot_id!r}.")
            else:
                for request_key, response_key in (
                    ("year", "matchedChoiceSlotYear"), ("semester", "matchedChoiceSlotSemester"),
                ):
                    if slot.get(request_key) is not None and rec.get(response_key) != slot[request_key]:
                        slot_failures.append(f"{code}: {response_key} differs from request slot {slot_id}.")
        breakdown = rec.get("scoreBreakdown") or {}
        if not all(is_number(breakdown.get(key)) for key in (*SCORE_COMPONENTS, "finalScore")) or not is_number(rec.get("score")):
            score_skipped += 1
        else:
            expected = max(1, sum(breakdown[key] for key in SCORE_COMPONENTS))
            if breakdown["finalScore"] != expected or rec["score"] != breakdown["finalScore"]:
                score_failures.append(
                    f"{code}: score={rec['score']}, finalScore={breakdown['finalScore']}, "
                    f"floored component sum={expected}."
                )
    checks.update({
        "knownExactSlots": validation_check(slot_checked, slot_failures, len(recommendations) - slot_checked),
        "uniqueSlotAssignments": validation_check(len(seen_slots), duplicate_slot_failures, len(recommendations) - sum(bool(prediction_slot_id(rec)) for rec in recommendations)),
        "uniqueModuleAssignments": validation_check(len(recommendations), duplicate_code_failures),
        "scoreConsistency": validation_check(len(recommendations) - score_skipped, score_failures, score_skipped),
    })

    endpoint_failures, placement_failures = [], []
    edge_count, placement_count, placement_skipped = 0, 0, 0
    completed = {curriculum_code(code) for code in request.get("completedCourseCodes", [])}
    for rec in recommendations:
        for edge in rec.get("plannedRoadmapEdges", []):
            edge_count += 1
            source, target = nodes_by_id.get(edge.get("source")), nodes_by_id.get(edge.get("target"))
            if source is None or target is None:
                endpoint_failures.append(f"Dangling planning edge {edge.get('source')} -> {edge.get('target')}.")
                placement_skipped += 1
                continue
            if curriculum_code(source) in completed:
                placement_skipped += 1
                continue
            source_position, target_position = semester_position(source), semester_position(target)
            if source_position is None or target_position is None:
                placement_skipped += 1
            else:
                placement_count += 1
                if source_position >= target_position:
                    placement_failures.append(f"Prerequisite edge {edge['source']} -> {edge['target']} is not strictly earlier.")
        target = slots_by_id.get(prediction_slot_id(rec), {
            "year": rec.get("matchedChoiceSlotYear"), "semester": rec.get("matchedChoiceSlotSemester"),
        })
        for node in rec.get("plannedRoadmapNodes", []):
            source_position, target_position = semester_position(node), semester_position(target)
            if source_position is None or target_position is None:
                placement_skipped += 1
            else:
                placement_count += 1
                if source_position >= target_position:
                    placement_failures.append(f"Planned node {node.get('id')} does not precede {prediction_slot_id(rec)}.")
    artifact_fields_present = all("plannedRoadmapNodes" in rec and "plannedRoadmapEdges" in rec for rec in recommendations)
    checks.update({
        "planningEdgeEndpoints": validation_check(edge_count or int(artifact_fields_present and bool(recommendations)), endpoint_failures),
        "precedingPrerequisitePlacement": validation_check(placement_count, placement_failures, placement_skipped),
    })
    failures = [message for check in checks.values() for message in check["violations"]]
    return {"scope": "request-response-contract-only", "recommendationCount": len(recommendations), "checks": checks, "violations": failures}

def load_json(path: Path) -> dict[str, Any]:
    with path.open() as file:
        return json.load(file)

def normalise_predictions(raw_predictions: dict[str, Any]) -> dict[str, list[dict[str, Any]]]:
    if isinstance(raw_predictions.get("cases"), list):
        return {
            case["caseId"]: case.get("recommendations", case.get("reviewedCandidates", []))
            for case in raw_predictions["cases"]
        }

    return {
        case_id: recommendations
        for case_id, recommendations in raw_predictions.items()
        if isinstance(recommendations, list)
    }

def reviewed_candidates_as_predictions(benchmark: dict[str, Any]) -> dict[str, list[dict[str, Any]]]:
    return {
        case["caseId"]: case.get("reviewedCandidates", [])
        for case in benchmark.get("cases", [])
    }

def candidate_lookup(case: dict[str, Any]) -> dict[str, dict[str, Any]]:
    return {
        candidate["courseCode"]: candidate
        for candidate in case.get("reviewedCandidates", [])
    }

def prediction_course_code(prediction: dict[str, Any]) -> str:
    return str(prediction.get("courseCode", "")).strip().upper()

def prediction_slot_id(prediction: dict[str, Any]) -> str | None:
    return prediction.get("matchedChoiceSlotId") or prediction.get("targetSlotId")

def prediction_score(prediction: dict[str, Any]) -> float | None:
    score = prediction.get("score")

    return float(score) if isinstance(score, (int, float)) else None

def display_career_goal(career_goal: str) -> str:
    return career_goal.replace("-", " ").title()

def is_old_code(course_code: str) -> bool:
    return course_code.startswith(OLD_CODE_PREFIXES)

def gain_for_prediction(prediction: dict[str, Any], candidates: dict[str, dict[str, Any]]) -> int:
    course_code = prediction_course_code(prediction)
    expected_label = candidates.get(course_code, {}).get("expectedRelevance", "irrelevant")
    return RELEVANCE_GAINS.get(expected_label, 0)

def dcg(gains: list[int]) -> float:
    return sum(gain / math.log2(index + 2) for index, gain in enumerate(gains))

def ndcg_at_k(predictions: list[dict[str, Any]], candidates: dict[str, dict[str, Any]], k: int) -> float:
    predicted_gains = [
        gain_for_prediction(prediction, candidates)
        for prediction in predictions[:k]
    ]
    ideal_gains = sorted(
        (
            RELEVANCE_GAINS.get(candidate.get("expectedRelevance", "irrelevant"), 0)
            for candidate in candidates.values()
            if candidate.get("oldCodeHandling") != "excluded"
        ),
        reverse=True,
    )[:k]
    ideal_dcg = dcg(ideal_gains)
    return dcg(predicted_gains) / ideal_dcg if ideal_dcg else 0.0

def rank_predictions_for_relevance_metrics(predictions: list[dict[str, Any]]) -> list[dict[str, Any]]:
    # Recommendation responses are exact slot assignments, so response order follows roadmap slots.
    # Rank-sensitive offline metrics should use the backend score instead of slot display order.
    return [
        prediction
        for _, prediction in sorted(
            enumerate(predictions),
            key=lambda indexed_prediction: (
                -prediction_score(indexed_prediction[1])
                if prediction_score(indexed_prediction[1]) is not None
                else 0,
                indexed_prediction[0],
            ),
        )
    ]

def ranked_prediction_summary(predictions: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [
        {
            "courseCode": prediction_course_code(prediction),
            "score": prediction_score(prediction),
            "matchedChoiceSlotId": prediction_slot_id(prediction),
        }
        for prediction in rank_predictions_for_relevance_metrics(predictions)
    ]

def assigned_slot_ids(predictions: list[dict[str, Any]], case: dict[str, Any]) -> set[str]:
    valid_slot_ids = {slot["slotId"] for slot in case.get("choiceSlots", [])}
    return {
        slot_id
        for slot_id in (prediction_slot_id(prediction) for prediction in predictions)
        if slot_id in valid_slot_ids
    }

def career_skill_path(prediction: dict[str, Any]) -> str | None:
    evidence = (
        prediction.get("scoreBreakdown", {})
        .get("careerSkillEvidence")
    )
    if not evidence:
        return None

    career_goal = evidence.get("careerGoal")
    skill_area = evidence.get("skillArea")
    tag = evidence.get("tag")
    title = prediction.get("title")
    if not all([career_goal, skill_area, tag, title]):
        return None

    return f"{display_career_goal(career_goal)} -> {skill_area} -> {tag} -> {title}"

def slot_fits(prediction: dict[str, Any], case: dict[str, Any]) -> bool:
    slot_id = prediction_slot_id(prediction)
    if slot_id is None:
        return False

    slot = next((item for item in case.get("choiceSlots", []) if item["slotId"] == slot_id), None)
    if slot is None:
        return False

    course_code = prediction_course_code(prediction)
    slot_code = slot["courseCode"]
    if slot_code == "BDE":
        return True
    if slot_code.startswith("SC") and course_code.startswith("SC"):
        return len(course_code) > 2 and len(slot_code) > 2 and course_code[2] == slot_code[2]
    return course_code == slot_code

def prediction_is_constraint_valid(prediction: dict[str, Any], case: dict[str, Any]) -> bool:
    course_code = prediction_course_code(prediction)
    completed_codes = {code.upper() for code in case.get("completedCourseCodes", [])}
    curriculum_codes = {curriculum_code(item) for item in fixed_curriculum_items(case)}
    return (
        bool(course_code)
        and not is_old_code(course_code)
        and course_code not in completed_codes
        and course_code not in curriculum_codes
        and slot_fits(prediction, case)
    )

def evaluate_case(case: dict[str, Any], predictions: list[dict[str, Any]], k: int) -> dict[str, Any]:
    ranked_predictions = rank_predictions_for_relevance_metrics(predictions)
    top_predictions = ranked_predictions[:k]
    candidates = candidate_lookup(case)
    relevant_count = sum(
        1
        for prediction in top_predictions
        if candidates.get(prediction_course_code(prediction), {}).get("expectedRelevance") in RELEVANT_LABELS
    )
    returned_relevant_count = sum(
        1
        for prediction in ranked_predictions
        if candidates.get(prediction_course_code(prediction), {}).get("expectedRelevance") in RELEVANT_LABELS
    )
    old_code_count = sum(1 for prediction in top_predictions if is_old_code(prediction_course_code(prediction)))
    valid_count = sum(1 for prediction in top_predictions if prediction_is_constraint_valid(prediction, case))
    expected_slot_count = len(case.get("choiceSlots", []))
    assigned_slot_count = len(assigned_slot_ids(predictions, case))
    evidence_predictions = [
        prediction
        for prediction in top_predictions
        if prediction.get("scoreBreakdown", {}).get("careerSkillEvidence")
    ]
    explanation_checks = []
    for prediction in top_predictions:
        expected_path = candidates.get(prediction_course_code(prediction), {}).get("expectedSkillPath")
        actual_path = career_skill_path(prediction)
        if expected_path and not expected_path.startswith("N/A"):
            explanation_checks.append(actual_path == expected_path)

    skill_areas = {
        prediction.get("scoreBreakdown", {}).get("careerSkillEvidence", {}).get("skillArea")
        for prediction in top_predictions
        if prediction.get("scoreBreakdown", {}).get("careerSkillEvidence")
    }
    skill_areas.discard(None)

    return {
        "caseId": case["caseId"],
        "recommendationCount": len(top_predictions),
        "rankedCourseOrder": ranked_prediction_summary(predictions)[:k],
        "precisionAtK": relevant_count / k,
        "ndcgAtK": ndcg_at_k(top_predictions, candidates, k),
        "precisionAtReturned": (
            returned_relevant_count / len(ranked_predictions)
            if ranked_predictions
            else 0.0
        ),
        "ndcgAtReturned": (
            ndcg_at_k(ranked_predictions, candidates, len(ranked_predictions))
            if ranked_predictions
            else 0.0
        ),
        "expectedSlotCount": expected_slot_count,
        "assignedSlotCount": assigned_slot_count,
        "slotFillRate": (
            min(assigned_slot_count, expected_slot_count) / expected_slot_count
            if expected_slot_count
            else 0.0
        ),
        "explanationCoverage": len(evidence_predictions) / len(top_predictions) if top_predictions else 0.0,
        "explanationFidelity": (
            sum(1 for item in explanation_checks if item) / len(explanation_checks)
            if explanation_checks
            else None
        ),
        "skillAreaDiversityAtK": len(skill_areas),
        "oldCodeExposure": old_code_count,
        "constraintValidity": valid_count / len(top_predictions) if top_predictions else 0.0,
    }

def average(values: list[float]) -> float:
    return sum(values) / len(values) if values else 0.0

def evaluate_benchmark(
    benchmark: dict[str, Any],
    predictions_by_case: dict[str, list[dict[str, Any]]],
    k: int,
    captures_by_case: dict[str, dict[str, Any]] | None = None,
) -> dict[str, Any]:
    case_results = [
        evaluate_case(case, predictions_by_case.get(case["caseId"], []), k)
        for case in benchmark.get("cases", [])
    ]
    fidelity_values = [
        result["explanationFidelity"]
        for result in case_results
        if result["explanationFidelity"] is not None
    ]
    total_predictions = sum(result["recommendationCount"] for result in case_results)
    cases_with_predictions = sum(1 for result in case_results if result["recommendationCount"] > 0)
    captures_by_case = captures_by_case or {}
    for case, result in zip(benchmark.get("cases", []), case_results):
        capture = captures_by_case.get(case["caseId"], {})
        result["supplementaryValidation"] = validate_response(
            capture.get("request", case),
            capture.get("response", {"recommendations": predictions_by_case.get(case["caseId"], [])}),
        )

    return {
        "k": k,
        "metricOrder": "backend-score-desc",
        "metricOrderNote": METRIC_ORDER_NOTE,
        "constraintValidityNote": LEGACY_VALIDITY_NOTE,
        "supplementaryViolationCount": sum(len(result["supplementaryValidation"]["violations"]) for result in case_results),
        "caseCount": len(case_results),
        "caseCoverage": cases_with_predictions / len(case_results) if case_results else 0.0,
        "totalPredictionsEvaluated": total_predictions,
        "averagePrecisionAtK": average([result["precisionAtK"] for result in case_results]),
        "averageNdcgAtK": average([result["ndcgAtK"] for result in case_results]),
        "averagePrecisionAtReturned": average(
            [result["precisionAtReturned"] for result in case_results]
        ),
        "averageNdcgAtReturned": average([result["ndcgAtReturned"] for result in case_results]),
        "averageSlotFillRate": average([result["slotFillRate"] for result in case_results]),
        "averageExplanationCoverage": average([result["explanationCoverage"] for result in case_results]),
        "averageExplanationFidelity": average(fidelity_values),
        "averageSkillAreaDiversityAtK": average([result["skillAreaDiversityAtK"] for result in case_results]),
        "oldCodeExposure": sum(result["oldCodeExposure"] for result in case_results),
        "averageConstraintValidity": average([result["constraintValidity"] for result in case_results]),
        "cases": case_results,
    }

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Evaluate saved recommendation predictions against benchmark cases."
    )
    parser.add_argument(
        "--benchmark",
        default="data/recommendation_benchmark_cases.json",
        help="Path to the benchmark cases JSON file.",
    )
    parser.add_argument(
        "--predictions",
        help="Path to saved recommendation predictions JSON. Omit with --use-reviewed-candidates for a smoke run.",
    )
    parser.add_argument(
        "--use-reviewed-candidates",
        action="store_true",
        help="Use reviewedCandidates as draft predictions. This is for smoke testing only.",
    )
    parser.add_argument("--k", type=int, default=5, help="Ranking cutoff for @K metrics.")
    parser.add_argument("--fail-on-contract-violations", action="store_true", help="Exit nonzero on supplementary response violations; historical metrics are still printed.")
    return parser.parse_args()

def main() -> None:
    args = parse_args()
    benchmark = load_json(Path(args.benchmark))
    if args.predictions:
        raw_predictions = load_json(Path(args.predictions))
        predictions_by_case = normalise_predictions(raw_predictions)
    elif args.use_reviewed_candidates:
        predictions_by_case = reviewed_candidates_as_predictions(benchmark)
    else:
        raise SystemExit("Provide --predictions or use --use-reviewed-candidates for a smoke run.")

    captures = {case["caseId"]: case for case in raw_predictions.get("cases", [])} if args.predictions else {}
    result = evaluate_benchmark(benchmark, predictions_by_case, args.k, captures)
    print(json.dumps(result, indent=2))
    if args.fail_on_contract_violations and result["supplementaryViolationCount"]:
        raise SystemExit(1)

if __name__ == "__main__":
    main()
