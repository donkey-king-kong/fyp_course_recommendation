from __future__ import annotations
from typing import Optional
from pydantic import BaseModel

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

# Paginated list response so the frontend does not fetch all modules at once.
class ModuleListResponse(BaseModel):
    items: list[ModuleSummary]
    total: int
    limit: int
    offset: int

# Valid database-backed filter values for frontend dropdowns.
class ModuleFilterOptionsResponse(BaseModel):
    faculties: list[str]
    levels: list[int]
    categories: list[str]
