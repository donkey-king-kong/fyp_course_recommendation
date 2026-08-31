from fastapi import APIRouter, File, HTTPException, UploadFile

from backend.schemas.transcript import (
    TranscriptCurriculumMatchRequest,
    TranscriptCurriculumMatchResponse,
    TranscriptUploadResponse,
)
from backend.services.transcript_matching_service import match_transcript_to_curriculum
from backend.services.transcript_service import extract_completed_courses

router = APIRouter()

# Accept one PDF transcript
# Return completed roadmap courses found inside it
@router.post("/transcript", response_model=TranscriptUploadResponse)
async def upload_transcript(file: UploadFile = File(...)) -> TranscriptUploadResponse:
    # Validation that the uploaded file is a PDF
    if file.content_type != "application/pdf":
        raise HTTPException(status_code=400, detail="Only PDF transcripts are supported.")

    # Read the uploaded file bytes before passing to parser service
    file_content = await file.read()

    if not file_content:
        raise HTTPException(status_code=400, detail="Uploaded transcript is empty.")

    # Handoff to parser
    # Separate routing and parsing logic
    return extract_completed_courses(file_content)

@router.post(
    "/transcript/match-curriculum",
    response_model=TranscriptCurriculumMatchResponse,
    summary="Match parsed transcript courses to curriculum rows",
    description=(
        "Matches completed transcript modules to uploaded curriculum rows by exact "
        "course code first, then conservative title matching for course-code changes."
    ),
    response_description="Matched roadmap course IDs and unmatched transcript module codes.",
)
def create_transcript_curriculum_match(
    request: TranscriptCurriculumMatchRequest,
) -> TranscriptCurriculumMatchResponse:
    return match_transcript_to_curriculum(
        completed_course_codes=request.completedCourseCodes,
        transcript_completed_courses=request.transcriptCompletedCourses,
        curriculum_courses=request.curriculumCourses,
    )
