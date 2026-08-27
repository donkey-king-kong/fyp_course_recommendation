from __future__ import annotations

from pydantic import BaseModel

# One faculty status row returned by the faculties API.
class FacultyResponse(BaseModel):
    name: str
    is_active: bool

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "name": "CSC",
                    "is_active": True,
                }
            ]
        }
    }

# Faculty list response used by all, active, and inactive listing endpoints.
class FacultyListResponse(BaseModel):
    items: list[FacultyResponse]
    total: int

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "items": [
                        {"name": "CSC", "is_active": True},
                        {"name": "CE", "is_active": True},
                    ],
                    "total": 2,
                }
            ]
        }
    }

# Request body for setting every faculty to the same active status.
class FacultyStatusUpdateRequest(BaseModel):
    is_active: bool

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "is_active": True,
                }
            ]
        }
    }

# Response returned after changing one or many faculty status values.
class FacultyStatusUpdateResponse(BaseModel):
    updated_count: int
    items: list[FacultyResponse]

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "updated_count": 1,
                    "items": [
                        {"name": "CSC", "is_active": True},
                    ],
                }
            ]
        }
    }
