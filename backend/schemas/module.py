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
                    "code": "BE2601",
                    "title": "Management Principles, Skills & Competencies",
                    "au": 4.0,
                    "faculty": "BUS",
                    "description": None,
                    "level": 2,
                    "categories": ["CORE", "GLOAD"],
                    "latest_year": "2026",
                    "latest_semester": "1",
                    "is_current_semester": True,
                    "not_available_to_programme": "BCE, BCG",
                    "prerequisites": ["AB1601"],
                    "unlocks": [],
                    "prerequisite_count": 1,
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
                            "code": "BE2601",
                            "title": "Management Principles, Skills & Competencies",
                            "au": 4.0,
                            "faculty": "BUS",
                            "description": None,
                            "level": 2,
                            "categories": ["CORE", "GLOAD"],
                            "latest_year": "2026",
                            "latest_semester": "1",
                            "is_current_semester": True,
                            "not_available_to_programme": "BCE, BCG",
                            "prerequisites": ["AB1601"],
                            "unlocks": [],
                            "prerequisite_count": 1,
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
                    "faculties": ["ACC", "ADM", "BUS", "CSC"],
                    "levels": [0, 1, 2, 3, 4],
                    "categories": ["CORE", "GERP", "GLOAD", "MLOAD"],
                }
            ]
        }
    }
