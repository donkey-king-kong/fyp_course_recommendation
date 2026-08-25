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

class ModuleListResponse(BaseModel):
    items: list[ModuleSummary]
    total: int
    limit: int
    offset: int

class ModuleFilterOptionsResponse(BaseModel):
    faculties: list[str]
    levels: list[int]
    categories: list[str]
