from __future__ import annotations
from typing import Optional
from pydantic import BaseModel

# One module card/detail returned by the modules API.
class ModuleSummary(BaseModel):
    code: str
    title: str
    au: Optional[float]
    faculty: Optional[str]
    description: Optional[str]
    level: Optional[int]
    categories: list[str]
    recommendation_tags: list[str]
    latest_year: Optional[str]
    latest_semester: Optional[str]
    is_current_semester: bool
    not_available_to_programme: Optional[str]
    prerequisites: list[str]
    unlocks: list[str]
    prerequisite_count: int
    unlock_count: int

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "code": "CC0002",
                    "title": "Navigating The Digital World",
                    "au": 2.0,
                    "faculty": "CSC",
                    "description": None,
                    "level": 0,
                    "categories": ["CORE"],
                    "recommendation_tags": [],
                    "latest_year": "2026",
                    "latest_semester": "1",
                    "is_current_semester": True,
                    "not_available_to_programme": None,
                    "prerequisites": [],
                    "unlocks": [],
                    "prerequisite_count": 0,
                    "unlock_count": 0,
                }
            ]
        }
    }

# Paginated list response so the frontend does not fetch all modules at once.
class ModuleListResponse(BaseModel):
    items: list[ModuleSummary]
    total: int
    limit: int
    offset: int

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "items": [
                        {
                            "code": "CC0002",
                            "title": "Navigating The Digital World",
                            "au": 2.0,
                            "faculty": "CSC",
                            "description": None,
                            "level": 0,
                            "categories": ["CORE"],
                            "recommendation_tags": [],
                            "latest_year": "2026",
                            "latest_semester": "1",
                            "is_current_semester": True,
                            "not_available_to_programme": None,
                            "prerequisites": [],
                            "unlocks": [],
                            "prerequisite_count": 0,
                            "unlock_count": 0,
                        }
                    ],
                    "total": 1,
                    "limit": 5,
                    "offset": 0,
                }
            ]
        }
    }

# Valid database-backed filter values for frontend dropdowns.
class ModuleFilterOptionsResponse(BaseModel):
    faculties: list[str]
    levels: list[int]
    categories: list[str]

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "faculties": ["CE", "CSC"],
                    "levels": [0, 1, 2, 3, 4],
                    "categories": ["CORE", "GERP", "GLOAD", "MLOAD"],
                }
            ]
        }
    }
