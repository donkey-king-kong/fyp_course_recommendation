import json
import math
from pathlib import Path
from typing import Any, Optional

from backend.schemas.admin import (
    AdminAnnotatedRecommendation,
    AdminBenchmarkCaseReviewItem,
    AdminBenchmarkCaseReviewResponse,
    AdminBenchmarkCaseDetailResponse,
    AdminBenchmarkReviewStatus,
    AdminBenchmarkCaseStatus,
    AdminBenchmarkCaseSummary,
    AdminBenchmarkPredictionSummary,
    AdminBenchmarkSummaryResponse,
    AdminReviewedCandidate,
)

PROJECT_ROOT = Path(__file__).resolve().parents[2]
BENCHMARK_CASES_PATH = PROJECT_ROOT / "data" / "recommendation_benchmark_cases.json"
BENCHMARK_PREDICTIONS_PATH = PROJECT_ROOT / "data" / "recommendation_benchmark_predictions.json"
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

def write_json(path: Path, data: dict[str, Any]) -> None:
    with path.open("w") as file:
        json.dump(data, file, indent=2)
        file.write("\n")

def prediction_course_code(prediction: dict[str, Any]) -> str:
    return str(prediction.get("courseCode", "")).strip().upper()

def prediction_slot_id(prediction: dict[str, Any]) -> Optional[str]:
    return prediction.get("matchedChoiceSlotId") or prediction.get("targetSlotId")

def prediction_score(prediction: dict[str, Any]) -> Optional[float]:
    score = prediction.get("score")

    return float(score) if isinstance(score, (int, float)) else None

def is_old_code(course_code: str) -> bool:
    return course_code.startswith(OLD_CODE_PREFIXES)

def normalise_predictions(raw_predictions: dict[str, Any]) -> dict[str, list[dict[str, Any]]]:
    return {
        case["caseId"]: case.get("recommendations", case.get("reviewedCandidates", []))
        for case in raw_predictions.get("cases", [])
    }

def prediction_case_lookup(raw_predictions: dict[str, Any]) -> dict[str, dict[str, Any]]:
    return {
        case["caseId"]: case
        for case in raw_predictions.get("cases", [])
    }

def case_lookup(benchmark: dict[str, Any]) -> dict[str, dict[str, Any]]:
    return {
        case["caseId"]: case
        for case in benchmark.get("cases", [])
    }

def candidate_lookup(case: dict[str, Any]) -> dict[str, dict[str, Any]]:
    return {
        candidate["courseCode"].upper(): candidate
        for candidate in case.get("reviewedCandidates", [])
    }

def gain_for_prediction(prediction: dict[str, Any], candidates: dict[str, dict[str, Any]]) -> int:
    expected_label = candidates.get(prediction_course_code(prediction), {}).get("expectedRelevance", "irrelevant")
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

def assigned_slot_ids(predictions: list[dict[str, Any]], case: dict[str, Any]) -> set[str]:
    valid_slot_ids = {slot["slotId"] for slot in case.get("choiceSlots", [])}
    return {
        slot_id
        for slot_id in (prediction_slot_id(prediction) for prediction in predictions)
        if slot_id in valid_slot_ids
    }

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
    curriculum_codes = {
        course.get("courseCode", "").upper() if isinstance(course, dict) else str(course).upper()
        for course in case.get("curriculumCourses", [])
    }
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
    valid_count = sum(1 for prediction in top_predictions if prediction_is_constraint_valid(prediction, case))
    expected_slot_count = len(case.get("choiceSlots", []))
    assigned_slot_count = len(assigned_slot_ids(predictions, case))
    old_code_count = sum(1 for prediction in top_predictions if is_old_code(prediction_course_code(prediction)))

    return {
        "caseId": case["caseId"],
        "recommendationCount": len(top_predictions),
        "precisionAtK": relevant_count / k,
        "ndcgAtK": ndcg_at_k(top_predictions, candidates, k),
        "expectedSlotCount": expected_slot_count,
        "assignedSlotCount": assigned_slot_count,
        "slotFillRate": (
            min(assigned_slot_count, expected_slot_count) / expected_slot_count
            if expected_slot_count
            else 0.0
        ),
        "oldCodeExposure": old_code_count,
        "constraintValidity": valid_count / len(top_predictions) if top_predictions else 0.0,
    }

def average(values: list[float]) -> float:
    return sum(values) / len(values) if values else 0.0

