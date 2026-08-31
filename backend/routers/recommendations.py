from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from backend.database.connection import SessionLocal
from backend.schemas.recommendation import RecommendationRequest, RecommendationResponse
from backend.services.recommendation_service import recommend_courses

router = APIRouter(tags=["Recommendations"])

RECOMMENDATION_DATABASE_ERROR_RESPONSE = {
    "description": "PostgreSQL is unavailable or the module tables cannot be queried.",
    "content": {
        "application/json": {
            "example": {"detail": "Recommendation data is currently unavailable."}
        }
    },
}

def get_db() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post(
    "/recommendations",
    response_model=RecommendationResponse,
    summary="Assign recommended modules to open choice slots",
    description=(
        "Returns backend-ranked and backend-assigned module recommendations for exact "
        "open BDE/MPE choice slots. Each returned recommendation includes "
        "`matchedChoiceSlotId`, so the frontend should render it in that slot instead "
        "of re-ranking or allocating candidates. Diversity is a gentle tiebreaker and "
        "does not override eligibility, career relevance, or student topic preferences."
    ),
    response_description="Assigned module recommendations with slot IDs, planning artifacts, and reasons.",
    responses={503: RECOMMENDATION_DATABASE_ERROR_RESPONSE},
)
def create_recommendations(
    request: RecommendationRequest,
    db: Session = Depends(get_db),
) -> RecommendationResponse:
    try:
        return recommend_courses(
            db=db,
            career_goal=request.careerGoal,
            preferred_recommendation_tags=request.preferredRecommendationTags,
            student_faculty=request.studentFaculty,
            completed_course_codes=request.completedCourseCodes,
            choice_slot_codes=request.choiceSlotCodes,
            choice_slots=request.choiceSlots,
            curriculum_courses=request.curriculumCourses,
            excluded_course_codes=request.excludedCourseCodes,
            excluded_course_titles=request.excludedCourseTitles,
            limit=request.limit,
        )
    except SQLAlchemyError as error:
        raise HTTPException(
            status_code=503,
            detail="Recommendation data is currently unavailable.",
        ) from error
