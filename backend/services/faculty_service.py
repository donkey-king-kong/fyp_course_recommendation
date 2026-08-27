from __future__ import annotations

from sqlalchemy.orm import Session

from backend.models import FacultyModel
from backend.schemas.faculty import FacultyListResponse, FacultyResponse, FacultyStatusUpdateResponse

class FacultyNotFoundError(ValueError):
    pass

class FacultyAlreadyActiveError(ValueError):
    pass

class FacultyAlreadyInactiveError(ValueError):
    pass

class NoFacultyStatusChangeError(ValueError):
    pass

# Converts one SQLAlchemy faculty row into an API response model.
def build_faculty_response(faculty: FacultyModel) -> FacultyResponse:
    return FacultyResponse(name=faculty.name, is_active=faculty.is_active)

# Lists faculties, optionally narrowed to active or inactive rows.
def list_faculties(db: Session, is_active: bool | None = None) -> FacultyListResponse:
    query = db.query(FacultyModel)

    if is_active is not None:
        query = query.filter(FacultyModel.is_active.is_(is_active))

    faculties = query.order_by(FacultyModel.name).all()

    return FacultyListResponse(
        items=[build_faculty_response(faculty) for faculty in faculties],
        total=len(faculties),
    )

# Returns active faculty names used by the module catalogue service.
def list_active_faculty_names(db: Session) -> list[str]:
    return [
        name
        for (name,) in db.query(FacultyModel.name)
        .filter(FacultyModel.is_active.is_(True))
        .order_by(FacultyModel.name)
        .all()
    ]

# Sets every faculty to the same status and rejects no-op updates.
def set_all_faculties_status(db: Session, is_active: bool) -> FacultyStatusUpdateResponse:
    faculties = db.query(FacultyModel).order_by(FacultyModel.name).all()
    changed_faculties = [faculty for faculty in faculties if faculty.is_active != is_active]

    if not changed_faculties:
        raise NoFacultyStatusChangeError("All faculties already have the requested active status.")

    for faculty in changed_faculties:
        faculty.is_active = is_active

    db.commit()

    return FacultyStatusUpdateResponse(
        updated_count=len(changed_faculties),
        items=[build_faculty_response(faculty) for faculty in changed_faculties],
    )

# Activates one faculty and rejects unknown or already-active faculties.
def activate_faculty(db: Session, name: str) -> FacultyStatusUpdateResponse:
    faculty = get_faculty_or_raise(db, name)

    if faculty.is_active:
        raise FacultyAlreadyActiveError(f"Faculty {faculty.name} is already active.")

    faculty.is_active = True
    db.commit()

    return FacultyStatusUpdateResponse(updated_count=1, items=[build_faculty_response(faculty)])

# Deactivates one faculty and rejects unknown or already-inactive faculties.
def deactivate_faculty(db: Session, name: str) -> FacultyStatusUpdateResponse:
    faculty = get_faculty_or_raise(db, name)

    if not faculty.is_active:
        raise FacultyAlreadyInactiveError(f"Faculty {faculty.name} is already inactive.")

    faculty.is_active = False
    db.commit()

    return FacultyStatusUpdateResponse(updated_count=1, items=[build_faculty_response(faculty)])

# Looks up a faculty by name using uppercase labels stored in the database.
def get_faculty_or_raise(db: Session, name: str) -> FacultyModel:
    faculty = db.query(FacultyModel).filter(FacultyModel.name == name.upper()).first()

    if faculty is None:
        raise FacultyNotFoundError(f"Faculty {name.upper()} was not found.")

    return faculty
