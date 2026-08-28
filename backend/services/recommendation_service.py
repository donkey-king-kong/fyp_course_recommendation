import logging
import re
from typing import Optional

from sqlalchemy import and_, or_
from sqlalchemy.orm import Session

from backend.models import ModuleModel
from backend.schemas.recommendation import (
    CourseRecommendation,
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

CHOICE_SLOT_LEVEL_PATTERN = re.compile(r"^[A-Z]{2}([3-4])xxx$")
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
    mpe_levels = get_mpe_candidate_levels(choice_slot_codes)
    has_bde_slot = any(code.upper() == "BDE" for code in choice_slot_codes)
    active_faculties = list_active_faculty_names(db)
    slot_filters = build_slot_filters(mpe_levels, has_bde_slot)

    if not slot_filters:
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
        choice_slot_codes,
        summarize_codes([module.code for module in modules]),
    )
    prerequisites_by_module = get_prerequisites_by_module(db, [module.code for module in modules])
    prerequisite_modules_by_code = get_prerequisite_modules_by_code(db, prerequisites_by_module)
    recommendations: list[CourseRecommendation] = []

    for module in modules:
        matched_choice_slot = get_matching_choice_slot(module, mpe_levels, has_bde_slot)

        if matched_choice_slot is None:
            continue

        if is_excluded_module(module, completed_codes | excluded_codes, excluded_titles):
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

        # Rank remaining modules by career keyword matches in title and description.
        matched_keywords, score = score_software_engineer_match(module)

        if score == 0:
            continue

        recommendations.append(
            CourseRecommendation(
                courseCode=module.code,
                title=module.title,
                academicUnits=module.au,
                faculty=module.faculty,
                level=module.level,
                matchedChoiceSlot=matched_choice_slot,
                matchedKeywords=matched_keywords,
                missingPrerequisites=missing_prerequisites,
                prerequisiteRecommendations=prerequisite_recommendations,
                score=score,
                reason=build_recommendation_reason(matched_keywords),
            )
        )

    sorted_recommendations = sorted(
        recommendations,
        key=lambda recommendation: (-recommendation.score, recommendation.courseCode),
    )
    final_recommendations = sorted_recommendations[:limit]
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

def build_slot_filters(mpe_levels: list[int], has_bde_slot: bool) -> list:
    filters = []

    if mpe_levels:
        filters.append(and_(ModuleModel.faculty == "CSC", ModuleModel.level.in_(mpe_levels)))

    if has_bde_slot:
        filters.append(ModuleModel.code.is_not(None))

    return filters

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

def get_mpe_candidate_levels(choice_slot_codes: list[str]) -> list[int]:
    # SC3xxx means recommend 3000-level modules; SC4xxx means recommend 4000-level modules.
    levels = {
        int(match.group(1))
        for code in choice_slot_codes
        if (match := CHOICE_SLOT_LEVEL_PATTERN.match(code))
    }

    return sorted(levels)

def get_matching_choice_slot(
    module: ModuleModel,
    mpe_levels: list[int],
    has_bde_slot: bool,
) -> Optional[str]:
    # MPE slots must stay within CSC and match the placeholder level.
    if module.faculty == "CSC" and module.level in mpe_levels:
        return f"SC{module.level}xxx"

    # BDE is broader: any active-faculty catalog module can be considered.
    if has_bde_slot:
        return "BDE"

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
