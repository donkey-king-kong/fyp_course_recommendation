from fastapi import APIRouter

from backend.schemas.student_skills import StudentSkillsRequest, StudentSkillsResponse
from backend.services.student_skills_service import build_student_skills_picture

router = APIRouter(tags=["Student skills"])

@router.post(
    "/student-skills/preview",
    response_model=StudentSkillsResponse,
    summary="Preview likely prior learning for a pilot career",
    description=(
        "Matches submitted completed and candidate course codes to a small, source-linked "
        "course-content ledger for Software Engineer or Data Engineer. Introductory and "
        "advanced exposure describe course content, not verified student mastery. "
        "Unmapped courses remain unknown. This preview does not rank, check eligibility, "
        "or change recommendations."
    ),
    response_description="Shared skill areas with course excerpts and explicit unknown coverage.",
    responses={422: {"description": "Unsupported career goal or invalid request shape."}},
)
def preview_student_skills(request: StudentSkillsRequest) -> StudentSkillsResponse:
    return build_student_skills_picture(request)
