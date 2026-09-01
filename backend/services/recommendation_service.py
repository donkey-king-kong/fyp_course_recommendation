import logging
import re
from dataclasses import dataclass
from typing import Optional

from sqlalchemy import String, and_, or_
from sqlalchemy.orm import Session

from backend.models import ModuleModel
from backend.schemas.recommendation import (
    CourseRecommendation,
    RecommendationCareerSkillEvidence,
    RecommendationChoiceSlot,
    RecommendationCurriculumCourse,
    RecommendationPlannedRoadmapEdge,
    RecommendationPlannedRoadmapNode,
    RecommendationPrerequisite,
    RecommendationReadinessStatus,
    RecommendationResponse,
    RecommendationScoreBreakdown,
)
from backend.services.career_skill_mappings import CAREER_SKILL_MAPPINGS, CareerSkillMapping, SkillTagRelationship
from backend.services.faculty_service import list_active_faculty_names
from backend.services.module_service import get_prerequisites_by_module, get_unlocks_by_module

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
SOFTWARE_ENGINEER_TAG_WEIGHTS = {
    "software-engineering": 6,
    "programming": 3,
    "backend-engineering": 4,
    "frontend-engineering": 4,
    "web-development": 3,
    "database": 5,
    "computer-network": 5,
    "computer-security": 5,
    "algorithms": 5,
    "data-structures": 5,
    "operating-systems": 5,
    "distributed-systems": 5,
    "cloud-computing": 4,
    "ai-ml": 2,
    "data-science": 2,
    "compiler": 3,
    "parallel-computing": 2,
    "computer-architecture": 3,
}
# Used for near-duplicate titles where the curriculum and catalog use slightly different wording.
TITLE_SIGNATURE_STOP_WORDS = {"principle", "principles"}
TITLE_SIGNATURE_TOKEN_REPLACEMENTS = {
    "algorithms": "algorithm",
    "networks": "network",
    "structures": "structure",
    "systems": "system",
}
# Preferences should visibly influence ordering, but they remain soft boosts after hard checks.
PREFERENCE_TAG_BOOST = 30
SAME_FACULTY_BOOST = 8
DIVERSITY_TAG_REPEAT_PENALTY = 8
PREFERRED_DIVERSITY_TAG_REPEAT_PENALTY = 2
BROAD_DEFAULT_PROFILE_BOOST = 14
SPECIALIST_PROFILE_PENALTY = -16
EXTRA_PREREQUISITE_PLANNING_PENALTY = -10
# Old CE/CSC course-code families should not be recommended; current curricula use SC codes.
DEPRECATED_COURSE_CODE_PREFIXES = ("CE", "CSC", "CZ", "CPE")
CHOICE_SLOT_LEVEL_PATTERN = re.compile(r"^[A-Z]{2}([3-4])xxx$", re.IGNORECASE)
logger = logging.getLogger(__name__)

@dataclass
class RecommendationReadiness:
    status: RecommendationReadinessStatus
    existing_prerequisite_course_codes: list[str]
    planned_prerequisite_course_codes: list[str]
    missing_prerequisites: list[str]
    prerequisite_planning_penalty: int
    unlock_value: int

@dataclass(frozen=True)
class CareerSkillContribution:
    mapping: CareerSkillMapping
    relationship: SkillTagRelationship
    score: float

@dataclass(frozen=True)
class CareerMatchScore:
    matched_signals: list[str]
    matched_skill_contributions: list[CareerSkillContribution]
    top_skill_contribution: Optional[CareerSkillContribution]
    career_tag_score: int
    career_skill_score: int
    current_semester_bonus: int

# Keep debug logs readable while still showing enough candidates to diagnose missed slots.
def summarize_codes(codes: list[str], max_items: int = 80) -> str:
    visible_codes = codes[:max_items]
    suffix = "" if len(codes) <= max_items else f", ... +{len(codes) - max_items} more"

    return ", ".join(visible_codes) + suffix

