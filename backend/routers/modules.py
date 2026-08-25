from __future__ import annotations

from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from backend.database.connection import SessionLocal
from backend.schemas.module import ModuleFilterOptionsResponse, ModuleListResponse, ModuleSummary
from backend.services.module_service import get_module_by_code, get_module_filter_options, list_modules

router = APIRouter()

def get_db() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/modules/filters", response_model=ModuleFilterOptionsResponse)
def read_module_filters(db: Session = Depends(get_db)) -> ModuleFilterOptionsResponse:
    return get_module_filter_options(db)

@router.get("/modules", response_model=ModuleListResponse)
def read_modules(
    search: Optional[str] = Query(default=None, description="Search by module code or title."),
    faculty: Optional[str] = Query(default=None, description="Filter by exact faculty value."),
    level: Optional[int] = Query(default=None, ge=0, le=9, description="Filter by inferred module level."),
    category: Optional[str] = Query(default=None, description="Filter by category, such as CORE or BDE."),
    current_only: bool = Query(default=False, description="Only show modules marked as current semester."),
    limit: int = Query(default=30, ge=1, le=100, description="Maximum number of modules to return."),
    offset: int = Query(default=0, ge=0, description="Number of modules to skip for pagination."),
    db: Session = Depends(get_db),
) -> ModuleListResponse:
    return list_modules(
        db=db,
        search=search,
        faculty=faculty,
        level=level,
        category=category,
        current_only=current_only,
        limit=limit,
        offset=offset,
    )


@router.get("/modules/{code}", response_model=ModuleSummary)
def read_module(code: str, db: Session = Depends(get_db)) -> ModuleSummary:
    module = get_module_by_code(db, code)

    if module is None:
        raise HTTPException(status_code=404, detail=f"Module {code.upper()} was not found.")

    return module
