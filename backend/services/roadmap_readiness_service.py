import re
from typing import Optional

from backend.schemas.roadmap_readiness import (
    RoadmapCourseReadiness,
    RoadmapReadinessCourse,
    RoadmapReadinessResponse,
    RoadmapReadinessStatus,
    RoadmapStandingRequirement,
)

COURSE_CODE_PATTERN = re.compile(r"[A-Z]{2,4}\d{4}[A-Z]?", re.IGNORECASE)

def evaluate_roadmap_readiness(
    courses: list[RoadmapReadinessCourse],
    completed_course_ids: list[str],
    completed_academic_units: float,
    standing_requirements: list[RoadmapStandingRequirement],
) -> RoadmapReadinessResponse:
    completed_ids = set(completed_course_ids)
    readiness = [
        evaluate_course_readiness(
            course,
            completed_ids,
            completed_academic_units,
            standing_requirements,
        )
        for course in courses
    ]

    return RoadmapReadinessResponse(courses=readiness)

def evaluate_course_readiness(
    course: RoadmapReadinessCourse,
    completed_course_ids: set[str],
    completed_academic_units: float,
    standing_requirements: list[RoadmapStandingRequirement],
) -> RoadmapCourseReadiness:
    if course.id in completed_course_ids:
        return build_course_readiness(course.id, "completed", [])

    missing_prerequisites = [
        prerequisite_id
        for prerequisite_id in course.prerequisites
        if prerequisite_id not in completed_course_ids
    ]
    missing_standing_requirement = get_missing_standing_requirement(
        course,
        completed_academic_units,
        standing_requirements,
    )
    missing_requirements = [
        *dict.fromkeys(missing_prerequisites),
        *([missing_standing_requirement] if missing_standing_requirement else []),
    ]

    if not missing_requirements:
        return build_course_readiness(course.id, "available", [])

    return build_course_readiness(course.id, "locked", missing_requirements)

def build_course_readiness(
    course_id: str,
    status: RoadmapReadinessStatus,
    missing_requirements: list[str],
) -> RoadmapCourseReadiness:
    return RoadmapCourseReadiness(
        courseId=course_id,
        status=status,
        missingRequirements=missing_requirements,
    )

def get_missing_standing_requirement(
    course: RoadmapReadinessCourse,
    completed_academic_units: float,
    standing_requirements: list[RoadmapStandingRequirement],
) -> Optional[str]:
    if should_ignore_prerequisite_text(course):
        return None

    standing_year = get_standing_year(course.prerequisiteText)

    if not standing_year:
        if has_course_code_prerequisite(course.prerequisiteText):
            return None

        return course.prerequisiteText or "Prerequisite required"

    standing_requirement = next(
        (
            requirement
            for requirement in standing_requirements
            if requirement.standingYear == standing_year
        ),
        None,
    )

    if not standing_requirement:
        return course.prerequisiteText or f"Year {standing_year} standing"

    if completed_academic_units >= standing_requirement.minimumAcademicUnits:
        return None

    return (
        f"Year {standing_year} standing requires "
        f"{standing_requirement.minimumAcademicUnits} AU; "
        f"you have {completed_academic_units:g} AU"
    )

def should_ignore_prerequisite_text(course: RoadmapReadinessCourse) -> bool:
    prerequisite_text = (course.prerequisiteText or "").strip().lower()

    return (
        not prerequisite_text or
        prerequisite_text == "nil" or
        course.courseCode == "BDE" or
        course.type == "BDE" or
        "refer to class schedule" in prerequisite_text
    )

def get_standing_year(prerequisite_text: Optional[str]) -> Optional[int]:
    standing_match = re.search(r"\byear\s+([2-4])\s+standing\b", prerequisite_text or "", re.IGNORECASE)

    return int(standing_match.group(1)) if standing_match else None

def has_course_code_prerequisite(prerequisite_text: Optional[str]) -> bool:
    return bool(COURSE_CODE_PATTERN.search(prerequisite_text or ""))
