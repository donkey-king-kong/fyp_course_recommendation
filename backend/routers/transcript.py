from fastapi import APIRouter, File, HTTPException, UploadFile

from backend.schemas.transcript import TranscriptUploadResponse
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