# Builds rule-based recommendations from module catalog data and the student's current profile state.
def recommend_courses(
    db: Session,
    career_goal: str,
    preferred_recommendation_tags: list[str],
    student_faculty: Optional[str],
    completed_course_codes: list[str],
    choice_slot_codes: list[str],
    choice_slots: list[RecommendationChoiceSlot],
    curriculum_courses: list[RecommendationCurriculumCourse],
    excluded_course_codes: list[str],
    excluded_course_titles: list[str],
    limit: int,
) -> RecommendationResponse:
    # Keep unsupported career goals empty instead of pretending we can recommend them.
    if career_goal != "software-engineer":
        return RecommendationResponse(careerGoal=career_goal, recommendations=[])

    completed_codes = {course_code.upper() for course_code in completed_course_codes}
    preferred_tags = normalize_recommendation_tags(preferred_recommendation_tags)
    normalized_student_faculty = normalize_student_faculty(student_faculty)
    excluded_codes = {course_code.upper() for course_code in excluded_course_codes}
    excluded_titles = get_excluded_title_keys(excluded_course_titles)
    candidate_slots = build_recommendation_choice_slots(choice_slot_codes, choice_slots)
    mpe_levels = get_mpe_candidate_levels([slot.courseCode for slot in candidate_slots])
    has_bde_slot = any(slot.courseCode.upper() == "BDE" for slot in candidate_slots)
    active_faculties = list_active_faculty_names(db)
    slot_filters = build_slot_filters(mpe_levels, has_bde_slot)

    if not candidate_slots or not slot_filters:
        return RecommendationResponse(careerGoal=career_goal, recommendations=[])

    # Filter by keywords, tags, and mapped career skills so BDE does not load the entire catalog.
    query = db.query(ModuleModel).filter(
        ModuleModel.faculty.in_(active_faculties),
        or_(*slot_filters),
        or_(*build_relevance_filters(career_goal)),
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
    unlocks_by_module = get_unlocks_by_module(db, [module.code for module in modules])
    prerequisite_modules_by_code = get_prerequisite_modules_by_code(db, prerequisites_by_module)
    recommendations_by_slot: dict[str, list[CourseRecommendation]] = {}

    for module in modules:
        if is_excluded_module(module, completed_codes | excluded_codes, excluded_titles):
            continue

        if is_deprecated_course_code(module):
            continue

        eligible_slots = get_matching_choice_slots(module, candidate_slots)

        if not eligible_slots:
            continue

        # Rank remaining modules by deterministic career signals before softer profile boosts.
        career_match = score_career_match(module, career_goal)

        if career_match.career_tag_score == 0 and career_match.career_skill_score == 0:
            continue

        # Send all prerequisites for arrows, and missing ones for extra planning nodes.
        prerequisites = prerequisites_by_module.get(module.code, [])
        unlock_codes = unlocks_by_module.get(module.code, [])

        for slot in eligible_slots:
            readiness = evaluate_recommendation_readiness(
                prerequisites=prerequisites,
                completed_codes=completed_codes,
                slot=slot,
                choice_slots=candidate_slots,
                curriculum_courses=curriculum_courses,
                prerequisite_modules_by_code=prerequisite_modules_by_code,
                unlock_codes=unlock_codes,
            )

            if readiness is None:
                continue

            prerequisite_recommendations = build_prerequisite_recommendations(
                readiness.planned_prerequisite_course_codes,
                prerequisite_modules_by_code,
                completed_codes | excluded_codes,
                excluded_titles,
            )
            preference_boost = get_preference_boost(module, preferred_tags)
            faculty_boost = get_faculty_boost(module, normalized_student_faculty)
            course_code_adjustment = get_course_code_generation_adjustment(
                module,
                normalized_student_faculty,
            )
            default_profile_adjustment = get_default_profile_adjustment(module, preferred_tags)
            unlock_contribution = min(readiness.unlock_value, 3)
            adjusted_score = max(1, (
                career_match.career_tag_score +
                career_match.career_skill_score +
                career_match.current_semester_bonus +
                unlock_contribution +
                preference_boost +
                faculty_boost +
                course_code_adjustment +
                default_profile_adjustment +
                readiness.prerequisite_planning_penalty
            ))
            score_breakdown = RecommendationScoreBreakdown(
                careerTagScore=career_match.career_tag_score,
                careerSkillScore=career_match.career_skill_score,
                careerSkillEvidence=build_career_skill_evidence(
                    career_goal,
                    career_match.top_skill_contribution,
                ),
                currentSemesterBonus=career_match.current_semester_bonus,
                preferenceBoost=preference_boost,
                sameFacultyBoost=faculty_boost,
                legacyCodePenalty=course_code_adjustment,
                defaultProfileAdjustment=default_profile_adjustment,
                prerequisitePlanningPenalty=readiness.prerequisite_planning_penalty,
                unlockContribution=unlock_contribution,
                finalScore=adjusted_score,
            )
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
                    matchedKeywords=career_match.matched_signals,
                    prerequisites=prerequisites,
                    missingPrerequisites=readiness.missing_prerequisites,
                    existingPrerequisiteCourseCodes=readiness.existing_prerequisite_course_codes,
                    plannedPrerequisiteCourseCodes=readiness.planned_prerequisite_course_codes,
                    prerequisiteRecommendations=prerequisite_recommendations,
                    readinessStatus=readiness.status,
                    unlockValue=readiness.unlock_value,
                    score=adjusted_score,
                    scoreBreakdown=score_breakdown,
                    reason=build_recommendation_reason(
                        module.title,
                        career_match.matched_signals,
                        career_match.top_skill_contribution,
                        readiness.unlock_value,
                        preference_boost,
                        faculty_boost,
                        course_code_adjustment,
                    ),
                )
            )

    sorted_recommendations = assign_ranked_slot_recommendations(
        candidate_slots,
        recommendations_by_slot,
        preferred_tags,
        limit,
    )
    final_recommendations = add_planned_roadmap_artifacts(
        sorted_recommendations,
        candidate_slots,
        curriculum_courses,
    )
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
    normalized_title = title.lower().replace("&", " and ")
    normalized_title = re.sub(r"[^a-z0-9]+", " ", normalized_title)

    return " ".join(normalized_title.split())

