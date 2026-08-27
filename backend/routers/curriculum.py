from fastapi import APIRouter, File, HTTPException, UploadFile

from backend.schemas.curriculum import CurriculumGuideResponse
from backend.services.curriculum_service import extract_curriculum_guide

router = APIRouter()

# This endpoint only handles HTTP upload concerns.
# PDF parsing and roadmap shaping stay in the service layer.
@router.post(
    "/curriculum-guide",
    response_model=CurriculumGuideResponse,
    summary="Parse a curriculum guide PDF",
    response_description="Structured curriculum guide data grouped by year and semester.",
    responses={
        400: {"description": "The uploaded file is missing, empty, or not a PDF."},
        422: {"description": "The PDF could not be parsed into curriculum rows."},
    },
)
async def upload_curriculum_guide(
    file: UploadFile = File(
        ...,
        description="Official curriculum guide PDF to convert into roadmap-shaped data.",
    ),
) -> CurriculumGuideResponse:
    # Keep the first parser PDF-only so the service can rely on PyMuPDF extraction.
    if file.content_type != "application/pdf":
        raise HTTPException(status_code=400, detail="Only PDF curriculum guides are supported.")

    file_content = await file.read()

    # Empty uploads should fail before reaching the parser service.
    if not file_content:
        raise HTTPException(status_code=400, detail="Uploaded curriculum guide is empty.")

    try:
        # Convert the uploaded guide into data the frontend can later render as a roadmap.
        return extract_curriculum_guide(file_content)
    except ValueError as error:
        raise HTTPException(status_code=422, detail=str(error)) from error
