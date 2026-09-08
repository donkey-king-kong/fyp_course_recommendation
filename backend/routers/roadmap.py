import logging

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from backend.database.connection import SessionLocal
from backend.schemas.roadmap import PersonalizedRoadmapRequest, RoadmapResponse
from backend.services.personalized_roadmap_service import build_personalized_roadmap
from backend.services.roadmap_service import get_csc_roadmap

router = APIRouter()
logger = logging.getLogger(__name__)
ROADMAP_DATABASE_UNAVAILABLE_DETAIL = (
    "Roadmap module data is unavailable. Check that PostgreSQL is running and the database has been seeded."
)

ROADMAP_DATABASE_ERROR_RESPONSE = {
    "description": "PostgreSQL is unavailable or module metadata cannot be queried.",
    "content": {
        "application/json": {
            "example": {"detail": ROADMAP_DATABASE_UNAVAILABLE_DETAIL}
        }
    },
}

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
        "or unlock arrows into the roadmap shape used by the frontend. Curriculum "
        "guide edges are normalized into `RoadmapEdge` objects before response "
        "validation so the frontend receives one consistent roadmap edge shape."
    ),
    response_description="Ready-to-render roadmap nodes and prerequisite edges.",
    responses={503: ROADMAP_DATABASE_ERROR_RESPONSE},
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
        logger.exception("Roadmap database operation failed.")
        raise HTTPException(
            status_code=503,
            detail=ROADMAP_DATABASE_UNAVAILABLE_DETAIL,
        ) from error