def get_title_signature(title: str) -> str:
    # Keep this intentionally conservative so unrelated courses are not merged too aggressively.
    tokens = [
        TITLE_SIGNATURE_TOKEN_REPLACEMENTS.get(token, token)
        for token in normalize_title(title).split()
    ]
    meaningful_tokens = [
        token
        for token in tokens
        if token not in TITLE_SIGNATURE_STOP_WORDS
    ]

    return " ".join(meaningful_tokens)

def get_excluded_title_keys(titles: list[str]) -> set[str]:
    return {
        key
        for title in titles
        for key in (normalize_title(title), get_title_signature(title))
        if key
    }

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

def get_semester_order(year: Optional[int], semester: Optional[int]) -> Optional[int]:
    if year is None or semester is None:
        return None

    return (year - 1) * 2 + semester

def get_semester_from_order(semester_order: int) -> tuple[int, int]:
    year = ((semester_order - 1) // 2) + 1
    semester = ((semester_order - 1) % 2) + 1

    return year, semester

def evaluate_recommendation_readiness(
    prerequisites: list[str],
    completed_codes: set[str],
    slot: RecommendationChoiceSlot,
    choice_slots: list[RecommendationChoiceSlot],
    curriculum_courses: list[RecommendationCurriculumCourse],
    prerequisite_modules_by_code: dict[str, ModuleModel],
    unlock_codes: list[str],
) -> Optional[RecommendationReadiness]:
    prerequisite_codes = [prerequisite.upper() for prerequisite in prerequisites]
    existing_prerequisite_codes = get_existing_prerequisite_course_codes(
        prerequisite_codes,
        slot,
        curriculum_courses,
        prerequisite_modules_by_code,
    )
    unlock_value = get_unlock_value(unlock_codes, slot, curriculum_courses)

    if not prerequisite_codes:
        return RecommendationReadiness(
            status="ready",
            existing_prerequisite_course_codes=[],
            planned_prerequisite_course_codes=[],
            missing_prerequisites=[],
            prerequisite_planning_penalty=0,
            unlock_value=unlock_value,
        )

    # The parsed prerequisite graph is currently flat. If one listed prerequisite is completed
    # or already planned earlier, treat the recommendation as pathway-ready instead of adding
    # every other listed code as a separate requirement.
    if any(prerequisite in completed_codes for prerequisite in prerequisite_codes):
        return RecommendationReadiness(
            status="ready",
            existing_prerequisite_course_codes=existing_prerequisite_codes,
            planned_prerequisite_course_codes=[],
            missing_prerequisites=[],
            prerequisite_planning_penalty=0,
            unlock_value=unlock_value,
        )

    if existing_prerequisite_codes:
        return RecommendationReadiness(
            status="needs-prerequisite-planning",
            existing_prerequisite_course_codes=existing_prerequisite_codes,
            planned_prerequisite_course_codes=[],
            missing_prerequisites=[],
            prerequisite_planning_penalty=0,
            unlock_value=unlock_value,
        )

    planned_prerequisite_codes = get_plannable_prerequisite_course_codes(
        prerequisite_codes,
        slot,
        choice_slots,
        prerequisite_modules_by_code,
    )

    if not planned_prerequisite_codes:
        # In curriculum-only mode, keep strong modules visible when their missing
        # prerequisite is known, but make the extra planning cost affect ranking.
        catalog_known_prerequisite_codes = [
            prerequisite_code
            for prerequisite_code in prerequisite_codes
            if prerequisite_code in prerequisite_modules_by_code
        ]

        if not catalog_known_prerequisite_codes:
            return None

        return RecommendationReadiness(
            status="needs-prerequisite-planning",
            existing_prerequisite_course_codes=[],
            planned_prerequisite_course_codes=catalog_known_prerequisite_codes,
            missing_prerequisites=catalog_known_prerequisite_codes,
            prerequisite_planning_penalty=EXTRA_PREREQUISITE_PLANNING_PENALTY,
            unlock_value=unlock_value,
        )

    planned_prerequisite_codes = sorted(set(planned_prerequisite_codes))

    return RecommendationReadiness(
        status="needs-prerequisite-planning",
        existing_prerequisite_course_codes=[],
        planned_prerequisite_course_codes=planned_prerequisite_codes,
        missing_prerequisites=planned_prerequisite_codes,
        prerequisite_planning_penalty=EXTRA_PREREQUISITE_PLANNING_PENALTY,
        unlock_value=unlock_value,
    )

def get_existing_prerequisite_course_codes(
    prerequisite_codes: list[str],
    slot: RecommendationChoiceSlot,
    curriculum_courses: list[RecommendationCurriculumCourse],
    prerequisite_modules_by_code: dict[str, ModuleModel],
) -> list[str]:
    target_order = get_semester_order(slot.year, slot.semester)

    if target_order is None:
        return []

    existing_codes = []

    for course in curriculum_courses:
        course_order = get_semester_order(course.year, course.semester)
        course_code = course.courseCode.upper()
        course_title = course.title or ""

        if (
            not course.isChoiceSlot and
            course_order is not None and
            course_order < target_order and
            (
                course_code in prerequisite_codes or
                has_equivalent_prerequisite_title(
                    course_title,
                    prerequisite_codes,
                    prerequisite_modules_by_code,
                )
            )
        ):
            existing_codes.append(course_code)

    return sorted(set(existing_codes))

def get_existing_prerequisite_node_ids(
    recommendation: CourseRecommendation,
    curriculum_courses: list[RecommendationCurriculumCourse],
) -> list[str]:
    target_order = get_semester_order(
        recommendation.matchedChoiceSlotYear,
        recommendation.matchedChoiceSlotSemester,
    )

    if target_order is None:
        return []

    existing_codes = {
        course_code.upper()
        for course_code in recommendation.existingPrerequisiteCourseCodes
    }
    node_ids = [
        course.nodeId
        for course in curriculum_courses
        if (
            course.nodeId and
            not course.isChoiceSlot and
            course.courseCode.upper() in existing_codes and
            get_semester_order(course.year, course.semester) is not None and
            get_semester_order(course.year, course.semester) < target_order
        )
    ]

    return sorted(set(node_ids))

def add_planned_roadmap_artifacts(
    recommendations: list[CourseRecommendation],
    choice_slots: list[RecommendationChoiceSlot],
    curriculum_courses: list[RecommendationCurriculumCourse],
) -> list[CourseRecommendation]:
    remaining_semester_orders = sorted({
        semester_order
        for slot in choice_slots
        for semester_order in [get_semester_order(slot.year, slot.semester)]
        if semester_order is not None
    })

    return [
        recommendation.model_copy(
            update={
                "plannedRoadmapNodes": build_planned_roadmap_nodes(
                    recommendation,
                    remaining_semester_orders,
                ),
                "plannedRoadmapEdges": build_planned_roadmap_edges(
                    recommendation,
                    curriculum_courses,
                ),
            }
        )
        for recommendation in recommendations
    ]

def build_planned_roadmap_nodes(
    recommendation: CourseRecommendation,
    remaining_semester_orders: list[int],
) -> list[RecommendationPlannedRoadmapNode]:
    target_order = get_semester_order(
        recommendation.matchedChoiceSlotYear,
        recommendation.matchedChoiceSlotSemester,
    )

    if target_order is None:
        return []

    prerequisite_semester_order = next(
        (
            semester_order
            for semester_order in reversed(remaining_semester_orders)
            if semester_order < target_order
        ),
        None,
    )

    if prerequisite_semester_order is None:
        return []

    prerequisite_year, prerequisite_semester = get_semester_from_order(
        prerequisite_semester_order,
    )
    prerequisites_by_code = {
        prerequisite.courseCode: prerequisite
        for prerequisite in recommendation.prerequisiteRecommendations
    }

    return [
        RecommendationPlannedRoadmapNode(
            id=get_recommended_prerequisite_node_id(recommendation, prerequisite_code),
            courseCode=prerequisite_code,
            title=prerequisites_by_code[prerequisite_code].title,
            type="Recommended Pre-Requisite",
            year=prerequisite_year,
            semester=prerequisite_semester,
            academicUnits=prerequisites_by_code[prerequisite_code].academicUnits or 0,
            prerequisiteText=f"Recommended prerequisite for {recommendation.courseCode}",
            recommendedForCourseCode=recommendation.courseCode,
        )
        for prerequisite_code in recommendation.plannedPrerequisiteCourseCodes
        if prerequisite_code in prerequisites_by_code
    ]

def build_planned_roadmap_edges(
    recommendation: CourseRecommendation,
    curriculum_courses: list[RecommendationCurriculumCourse],
) -> list[RecommendationPlannedRoadmapEdge]:
    if not recommendation.matchedChoiceSlotId:
        return []

    edge_keys = set()
    edges = []
    prerequisite_node_ids = [
        *get_existing_prerequisite_node_ids(recommendation, curriculum_courses),
        *[
            get_recommended_prerequisite_node_id(recommendation, prerequisite_code)
            for prerequisite_code in recommendation.plannedPrerequisiteCourseCodes
        ],
    ]

    for node_id in prerequisite_node_ids:
        edge_key = f"{node_id}->{recommendation.matchedChoiceSlotId}"

        if edge_key not in edge_keys:
            edges.append(
                RecommendationPlannedRoadmapEdge(
                    source=node_id,
                    target=recommendation.matchedChoiceSlotId,
                )
            )
            edge_keys.add(edge_key)

    return edges

def get_recommended_prerequisite_node_id(
    recommendation: CourseRecommendation,
    prerequisite_course_code: str,
) -> str:
    return (
        "recommended-prerequisite-"
        f"{recommendation.matchedChoiceSlotId}-"
        f"{prerequisite_course_code.lower()}"
    )

# Older CZ prerequisites can correspond to newer SC curriculum rows with the same title.
def has_equivalent_prerequisite_title(
    course_title: str,
    prerequisite_codes: list[str],
    prerequisite_modules_by_code: dict[str, ModuleModel],
) -> bool:
    course_title_keys = {normalize_title(course_title), get_title_signature(course_title)}

    return any(
        bool(course_title_keys.intersection({
            normalize_title(prerequisite_module.title),
            get_title_signature(prerequisite_module.title),
        }))
        for prerequisite_code in prerequisite_codes
        for prerequisite_module in [prerequisite_modules_by_code.get(prerequisite_code)]
        if prerequisite_module is not None
    )

def get_plannable_prerequisite_course_codes(
    prerequisite_codes: list[str],
    slot: RecommendationChoiceSlot,
    choice_slots: list[RecommendationChoiceSlot],
    prerequisite_modules_by_code: dict[str, ModuleModel],
) -> list[str]:
    target_order = get_semester_order(slot.year, slot.semester)

    if target_order is None:
        return []

    earlier_slots = [
        choice_slot
        for choice_slot in choice_slots
        if (
            get_semester_order(choice_slot.year, choice_slot.semester) is not None and
            get_semester_order(choice_slot.year, choice_slot.semester) < target_order
        )
    ]

    if not earlier_slots:
        return []

    plannable_codes = []

    for prerequisite_code in prerequisite_codes:
        prerequisite_module = prerequisite_modules_by_code.get(prerequisite_code)

        if prerequisite_module and any(
            can_module_fit_choice_slot(prerequisite_module, earlier_slot)
            for earlier_slot in earlier_slots
        ):
            plannable_codes.append(prerequisite_code)

    return sorted(set(plannable_codes))

def get_unlock_value(
    unlock_codes: list[str],
    slot: RecommendationChoiceSlot,
    curriculum_courses: list[RecommendationCurriculumCourse],
) -> int:
    target_order = get_semester_order(slot.year, slot.semester)
    unlock_code_set = {unlock_code.upper() for unlock_code in unlock_codes}

    if target_order is None or not unlock_code_set:
        return 0

    return len({
        course.courseCode.upper()
        for course in curriculum_courses
        if (
            course.courseCode.upper() in unlock_code_set and
            not course.isChoiceSlot and
            get_semester_order(course.year, course.semester) is not None and
            get_semester_order(course.year, course.semester) > target_order
        )
    })

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
    return (
        module.code in excluded_codes or
        normalize_title(module.title) in excluded_titles or
        get_title_signature(module.title) in excluded_titles
    )

def add_used_title_keys(used_course_titles: set[str], title: str) -> None:
    used_course_titles.add(normalize_title(title))
    title_signature = get_title_signature(title)

    if title_signature:
        used_course_titles.add(title_signature)

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

def build_relevance_filters(career_goal: str) -> list:
    filters = []

    for keyword in SOFTWARE_ENGINEER_KEYWORDS:
        pattern = f"%{keyword}%"
        filters.append(ModuleModel.title.ilike(pattern))
        filters.append(ModuleModel.description.ilike(pattern))

    for tag in SOFTWARE_ENGINEER_TAG_WEIGHTS:
        filters.append(ModuleModel.recommendation_tags.cast(String).ilike(f"%{tag}%"))

    for mapping in CAREER_SKILL_MAPPINGS.get(career_goal, ()):
        for relationship in mapping.tag_relationships:
            filters.append(
                ModuleModel.recommendation_tags.cast(String).ilike(f"%{relationship.tag}%")
            )

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
        if can_module_fit_choice_slot(module, slot):
            matching_slots.append(slot)

    return matching_slots

def can_module_fit_choice_slot(module: ModuleModel, slot: RecommendationChoiceSlot) -> bool:
    slot_code = normalize_choice_slot_code(slot.courseCode)
    mpe_level = get_mpe_slot_level(slot_code)

    # MPE slots must stay within CSC and match the placeholder level.
    if mpe_level:
        return module.faculty == "CSC" and module.level == mpe_level

    # BDE is broader, but each BDE slot should still fit its roadmap year level.
    return slot_code == "BDE" and can_fit_bde_slot(module, slot)

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

def assign_ranked_slot_recommendations(
    choice_slots: list[RecommendationChoiceSlot],
    recommendations_by_slot: dict[str, list[CourseRecommendation]],
    preferred_tags: set[str],
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
    used_recommendation_tags: dict[str, int] = {}

    for slot in choice_slots:
        if len(ranked_recommendations) >= limit:
            break

        slot_recommendations = sorted_recommendations_by_slot[get_choice_slot_identity(slot)]
        unique_recommendation = get_unique_recommendation_at_or_after_index(
            slot_recommendations,
            0,
            used_course_codes,
            used_course_titles,
            used_recommendation_tags,
            preferred_tags,
        )

        if not unique_recommendation:
            continue

        ranked_recommendations.append(unique_recommendation)
        used_course_codes.add(unique_recommendation.courseCode)
        add_used_title_keys(used_course_titles, unique_recommendation.title)
        add_used_recommendation_tags(used_recommendation_tags, unique_recommendation)

    return ranked_recommendations

def get_unique_recommendation_at_or_after_index(
    recommendations: list[CourseRecommendation],
    start_index: int,
    used_course_codes: set[str],
    used_course_titles: set[str],
    used_recommendation_tags: dict[str, int],
    preferred_tags: set[str],
) -> Optional[CourseRecommendation]:
    eligible_recommendations = []

    for recommendation in recommendations[start_index:]:
        recommendation_title = normalize_title(recommendation.title)
        recommendation_title_signature = get_title_signature(recommendation.title)

        if (
            recommendation.courseCode not in used_course_codes and
            recommendation_title not in used_course_titles and
            recommendation_title_signature not in used_course_titles
        ):
            eligible_recommendations.append(recommendation)

    if not eligible_recommendations:
        return None

    return max(
        eligible_recommendations,
        key=lambda recommendation: (
            get_diversity_adjusted_score(
                recommendation,
                used_recommendation_tags,
                preferred_tags,
            ),
            recommendation.score,
            _reverse_code_sort_key(recommendation.courseCode),
        ),
    )

def get_diversity_adjusted_score(
    recommendation: CourseRecommendation,
    used_recommendation_tags: dict[str, int],
    preferred_tags: set[str],
) -> int:
    penalty = 0

    for tag in get_recommendation_tags(recommendation):
        repeat_count = used_recommendation_tags.get(tag, 0)
        repeat_penalty = (
            PREFERRED_DIVERSITY_TAG_REPEAT_PENALTY
            if tag in preferred_tags
            else DIVERSITY_TAG_REPEAT_PENALTY
        )
        penalty += repeat_count * repeat_penalty

    return recommendation.score - penalty

def get_recommendation_tags(recommendation: CourseRecommendation) -> list[str]:
    return [
        signal.removeprefix("tag:")
        for signal in recommendation.matchedKeywords
        if signal.startswith("tag:")
    ]

def add_used_recommendation_tags(
    used_recommendation_tags: dict[str, int],
    recommendation: CourseRecommendation,
) -> None:
    for tag in get_recommendation_tags(recommendation):
        used_recommendation_tags[tag] = used_recommendation_tags.get(tag, 0) + 1

def _reverse_code_sort_key(course_code: str) -> tuple[int, ...]:
    return tuple(-ord(character) for character in course_code)

def score_career_match(module: ModuleModel, career_goal: str) -> CareerMatchScore:
    if career_goal != "software-engineer":
        return CareerMatchScore(
            matched_signals=[],
            matched_skill_contributions=[],
            top_skill_contribution=None,
            career_tag_score=0,
            career_skill_score=0,
            current_semester_bonus=0,
        )

    searchable_text = f"{module.title} {module.description or ''}".lower()
    matched_keywords = [
        keyword for keyword in SOFTWARE_ENGINEER_KEYWORDS if keyword in searchable_text
    ]
    matched_tags = [
        tag
        for tag in (module.recommendation_tags or [])
        if tag in SOFTWARE_ENGINEER_TAG_WEIGHTS
    ]
    matched_skill_contributions = get_career_skill_contributions(module, career_goal)
    top_skill_contribution = get_top_skill_contribution(matched_skill_contributions)
    matched_signals = (
        matched_keywords +
        [f"tag:{tag}" for tag in matched_tags] +
        [
            f"skill:{contribution.mapping.skill}:{contribution.relationship.tag}"
            for contribution in matched_skill_contributions
        ]
    )
    # Keep raw keyword/tag relevance separate from mapped career-skill relevance so the
    # score breakdown can show whether the module matched by text, tags, or skill area.
    career_tag_score = (
        sum(SOFTWARE_ENGINEER_KEYWORDS[keyword] for keyword in matched_keywords) +
        sum(SOFTWARE_ENGINEER_TAG_WEIGHTS[tag] for tag in matched_tags)
    )
    career_skill_score = round_positive_score(
        sum(contribution.score for contribution in matched_skill_contributions)
    )
    current_semester_bonus = 0

    # Prefer modules currently available in the catalog by giving them a small boost.
    if module.is_current_semester:
        current_semester_bonus = 1

    return CareerMatchScore(
        matched_signals=matched_signals,
        matched_skill_contributions=matched_skill_contributions,
        top_skill_contribution=top_skill_contribution,
        career_tag_score=career_tag_score,
        career_skill_score=career_skill_score,
        current_semester_bonus=current_semester_bonus,
    )

def get_career_skill_contributions(
    module: ModuleModel,
    career_goal: str,
) -> list[CareerSkillContribution]:
    module_tags = set(module.recommendation_tags or [])
    contributions: list[CareerSkillContribution] = []

    for mapping in CAREER_SKILL_MAPPINGS.get(career_goal, ()):
        matching_contributions = [
            CareerSkillContribution(
                mapping=mapping,
                relationship=relationship,
                score=mapping.weight * relationship.relationship_weight * relationship.tag_confidence,
            )
            for relationship in mapping.tag_relationships
            if relationship.tag in module_tags
        ]

        top_contribution = get_top_skill_contribution(matching_contributions)

        if top_contribution:
            contributions.append(top_contribution)

    return contributions

def get_top_skill_contribution(
    contributions: list[CareerSkillContribution],
) -> Optional[CareerSkillContribution]:
    if not contributions:
        return None

    return max(
        contributions,
        key=lambda contribution: (
            contribution.score,
            contribution.relationship.relationship_weight,
            contribution.relationship.tag_confidence,
            contribution.relationship.tag,
        ),
    )

def round_positive_score(score: float) -> int:
    return int(score + 0.5)

def build_career_skill_evidence(
    career_goal: str,
    top_skill_contribution: Optional[CareerSkillContribution],
) -> Optional[RecommendationCareerSkillEvidence]:
    if not top_skill_contribution:
        return None

    mapping = top_skill_contribution.mapping
    relationship = top_skill_contribution.relationship

    return RecommendationCareerSkillEvidence(
        careerGoal=career_goal,
        skillArea=mapping.skill,
        skillAreaWeight=mapping.weight,
        tag=relationship.tag,
        relationshipWeight=relationship.relationship_weight,
        tagConfidence=relationship.tag_confidence,
        contributionScore=top_skill_contribution.score,
        rationale=relationship.rationale,
    )

def normalize_recommendation_tags(tags: list[str]) -> set[str]:
    return {
        tag.strip().lower()
        for tag in tags
        if tag.strip()
    }

def normalize_student_faculty(student_faculty: Optional[str]) -> Optional[str]:
    if not student_faculty:
        return None

    normalized_faculty = student_faculty.strip().upper()

    return normalized_faculty or None

def get_preference_boost(module: ModuleModel, preferred_tags: set[str]) -> int:
    if not preferred_tags:
        return 0

    matching_tags = preferred_tags.intersection(module.recommendation_tags or [])
    return min(len(matching_tags) * PREFERENCE_TAG_BOOST, PREFERENCE_TAG_BOOST * 2)

def get_faculty_boost(module: ModuleModel, student_faculty: Optional[str]) -> int:
    if not student_faculty:
        return 0

    return SAME_FACULTY_BOOST if module.faculty == student_faculty else 0

def get_course_code_generation_adjustment(
    module: ModuleModel,
    student_faculty: Optional[str],
) -> int:
    return 0

def get_default_profile_adjustment(module: ModuleModel, preferred_tags: set[str]) -> int:
    if preferred_tags and preferred_tags != {"software-engineering"}:
        return 0

    if module.recommendation_profile == "broad-default":
        return BROAD_DEFAULT_PROFILE_BOOST

    if module.recommendation_profile == "specialist":
        return SPECIALIST_PROFILE_PENALTY

    return 0

def is_deprecated_course_code(module: ModuleModel) -> bool:
    module_code = module.code.upper()

    return module_code.startswith(DEPRECATED_COURSE_CODE_PREFIXES)

def build_recommendation_reason(
    course_title: str,
    matched_signals: list[str],
    top_skill_contribution: Optional[CareerSkillContribution],
    unlock_value: int,
    preference_boost: int,
    faculty_boost: int,
    course_code_adjustment: int,
) -> str:
    fallback_signals = [
        signal
        for signal in matched_signals
        if not signal.startswith("skill:")
    ][:3]
    base_reason = "Recommended for the Software Engineer career goal."
    extra_reasons = []

    if top_skill_contribution:
        extra_reasons.append(build_career_skill_reason(top_skill_contribution, course_title))
    elif fallback_signals:
        extra_reasons.append(f"matches career signals: {', '.join(fallback_signals)}")

    if preference_boost > 0:
        extra_reasons.append("matches selected topic preference(s)")

    if faculty_boost > 0:
        extra_reasons.append("matches your profile faculty")

    if course_code_adjustment < 0:
        extra_reasons.append("uses a lower-priority course code, so it is kept as a fallback")

    if unlock_value > 0:
        extra_reasons.append(f"unlocks {unlock_value} later curriculum module(s)")

    if not extra_reasons:
        return base_reason

    return f"{base_reason} Also {' and '.join(extra_reasons)}."

def build_career_skill_reason(
    top_skill_contribution: CareerSkillContribution,
    course_title: str,
) -> str:
    mapping = top_skill_contribution.mapping
    relationship = top_skill_contribution.relationship

    return (
        "top career-skill path: "
        f"Software Engineer -> {mapping.skill} -> {relationship.tag} -> "
        f"{course_title}"
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
