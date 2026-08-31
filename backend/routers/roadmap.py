from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from backend.database.connection import SessionLocal
from backend.schemas.roadmap import PersonalizedRoadmapRequest, RoadmapResponse
from backend.services.personalized_roadmap_service import build_personalized_roadmap
from backend.services.roadmap_service import get_csc_roadmap

router = APIRouter()

def get_db() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/roadmap", response_model=RoadmapResponse)
def read_roadmap() -> RoadmapResponse:
    return get_csc_roadmap()

@router.post(
    "/roadmap/personalized",
    response_model=RoadmapResponse,
    summary="Build a personalized roadmap",
    description=(
        "Combines an uploaded curriculum guide with parsed transcript modules, "
        "transcript placement overrides, transcript-only modules, and prerequisite "
        "or unlock arrows into the roadmap shape used by the frontend."
    ),
    response_description="Ready-to-render roadmap nodes and prerequisite edges.",
)
def create_personalized_roadmap(
    request: PersonalizedRoadmapRequest,
    db: Session = Depends(get_db),
) -> RoadmapResponse:
    try:
        return build_personalized_roadmap(
            db=db,
            curriculum_guide=request.curriculumGuide,
            transcript_completed_courses=request.transcriptCompletedCourses,
            transcript_unmatched_course_codes=request.transcriptUnmatchedCourseCodes,
        )
    except SQLAlchemyError as error:
        raise HTTPException(
            status_code=503,
            detail="Roadmap module data is currently unavailable.",
        ) from error
