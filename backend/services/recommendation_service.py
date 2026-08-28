import logging
import re
from typing import Optional

from sqlalchemy import and_, or_
from sqlalchemy.orm import Session

from backend.models import ModuleModel
from backend.schemas.recommendation import (
    CourseRecommendation,
    RecommendationChoiceSlot,
    RecommendationPrerequisite,
    RecommendationResponse,
)
from backend.services.faculty_service import list_active_faculty_names
from backend.services.module_service import get_prerequisites_by_module

# First recommendation MVP: one career goal with hand-picked keywords.
# Later milestones can replace or enrich this with job-market data, embeddings, or graph logic.
SOFTWARE_ENGINEER_KEYWORDS = {
    "software": 4,
    "engineering": 3,
    "programming": 4,
    "development": 4,
    "database": 4,
    "web": 4,
    "cloud": 3,
    "distributed": 4,
    "systems": 2,
    "algorithm": 3,
    "architecture": 3,
    "testing": 2,
    "security": 3,
}

CHOICE_SLOT_LEVEL_PATTERN = re.compile(r"^[A-Z]{2}([3-4])xxx$", re.IGNORECASE)
logger = logging.getLogger(__name__)

# Keep debug logs readable while still showing enough candidates to diagnose missed slots.
def summarize_codes(codes: list[str], max_items: int = 80) -> str:
    visible_codes = codes[:max_items]
    suffix = "" if len(codes) <= max_items else f", ... +{len(codes) - max_items} more"

    return ", ".join(visible_codes) + suffix

# Builds rule-based recommendations from module catalog data and the student's current profile state.
def recommend_courses(
    db: Session,
    career_goal: str,
    completed_course_codes: list[str],
    choice_slot_codes: list[str],
    choice_slots: list[RecommendationChoiceSlot],
    excluded_course_codes: list[str],
    excluded_course_titles: list[str],
    limit: int,
) -> RecommendationResponse:
    # Keep unsupported career goals empty instead of pretending we can recommend them.
    if career_goal != "software-engineer":
        return RecommendationResponse(careerGoal=career_goal, recommendations=[])

    completed_codes = {course_code.upper() for course_code in completed_course_codes}
    excluded_codes = {course_code.upper() for course_code in excluded_course_codes}
    excluded_titles = {normalize_title(title) for title in excluded_course_titles}
    candidate_slots = build_recommendation_choice_slots(choice_slot_codes, choice_slots)
    mpe_levels = get_mpe_candidate_levels([slot.courseCode for slot in candidate_slots])
    has_bde_slot = any(slot.courseCode.upper() == "BDE" for slot in candidate_slots)
    active_faculties = list_active_faculty_names(db)
    slot_filters = build_slot_filters(mpe_levels, has_bde_slot)

    if not candidate_slots or not slot_filters:
        return RecommendationResponse(careerGoal=career_goal, recommendations=[])

    # Filter by keywords in SQL first so BDE does not load the entire catalog.
    query = db.query(ModuleModel).filter(
        ModuleModel.faculty.in_(active_faculties),
        or_(*slot_filters),
        or_(*build_keyword_filters()),
    )
    modules = query.order_by(ModuleModel.code).all()
    logger.info(
        "Recommendation initial candidates: count=%s, limit=%s, slots=%s, codes=%s",
        len(modules),
        limit,
        [slot.courseCode for slot in candidate_slots],
        summarize_codes([module.code for module in modules]),
    )
    prerequisites_by_module = get_prerequisites_by_module(db, [module.code for module in modules])
    prerequisite_modules_by_code = get_prerequisite_modules_by_code(db, prerequisites_by_module)
    recommendations_by_slot: dict[str, list[CourseRecommendation]] = {}

    for module in modules:
        if is_excluded_module(module, completed_codes | excluded_codes, excluded_titles):
            continue

        eligible_slots = get_matching_choice_slots(module, candidate_slots)

        if not eligible_slots:
            continue

        # Rank remaining modules by career keyword matches in title and description.
        matched_keywords, score = score_software_engineer_match(module)

        if score == 0:
            continue

        # Keep missing prerequisites so the UI can place them into an earlier slot.
        prerequisites = prerequisites_by_module.get(module.code, [])
        missing_prerequisites = [
            prerequisite for prerequisite in prerequisites if prerequisite not in completed_codes
        ]
        prerequisite_recommendations = build_prerequisite_recommendations(
            missing_prerequisites,
            prerequisite_modules_by_code,
            completed_codes | excluded_codes,
            excluded_titles,
        )

        for slot in eligible_slots:
            slot_key = get_choice_slot_identity(slot)
            recommendations_by_slot.setdefault(slot_key, []).append(
                CourseRecommendation(
                    courseCode=module.code,
                    title=module.title,
                    academicUnits=module.au,
                    faculty=module.faculty,
                    level=module.level,
                    matchedChoiceSlot=normalize_choice_slot_code(slot.courseCode),
                    matchedChoiceSlotId=slot.slotId,
                    matchedChoiceSlotYear=slot.year,
                    matchedChoiceSlotSemester=slot.semester,
                    matchedKeywords=matched_keywords,
                    missingPrerequisites=missing_prerequisites,
                    prerequisiteRecommendations=prerequisite_recommendations,
                    score=score,
                    reason=build_recommendation_reason(matched_keywords),
                )
            )

    sorted_recommendations = flatten_ranked_slot_recommendations(
        candidate_slots,
        recommendations_by_slot,
        limit,
    )
    final_recommendations = sorted_recommendations
    logger.info(
        "Recommendation ranked before cut: count=%s, items=%s",
        len(sorted_recommendations),
        summarize_recommendations(sorted_recommendations),
    )
    logger.info(
        "Recommendation final cut: count=%s, items=%s",
        len(final_recommendations),
        summarize_recommendations(final_recommendations),
    )

    return RecommendationResponse(
        careerGoal=career_goal,
        recommendations=final_recommendations,
    )

