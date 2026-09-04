from __future__ import annotations

import logging

from fastapi import APIRouter, Depends, HTTPException, Path
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from backend.database.connection import SessionLocal
from backend.schemas.faculty import FacultyListResponse, FacultyStatusUpdateRequest, FacultyStatusUpdateResponse
from backend.services.faculty_service import (
    FacultyAlreadyActiveError,
    FacultyAlreadyInactiveError,
    FacultyNotFoundError,
    NoFacultyStatusChangeError,
    activate_faculty,
    deactivate_faculty,
    list_faculties,
    set_all_faculties_status,
)

router = APIRouter(tags=["Faculties"])
logger = logging.getLogger(__name__)
FACULTY_DATABASE_UNAVAILABLE_DETAIL = (
    "Faculty database is unavailable. Check that PostgreSQL is running and the database has been seeded."
)

FACULTY_DATABASE_ERROR_RESPONSE = {
    "description": "PostgreSQL is unavailable or the faculty table cannot be queried.",
    "content": {"application/json": {"example": {"detail": FACULTY_DATABASE_UNAVAILABLE_DETAIL}}},
}

FACULTY_NOT_FOUND_RESPONSE = {
    "description": "The requested faculty does not exist in the faculty table.",
    "content": {"application/json": {"example": {"detail": "Faculty ADM was not found."}}},
}

FACULTY_CONFLICT_RESPONSE = {
    "description": "The requested status change would not change any faculty row.",
    "content": {"application/json": {"example": {"detail": "Faculty CSC is already active."}}},
}

# Dependency used by faculty routes to open and close one database session per request.
def get_db() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Shared error response for database failures in faculty endpoints.
def raise_faculty_database_error(error: SQLAlchemyError) -> None:
    logger.exception("Faculty database operation failed.")
    raise HTTPException(status_code=503, detail=FACULTY_DATABASE_UNAVAILABLE_DETAIL) from error

# Returns every faculty and its active status.
@router.get(
    "/faculties",
    response_model=FacultyListResponse,
    summary="List all faculties",
    description="No request body required. Returns every faculty stored in PostgreSQL with its active status.",
    response_description="All faculties and their active statuses.",
    responses={503: FACULTY_DATABASE_ERROR_RESPONSE},
)
def read_faculties(db: Session = Depends(get_db)) -> FacultyListResponse:
    try:
        return list_faculties(db)
    except SQLAlchemyError as error:
        raise_faculty_database_error(error)

# Returns only faculties that are active in the module catalogue.
@router.get(
    "/faculties/active",
    response_model=FacultyListResponse,
    summary="List active faculties",
    description="No request body required. Returns faculties currently included in the module catalogue.",
    response_description="Active faculties.",
    responses={503: FACULTY_DATABASE_ERROR_RESPONSE},
)
def read_active_faculties(db: Session = Depends(get_db)) -> FacultyListResponse:
    try:
        return list_faculties(db, is_active=True)
    except SQLAlchemyError as error:
        raise_faculty_database_error(error)

# Returns only faculties that are hidden from the module catalogue.
@router.get(
    "/faculties/inactive",
    response_model=FacultyListResponse,
    summary="List inactive faculties",
    description="No request body required. Returns faculties currently excluded from the module catalogue.",
    response_description="Inactive faculties.",
    responses={503: FACULTY_DATABASE_ERROR_RESPONSE},
)
def read_inactive_faculties(db: Session = Depends(get_db)) -> FacultyListResponse:
    try:
        return list_faculties(db, is_active=False)
    except SQLAlchemyError as error:
        raise_faculty_database_error(error)

# Sets every faculty to active or inactive using a request body.
@router.patch(
    "/faculties/status",
    response_model=FacultyStatusUpdateResponse,
    summary="Set all faculty statuses",
    description=(
        "Request body required. Set `is_active` to true to include all faculties "
        "in the module catalogue, or false to exclude all faculties. Returns 409 "
        "if all faculties already have the requested status."
    ),
    response_description="Faculties whose active status changed.",
    responses={409: FACULTY_CONFLICT_RESPONSE, 503: FACULTY_DATABASE_ERROR_RESPONSE},
)
def update_all_faculty_statuses(
    payload: FacultyStatusUpdateRequest,
    db: Session = Depends(get_db),
) -> FacultyStatusUpdateResponse:
    try:
        return set_all_faculties_status(db, payload.is_active)
    except NoFacultyStatusChangeError as error:
        raise HTTPException(status_code=409, detail=str(error)) from error
    except SQLAlchemyError as error:
        raise_faculty_database_error(error)

# Activates one faculty by exact faculty name.
@router.patch(
    "/faculties/{name}/activate",
    response_model=FacultyStatusUpdateResponse,
    summary="Activate one faculty",
    description=(
        "No request body required. Marks one faculty as active so its modules can "
        "appear in `/modules`. Returns 409 if the faculty is already active."
    ),
    response_description="Activated faculty.",
    responses={404: FACULTY_NOT_FOUND_RESPONSE, 409: FACULTY_CONFLICT_RESPONSE, 503: FACULTY_DATABASE_ERROR_RESPONSE},
)
def activate_one_faculty(
    name: str = Path(description="Faculty name to activate.", examples=["CSC"]),
    db: Session = Depends(get_db),
) -> FacultyStatusUpdateResponse:
    try:
        return activate_faculty(db, name)
    except FacultyNotFoundError as error:
        raise HTTPException(status_code=404, detail=str(error)) from error
    except FacultyAlreadyActiveError as error:
        raise HTTPException(status_code=409, detail=str(error)) from error
    except SQLAlchemyError as error:
        raise_faculty_database_error(error)

# Deactivates one faculty by exact faculty name.
@router.patch(
    "/faculties/{name}/deactivate",
    response_model=FacultyStatusUpdateResponse,
    summary="Deactivate one faculty",
    description=(
        "No request body required. Marks one faculty as inactive so its modules are "
        "excluded from `/modules`. Returns 409 if the faculty is already inactive."
    ),
    response_description="Deactivated faculty.",
    responses={404: FACULTY_NOT_FOUND_RESPONSE, 409: FACULTY_CONFLICT_RESPONSE, 503: FACULTY_DATABASE_ERROR_RESPONSE},
)
def deactivate_one_faculty(
    name: str = Path(description="Faculty name to deactivate.", examples=["ADM"]),
    db: Session = Depends(get_db),
) -> FacultyStatusUpdateResponse:
    try:
        return deactivate_faculty(db, name)
    except FacultyNotFoundError as error:
        raise HTTPException(status_code=404, detail=str(error)) from error
    except FacultyAlreadyInactiveError as error:
        raise HTTPException(status_code=409, detail=str(error)) from error
    except SQLAlchemyError as error:
        raise_faculty_database_error(error)