def admin_review_status(case: dict[str, Any]) -> AdminBenchmarkReviewStatus:
    status = case.get("adminReviewStatus", "unreviewed")
    if status in {"approved", "disapproved"}:
        return status
    return "unreviewed"

def benchmark_status(metrics: dict[str, Any]) -> AdminBenchmarkCaseStatus:
    if metrics["recommendationCount"] == 0:
        return "missing-predictions"
    if metrics["constraintValidity"] < 1 or metrics["ndcgAtK"] < 0.7:
        return "needs-review"
    return "ok"

def build_prediction_summary(
    predictions: list[dict[str, Any]],
    candidates: dict[str, dict[str, Any]],
    limit: int,
) -> list[AdminBenchmarkPredictionSummary]:
    return [
        AdminBenchmarkPredictionSummary(
            courseCode=prediction_course_code(prediction),
            title=str(prediction.get("title", "")),
            score=prediction_score(prediction),
            matchedChoiceSlotId=prediction_slot_id(prediction),
            expectedRelevance=candidates.get(prediction_course_code(prediction), {}).get("expectedRelevance", "unreviewed"),
        )
        for prediction in rank_predictions_for_relevance_metrics(predictions)[:limit]
    ]

def build_case_summary(
    case: dict[str, Any],
    predictions: list[dict[str, Any]],
    metrics: dict[str, Any],
    top_prediction_limit: int,
) -> AdminBenchmarkCaseSummary:
    candidates = candidate_lookup(case)
    return AdminBenchmarkCaseSummary(
        caseId=case["caseId"],
        description=case.get("description", ""),
        careerGoal=case.get("careerGoal", ""),
        studentFaculty=case.get("studentFaculty"),
        preferredRecommendationTags=case.get("preferredRecommendationTags", []),
        completedCourseCount=len(case.get("completedCourseCodes", [])),
        choiceSlotCount=len(case.get("choiceSlots", [])),
        reviewedCandidateCount=len(case.get("reviewedCandidates", [])),
        recommendationCount=metrics["recommendationCount"],
        precisionAtK=metrics["precisionAtK"],
        ndcgAtK=metrics["ndcgAtK"],
        slotFillRate=metrics["slotFillRate"],
        constraintValidity=metrics["constraintValidity"],
        status=benchmark_status(metrics),
        adminReviewStatus=admin_review_status(case),
        adminReviewNotes=case.get("adminReviewNotes"),
        topPredictions=build_prediction_summary(predictions, candidates, top_prediction_limit),
    )

def get_admin_benchmark_summary(k: int = 5) -> AdminBenchmarkSummaryResponse:
    benchmark = load_json(BENCHMARK_CASES_PATH)
    raw_predictions = load_json(BENCHMARK_PREDICTIONS_PATH)
    predictions_by_case = normalise_predictions(raw_predictions)
    case_metrics = [
        evaluate_case(case, predictions_by_case.get(case["caseId"], []), k)
        for case in benchmark.get("cases", [])
    ]
    summaries = [
        build_case_summary(
            case,
            predictions_by_case.get(case["caseId"], []),
            metrics,
            top_prediction_limit=k,
        )
        for case, metrics in zip(benchmark.get("cases", []), case_metrics)
    ]

    return AdminBenchmarkSummaryResponse(
        schemaVersion=benchmark.get("schemaVersion", "unknown"),
        benchmarkStatus=benchmark.get("status", ""),
        predictionGeneratedAt=raw_predictions.get("generatedAt"),
        predictionApiUrl=raw_predictions.get("apiUrl"),
        k=k,
        caseCount=len(case_metrics),
        averagePrecisionAtK=average([metrics["precisionAtK"] for metrics in case_metrics]),
        averageNdcgAtK=average([metrics["ndcgAtK"] for metrics in case_metrics]),
        averageSlotFillRate=average([metrics["slotFillRate"] for metrics in case_metrics]),
        averageConstraintValidity=average([metrics["constraintValidity"] for metrics in case_metrics]),
        oldCodeExposure=sum(metrics["oldCodeExposure"] for metrics in case_metrics),
        cases=sorted(summaries, key=lambda item: (item.status == "ok", item.ndcgAtK, item.caseId)),
    )