def normalize_title(title: str) -> str:
    return " ".join(title.lower().split())

def build_recommendation_choice_slots(
    choice_slot_codes: list[str],
    choice_slots: list[RecommendationChoiceSlot],
) -> list[RecommendationChoiceSlot]:
    if choice_slots:
        return choice_slots

    return [
        RecommendationChoiceSlot(courseCode=course_code)
        for course_code in choice_slot_codes
    ]

def build_slot_filters(mpe_levels: list[int], has_bde_slot: bool) -> list:
    filters = []

    if mpe_levels:
        filters.append(and_(ModuleModel.faculty == "CSC", ModuleModel.level.in_(mpe_levels)))

    if has_bde_slot:
        filters.append(ModuleModel.code.is_not(None))

    return filters

def get_choice_slot_identity(slot: RecommendationChoiceSlot) -> str:
    if slot.slotId:
        return slot.slotId

    return f"{normalize_choice_slot_code(slot.courseCode)}-{slot.year}-{slot.semester}"

def get_prerequisite_modules_by_code(
    db: Session,
    prerequisites_by_module: dict[str, list[str]],
) -> dict[str, ModuleModel]:
    prerequisite_codes = {
        prerequisite
        for prerequisites in prerequisites_by_module.values()
        for prerequisite in prerequisites
    }

    if not prerequisite_codes:
        return {}

    prerequisite_modules = db.query(ModuleModel).filter(
        ModuleModel.code.in_(prerequisite_codes)
    ).all()

    return {module.code: module for module in prerequisite_modules}

def is_excluded_module(
    module: ModuleModel,
    excluded_codes: set[str],
    excluded_titles: set[str],
) -> bool:
    return module.code in excluded_codes or normalize_title(module.title) in excluded_titles

def build_prerequisite_recommendations(
    missing_prerequisites: list[str],
    prerequisite_modules_by_code: dict[str, ModuleModel],
    excluded_codes: set[str],
    excluded_titles: set[str],
) -> list[RecommendationPrerequisite]:
    recommendations: list[RecommendationPrerequisite] = []

    for prerequisite in missing_prerequisites:
        prerequisite_module = prerequisite_modules_by_code.get(prerequisite)

        if not prerequisite_module:
            continue

        if is_excluded_module(prerequisite_module, excluded_codes, excluded_titles):
            continue

        recommendations.append(
            RecommendationPrerequisite(
                courseCode=prerequisite_module.code,
                title=prerequisite_module.title,
                academicUnits=prerequisite_module.au,
                faculty=prerequisite_module.faculty,
                level=prerequisite_module.level,
            )
        )

    return recommendations

def build_keyword_filters() -> list:
    filters = []

    for keyword in SOFTWARE_ENGINEER_KEYWORDS:
        pattern = f"%{keyword}%"
        filters.append(ModuleModel.title.ilike(pattern))
        filters.append(ModuleModel.description.ilike(pattern))

    return filters

def get_mpe_slot_level(choice_slot_code: str) -> Optional[int]:
    match = CHOICE_SLOT_LEVEL_PATTERN.match(choice_slot_code.strip())

    return int(match.group(1)) if match else None

def get_mpe_candidate_levels(choice_slot_codes: list[str]) -> list[int]:
    # SC3xxx means recommend 3000-level modules; SC4xxx means recommend 4000-level modules.
    levels = {
        level
        for code in choice_slot_codes
        if (level := get_mpe_slot_level(code))
    }

    return sorted(levels)

