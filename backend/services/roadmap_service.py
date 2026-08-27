import json
from pathlib import Path

from backend.schemas.roadmap import RoadmapResponse

ROADMAP_DATA_PATH = Path(__file__).resolve().parents[2] / "data" / "test_csc_roadmap.json"

def get_csc_roadmap() -> RoadmapResponse:
    with ROADMAP_DATA_PATH.open() as roadmap_file:
        roadmap_data = json.load(roadmap_file)

    return RoadmapResponse.model_validate(roadmap_data)
