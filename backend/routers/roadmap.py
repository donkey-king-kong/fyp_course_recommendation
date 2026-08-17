from fastapi import APIRouter

from backend.schemas.roadmap import RoadmapResponse
from backend.services.roadmap_service import get_csc_roadmap

router = APIRouter()

@router.get("/roadmap", response_model=RoadmapResponse)
def read_roadmap() -> RoadmapResponse:
    return get_csc_roadmap()
