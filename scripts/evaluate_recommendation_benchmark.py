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

    return f"{career_goal} -> {skill_area} -> {tag} -> {title}"


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
        return course_code[2] == slot_code[2]
    return course_code == slot_code


def prediction_is_constraint_valid(prediction: dict[str, Any], case: dict[str, Any]) -> bool:
    course_code = prediction_course_code(prediction)
    completed_codes = {code.upper() for code in case.get("completedCourseCodes", [])}
    curriculum_codes = {code.upper() for code in case.get("curriculumCourses", [])}
    return (
        bool(course_code)
        and not is_old_code(course_code)
        and course_code not in completed_codes
        and course_code not in curriculum_codes
        and slot_fits(prediction, case)
    )


def evaluate_case(case: dict[str, Any], predictions: list[dict[str, Any]], k: int) -> dict[str, Any]:
    top_predictions = predictions[:k]
    candidates = candidate_lookup(case)
    relevant_count = sum(
        1
        for prediction in top_predictions
        if candidates.get(prediction_course_code(prediction), {}).get("expectedRelevance") in RELEVANT_LABELS
    )
    old_code_count = sum(1 for prediction in top_predictions if is_old_code(prediction_course_code(prediction)))
    valid_count = sum(1 for prediction in top_predictions if prediction_is_constraint_valid(prediction, case))
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
        "precisionAtK": relevant_count / k,
        "ndcgAtK": ndcg_at_k(top_predictions, candidates, k),
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

    return {
        "k": k,
        "caseCount": len(case_results),
        "caseCoverage": cases_with_predictions / len(case_results) if case_results else 0.0,
        "totalPredictionsEvaluated": total_predictions,
        "averagePrecisionAtK": average([result["precisionAtK"] for result in case_results]),
        "averageNdcgAtK": average([result["ndcgAtK"] for result in case_results]),
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
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    benchmark = load_json(Path(args.benchmark))
    if args.predictions:
        predictions_by_case = normalise_predictions(load_json(Path(args.predictions)))
    elif args.use_reviewed_candidates:
        predictions_by_case = reviewed_candidates_as_predictions(benchmark)
    else:
        raise SystemExit("Provide --predictions or use --use-reviewed-candidates for a smoke run.")

    result = evaluate_benchmark(benchmark, predictions_by_case, args.k)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