def build_annotated_recommendation(
    prediction: dict[str, Any],
    case: dict[str, Any],
    candidates: dict[str, dict[str, Any]],
) -> AdminAnnotatedRecommendation:
    course_code = prediction_course_code(prediction)
    candidate = candidates.get(course_code, {})
    return AdminAnnotatedRecommendation(
        courseCode=course_code,
        title=str(prediction.get("title", "")),
        score=prediction_score(prediction),
        matchedChoiceSlot=prediction.get("matchedChoiceSlot"),
        matchedChoiceSlotId=prediction_slot_id(prediction),
        readinessStatus=prediction.get("readinessStatus"),
        reason=prediction.get("reason"),
        expectedRelevance=candidate.get("expectedRelevance", "unreviewed"),
        expectedSkillPath=candidate.get("expectedSkillPath"),
        reviewNotes=candidate.get("reviewNotes"),
        constraintValid=prediction_is_constraint_valid(prediction, case),
        scoreBreakdown=prediction.get("scoreBreakdown", {}),
    )

def build_reviewed_candidate(
    candidate: dict[str, Any],
    ranked_predictions: list[dict[str, Any]],
) -> AdminReviewedCandidate:
    course_code = candidate["courseCode"].upper()
    predicted_index = next(
        (
            index
            for index, prediction in enumerate(ranked_predictions)
            if prediction_course_code(prediction) == course_code
        ),
        None,
    )
    matched_prediction = ranked_predictions[predicted_index] if predicted_index is not None else {}

    return AdminReviewedCandidate(
        courseCode=course_code,
        title=candidate.get("title", ""),
        targetSlotId=candidate.get("targetSlotId"),
        expectedRelevance=candidate.get("expectedRelevance", "irrelevant"),
        expectedSkillPath=candidate.get("expectedSkillPath"),
        oldCodeHandling=candidate.get("oldCodeHandling"),
        reviewNotes=candidate.get("reviewNotes"),
        wasRecommended=predicted_index is not None,
        predictedRank=predicted_index + 1 if predicted_index is not None else None,
        predictedScore=prediction_score(matched_prediction),
    )

def get_admin_benchmark_case_detail(case_id: str, k: int = 5) -> Optional[AdminBenchmarkCaseDetailResponse]:
    benchmark = load_json(BENCHMARK_CASES_PATH)
    raw_predictions = load_json(BENCHMARK_PREDICTIONS_PATH)
    cases_by_id = case_lookup(benchmark)
    prediction_cases_by_id = prediction_case_lookup(raw_predictions)
    case = cases_by_id.get(case_id)
    if case is None:
        return None

    prediction_case = prediction_cases_by_id.get(case_id, {})
    predictions = prediction_case.get("recommendations", [])
    ranked_predictions = rank_predictions_for_relevance_metrics(predictions)
    candidates = candidate_lookup(case)

    return AdminBenchmarkCaseDetailResponse(
        caseId=case["caseId"],
        description=case.get("description", ""),
        studentFaculty=case.get("studentFaculty"),
        careerGoal=case.get("careerGoal", ""),
        reviewerStatus=case.get("reviewerStatus"),
        adminReviewStatus=admin_review_status(case),
        adminReviewNotes=case.get("adminReviewNotes"),
        preferredRecommendationTags=case.get("preferredRecommendationTags", []),
        completedCourseCodes=case.get("completedCourseCodes", []),
        choiceSlots=case.get("choiceSlots", []),
        curriculumCourses=case.get("curriculumCourses", []),
        metrics=evaluate_case(case, predictions, k),
        request=prediction_case.get("request", {}),
        rankedRecommendations=[
            build_annotated_recommendation(prediction, case, candidates)
            for prediction in ranked_predictions
        ],
        reviewedCandidates=[
            build_reviewed_candidate(candidate, ranked_predictions)
            for candidate in case.get("reviewedCandidates", [])
        ],
    )

def update_admin_benchmark_case_reviews(
    reviews: list[AdminBenchmarkCaseReviewItem],
    k: int = 5,
) -> Optional[AdminBenchmarkCaseReviewResponse]:
    benchmark = load_json(BENCHMARK_CASES_PATH)
    cases_by_id = case_lookup(benchmark)
    updated_case_ids = []

    for review in reviews:
        case = cases_by_id.get(review.caseId)
        if case is None:
            return None

        case["adminReviewStatus"] = review.adminReviewStatus
        case["adminReviewNotes"] = review.adminReviewNotes or None
        updated_case_ids.append(review.caseId)

    write_json(BENCHMARK_CASES_PATH, benchmark)
    summary = get_admin_benchmark_summary(k=k)

    return AdminBenchmarkCaseReviewResponse(
        updatedCaseIds=updated_case_ids,
        cases=summary.cases,
    )
