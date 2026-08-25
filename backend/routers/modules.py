from __future__ import annotations

from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Path, Query
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from backend.database.connection import SessionLocal
from backend.schemas.module import ModuleFilterOptionsResponse, ModuleListResponse, ModuleSummary
from backend.services.module_service import get_module_by_code, get_module_filter_options, list_modules

router = APIRouter(tags=["Modules"])

MODULE_DATABASE_ERROR_RESPONSE = {
    "description": "PostgreSQL is unavailable or the module tables cannot be queried.",
    "content": {"application/json": {"example": {"detail": "Module database is currently unavailable."}}},
}

MODULE_NOT_FOUND_RESPONSE = {
    "description": "The requested module code does not exist in the module table.",
    "content": {"application/json": {"example": {"detail": "Module NOPE9999 was not found."}}},
}

# Dependency used by module routes to open and close one database session per request.
def get_db() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Shared error response for database failures in module endpoints.
def raise_module_database_error() -> None:
    raise HTTPException(status_code=503, detail="Module database is currently unavailable.")

# Returns valid filter values so the frontend does not hardcode database labels.
@router.get(
    "/modules/filters",
    response_model=ModuleFilterOptionsResponse,
    summary="Get module filter options",
    description=(
        "No request body required. Returns valid faculty, level, and category values "
        "from PostgreSQL for frontend filter dropdowns."
    ),
    response_description="Available module filter options.",
    responses={503: MODULE_DATABASE_ERROR_RESPONSE},
)
def read_module_filters(db: Session = Depends(get_db)) -> ModuleFilterOptionsResponse:
    try:
        return get_module_filter_options(db)
    except SQLAlchemyError:
        raise_module_database_error()

# Returns a paginated module list with optional search and filter parameters.
@router.get(
    "/modules",
    response_model=ModuleListResponse,
    summary="List, search, and filter modules",
    description=(
        "No request body required. Returns one paginated page of modules. Use query "
        "parameters to search by code/title and filter by faculty, level, category, "
        "or current-semester status."
    ),
    response_description="Paginated module results with prerequisite and unlock data.",
    responses={503: MODULE_DATABASE_ERROR_RESPONSE},
)
def read_modules(
    search: Optional[str] = Query(default=None, description="Search by module code or title.", examples=["BE2601"]),
    faculty: Optional[str] = Query(default=None, description="Filter by exact faculty value.", examples=["BUS"]),
    level: Optional[int] = Query(default=None, ge=0, le=9, description="Filter by inferred module level.", examples=[2]),
    category: Optional[str] = Query(default=None, description="Filter by category, such as CORE or GLOAD.", examples=["CORE"]),
    current_only: bool = Query(default=False, description="Only show modules marked as current semester."),
    limit: int = Query(default=30, ge=1, le=100, description="Maximum number of modules to return.", examples=[20]),
    offset: int = Query(default=0, ge=0, description="Number of modules to skip for pagination.", examples=[0]),
    db: Session = Depends(get_db),
) -> ModuleListResponse:
    try:
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
    except SQLAlchemyError:
        raise_module_database_error()

# Returns one exact module by code, or 404 when the code is not in PostgreSQL.
@router.get(
    "/modules/{code}",
    response_model=ModuleSummary,
    summary="Get one module by code",
    description=(
        "No request body required. Returns the exact module matching the path code, "
        "including direct prerequisites and modules unlocked by this module."
    ),
    response_description="One exact module with prerequisite and unlock data.",
    responses={404: MODULE_NOT_FOUND_RESPONSE, 503: MODULE_DATABASE_ERROR_RESPONSE},
)
def read_module(
    code: str = Path(description="Exact module code to fetch.", examples=["BE2601"]),
    db: Session = Depends(get_db),
) -> ModuleSummary:
    try:
        module = get_module_by_code(db, code)
    except SQLAlchemyError:
        raise_module_database_error()
    if module is None:
        raise HTTPException(status_code=404, detail=f"Module {code.upper()} was not found.")

    return module
