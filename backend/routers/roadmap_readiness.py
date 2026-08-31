from fastapi import APIRouter

from backend.schemas.roadmap_readiness import (
    RoadmapReadinessRequest,
    RoadmapReadinessResponse,
)
from backend.services.roadmap_readiness_service import evaluate_roadmap_readiness

router = APIRouter(tags=["Roadmap"])

@router.post(
    "/roadmap/readiness",
    response_model=RoadmapReadinessResponse,
    summary="Evaluate roadmap course readiness",
    description=(
        "Evaluates displayed roadmap courses against completed roadmap IDs, "
        "completed AU, parsed prerequisite text, and curriculum standing rules."
    ),
    response_description="Readiness status and missing requirements for each roadmap course.",
)
def create_roadmap_readiness(
    request: RoadmapReadinessRequest,
) -> RoadmapReadinessResponse:
    return evaluate_roadmap_readiness(
        courses=request.courses,
        completed_course_ids=request.completedCourseIds,
        completed_academic_units=request.completedAcademicUnits,
        standing_requirements=request.standingRequirements,
    )