def get_matching_choice_slots(
    module: ModuleModel,
    choice_slots: list[RecommendationChoiceSlot],
) -> list[RecommendationChoiceSlot]:
    matching_slots: list[RecommendationChoiceSlot] = []

    for slot in choice_slots:
        slot_code = normalize_choice_slot_code(slot.courseCode)
        mpe_level = get_mpe_slot_level(slot_code)

        # MPE slots must stay within CSC and match the placeholder level.
        if mpe_level and module.faculty == "CSC" and module.level == mpe_level:
            matching_slots.append(slot)
            continue

        # BDE is broader, but each BDE slot should still fit its roadmap year level.
        if slot_code == "BDE" and can_fit_bde_slot(module, slot):
            matching_slots.append(slot)

    return matching_slots

def can_fit_bde_slot(module: ModuleModel, slot: RecommendationChoiceSlot) -> bool:
    if slot.year is None:
        return True

    return module.level == get_preferred_bde_level(slot.year)

def get_preferred_bde_level(year: int) -> int:
    return min(max(year, 1), 4)

def normalize_choice_slot_code(choice_slot_code: str) -> str:
    normalized_code = choice_slot_code.strip().upper()

    if normalized_code == "BDE":
        return "BDE"

    mpe_level = get_mpe_slot_level(normalized_code)

    return f"SC{mpe_level}xxx" if mpe_level else choice_slot_code

def flatten_ranked_slot_recommendations(
    choice_slots: list[RecommendationChoiceSlot],
    recommendations_by_slot: dict[str, list[CourseRecommendation]],
    limit: int,
) -> list[CourseRecommendation]:
    sorted_recommendations_by_slot = {
        get_choice_slot_identity(slot): sorted(
            recommendations_by_slot.get(get_choice_slot_identity(slot), []),
            key=lambda recommendation: (
                -recommendation.score,
                recommendation.courseCode,
            ),
        )
        for slot in choice_slots
    }
    ranked_recommendations: list[CourseRecommendation] = []
    used_course_codes: set[str] = set()
    used_course_titles: set[str] = set()
    candidate_index = 0

    while len(ranked_recommendations) < limit:
        added_this_round = False

        for slot in choice_slots:
            slot_recommendations = sorted_recommendations_by_slot[get_choice_slot_identity(slot)]
            unique_recommendation = get_unique_recommendation_at_or_after_index(
                slot_recommendations,
                candidate_index,
                used_course_codes,
                used_course_titles,
            )

            if not unique_recommendation:
                continue

            ranked_recommendations.append(unique_recommendation)
            used_course_codes.add(unique_recommendation.courseCode)
            used_course_titles.add(normalize_title(unique_recommendation.title))
            added_this_round = True

            if len(ranked_recommendations) >= limit:
                break

        if not added_this_round:
            break

        candidate_index += 1

    return ranked_recommendations

def get_unique_recommendation_at_or_after_index(
    recommendations: list[CourseRecommendation],
    start_index: int,
    used_course_codes: set[str],
    used_course_titles: set[str],
) -> Optional[CourseRecommendation]:
    for recommendation in recommendations[start_index:]:
        recommendation_title = normalize_title(recommendation.title)

        if (
            recommendation.courseCode not in used_course_codes and
            recommendation_title not in used_course_titles
        ):
            return recommendation

    return None

def score_software_engineer_match(module: ModuleModel) -> tuple[list[str], int]:
    searchable_text = f"{module.title} {module.description or ''}".lower()
    matched_keywords = [
        keyword for keyword in SOFTWARE_ENGINEER_KEYWORDS if keyword in searchable_text
    ]
    score = sum(SOFTWARE_ENGINEER_KEYWORDS[keyword] for keyword in matched_keywords)

    # Prefer modules currently available in the catalog by giving them a small boost.
    if module.is_current_semester:
        score += 1

    return matched_keywords, score

def build_recommendation_reason(matched_keywords: list[str]) -> str:
    return (
        "Matches Software Engineer keywords: "
        f"{', '.join(matched_keywords)}."
    )

def summarize_recommendations(
    recommendations: list[CourseRecommendation],
    max_items: int = 80,
) -> str:
    visible_recommendations = recommendations[:max_items]
    summary = [
        (
            f"{recommendation.courseCode}"
            f"(slot={recommendation.matchedChoiceSlot}, "
            f"level={recommendation.level}, "
            f"score={recommendation.score}, "
            f"missing={len(recommendation.missingPrerequisites)})"
        )
        for recommendation in visible_recommendations
    ]
    suffix = (
        ""
        if len(recommendations) <= max_items
        else f", ... +{len(recommendations) - max_items} more"
    )

    return ", ".join(summary) + suffix
