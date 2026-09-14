from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any

from sqlalchemy import inspect, text

from backend.database.connection import SessionLocal, engine
from backend.models import Base, FacultyModel, ModuleModel, ModulePrerequisiteModel

# Source dataset downloaded from NTUMods and committed under the repo data folder.
MODULES_JSON_PATH = Path(__file__).resolve().parents[2] / "data" / "modules.json"
PREREQUISITE_GRAPH_JSON_PATH = Path(__file__).resolve().parents[2] / "data" / "ntu_prerequisite_unlock_graph.json"
COURSE_CATALOG_JSON_PATH = Path(__file__).resolve().parents[2] / "data" / "course_catalog.json"
COURSE_OFFERINGS_JSON_PATH = Path(__file__).resolve().parents[2] / "data" / "course_offerings.json"
MPE_SPECIALISATION_PATHS_JSON_PATH = Path(__file__).resolve().parents[2] / "data" / "mpe_specialisation_paths.json"
DEFAULT_ACTIVE_FACULTIES = {"CSC", "CE"}
AU_NUMBER_PATTERN = re.compile(r"\d+(?:\.\d+)?")
CODE_PREFIX_FACULTY_OVERRIDES = {"SC": "CSC"}

def seed_database() -> None:
    # Create missing tables before inserting data so local setup stays simple.
    Base.metadata.create_all(bind=engine)
    ensure_module_recommendation_tags_column()
    ensure_module_mpe_specialisations_column()
    ensure_module_recommendation_profile_column()
    ensure_module_bde_ue_unavailability_column()

    modules = load_modules(MODULES_JSON_PATH)
    prerequisite_graph = load_prerequisite_graph(PREREQUISITE_GRAPH_JSON_PATH)
    catalog_by_code = load_course_catalog_by_code(COURSE_CATALOG_JSON_PATH)
    offerings_by_code = load_course_offerings_by_code(COURSE_OFFERINGS_JSON_PATH)
    description_by_code = load_course_catalog_descriptions(COURSE_CATALOG_JSON_PATH)
    mpe_specialisations_by_code = load_mpe_specialisations(
        MPE_SPECIALISATION_PATHS_JSON_PATH
    )
    modules = include_catalog_only_mpe_modules(
        modules,
        catalog_by_code,
        offerings_by_code,
        mpe_specialisations_by_code,
    )
    bde_ue_unavailable_by_code = load_course_catalog_bde_ue_unavailability(
        COURSE_CATALOG_JSON_PATH
    )
    db = SessionLocal()

    try:
        inserted_count, updated_count = seed_modules(
            db,
            modules,
            description_by_code,
            mpe_specialisations_by_code,
            bde_ue_unavailable_by_code,
        )
        faculty_count = seed_faculties(db, modules)
        prerequisite_count = seed_prerequisite_relationships(db, prerequisite_graph)
        db.commit()

        print(f"Found {len(description_by_code)} catalog descriptions.")
        print(f"Found {len(mpe_specialisations_by_code)} MPE-listed modules.")
        print(f"Inserted {inserted_count} modules.")
        print(f"Updated {updated_count} modules.")
        print(f"Seeded {faculty_count} faculties.")
        print(f"Seeded {prerequisite_count} prerequisite relationships.")
        print("Successfully seeded module data into PostgreSQL.")
    finally:
        db.close()

def seed_mpe_specialisations_only() -> None:
    Base.metadata.create_all(bind=engine)
    ensure_module_recommendation_tags_column()
    ensure_module_mpe_specialisations_column()
    ensure_module_recommendation_profile_column()
    ensure_module_bde_ue_unavailability_column()

    mpe_specialisations_by_code = load_mpe_specialisations(
        MPE_SPECIALISATION_PATHS_JSON_PATH
    )
    catalog_by_code = load_course_catalog_by_code(COURSE_CATALOG_JSON_PATH)
    offerings_by_code = load_course_offerings_by_code(COURSE_OFFERINGS_JSON_PATH)
    db = SessionLocal()

    try:
        inserted_count, updated_count, missing_count = seed_mpe_specialisation_modules(
            db,
            mpe_specialisations_by_code,
            catalog_by_code,
            offerings_by_code,
        )
        db.commit()

        print(f"Found {len(mpe_specialisations_by_code)} MPE-listed modules.")
        print(f"Inserted {inserted_count} missing MPE-listed modules.")
        print(f"Updated {updated_count} existing MPE-listed modules.")
        print(f"Skipped {missing_count} MPE-listed modules missing from catalog data.")
        print("Successfully seeded MPE specialisation data.")
    finally:
        db.close()

def seed_modules(
    db: Any,
    modules: list[dict[str, Any]],
    description_by_code: dict[str, str],
    mpe_specialisations_by_code: dict[str, list[str]],
    bde_ue_unavailable_by_code: dict[str, list[str]],
) -> tuple[int, int]:
    inserted_count = 0
    updated_count = 0

    print(f"Found {len(modules)} modules to seed...")

    for module in modules:
        code = module.get("code")

        if not code:
            continue

        existing = db.query(ModuleModel).filter_by(code=code).first()
        module_data = build_module_data(
            module,
            description_by_code,
            mpe_specialisations_by_code,
            bde_ue_unavailable_by_code,
        )

        if existing:
            # Update existing rows so the seed script can be rerun safely.
            for key, value in module_data.items():
                setattr(existing, key, value)
            updated_count += 1
            continue

        db.add(ModuleModel(**module_data))
        inserted_count += 1

    return inserted_count, updated_count

def seed_mpe_specialisation_modules(
    db: Any,
    mpe_specialisations_by_code: dict[str, list[str]],
    catalog_by_code: dict[str, dict[str, Any]],
    offerings_by_code: dict[str, list[dict[str, Any]]],
) -> tuple[int, int, int]:
    inserted_count = 0
    updated_count = 0
    missing_count = 0

    for code, specialisations in sorted(mpe_specialisations_by_code.items()):
        existing = db.query(ModuleModel).filter_by(code=code).first()

        if existing:
            existing.mpe_specialisations = specialisations
            updated_count += 1
            continue

        catalog_course = catalog_by_code.get(code)

        if not catalog_course:
            missing_count += 1
            continue

        db.add(
            ModuleModel(
                **build_catalog_module_data(
                    catalog_course,
                    offerings_by_code.get(code, []),
                    specialisations,
                )
            )
        )
        inserted_count += 1

    return inserted_count, updated_count, missing_count

def seed_faculties(db: Any, modules: list[dict[str, Any]]) -> int:
    faculty_names = sorted({module["faculty"] for module in modules if module.get("faculty")})

    for faculty_name in faculty_names:
        existing = db.query(FacultyModel).filter_by(name=faculty_name).first()

        if existing:
            continue

        db.add(FacultyModel(name=faculty_name, is_active=faculty_name in DEFAULT_ACTIVE_FACULTIES))

    return len(faculty_names)

def seed_prerequisite_relationships(db: Any, prerequisite_graph: dict[str, dict[str, list[str]]]) -> int:
    relationships = build_prerequisite_relationships(prerequisite_graph)

    # Rebuild generated relationships each run so deleted prerequisites do not linger.
    db.query(ModulePrerequisiteModel).delete()

    db.add_all(
        ModulePrerequisiteModel(module_code=module_code, prerequisite_code=prerequisite_code)
        for module_code, prerequisite_code in relationships
    )

    return len(relationships)

def load_modules(input_path: Path) -> list[dict[str, Any]]:
    try:
        data = json.loads(input_path.read_text(encoding="utf-8"))
    except FileNotFoundError as error:
        raise FileNotFoundError(f"Could not find {input_path}. Run this script from the project repo.") from error

    return data.get("modules", [])

def load_prerequisite_graph(input_path: Path) -> dict[str, dict[str, list[str]]]:
    try:
        return json.loads(input_path.read_text(encoding="utf-8"))
    except FileNotFoundError as error:
        raise FileNotFoundError(f"Could not find {input_path}. Run this script from the project repo.") from error

def load_course_catalog_descriptions(input_path: Path) -> dict[str, str]:
    try:
        courses = json.loads(input_path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        return {}

    return {
        course["code"]: course["description"].strip()
        for course in courses
        if course.get("code") and isinstance(course.get("description"), str) and course["description"].strip()
    }

def load_course_catalog_by_code(input_path: Path) -> dict[str, dict[str, Any]]:
    try:
        courses = json.loads(input_path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        return {}

    return {
        course["code"]: course
        for course in courses
        if course.get("code")
    }

def load_course_offerings_by_code(input_path: Path) -> dict[str, list[dict[str, Any]]]:
    try:
        offerings = json.loads(input_path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        return {}

    offerings_by_code: dict[str, list[dict[str, Any]]] = {}

    for offering in offerings:
        course_code = offering.get("course_code")

        if course_code:
            offerings_by_code.setdefault(course_code, []).append(offering)

    return offerings_by_code

def load_course_catalog_bde_ue_unavailability(input_path: Path) -> dict[str, list[str]]:
    try:
        courses = json.loads(input_path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        return {}

    return {
        course["code"]: course["not_available_as_bde_ue_to_programme"]
        for course in courses
        if course.get("code") and isinstance(course.get("not_available_as_bde_ue_to_programme"), list)
    }

def load_mpe_specialisations(input_path: Path) -> dict[str, list[str]]:
    try:
        data = json.loads(input_path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        return {}

    specialisations_by_code: dict[str, list[str]] = {}

    for path_key, path_data in data.get("paths", {}).items():
        for course_code in path_data.get("courseCodes", []):
            specialisations_by_code.setdefault(course_code, []).append(path_key)

    return {
        course_code: sorted(set(specialisations))
        for course_code, specialisations in specialisations_by_code.items()
    }

def build_module_data(
    module: dict[str, Any],
    description_by_code: dict[str, str] | None = None,
    mpe_specialisations_by_code: dict[str, list[str]] | None = None,
    bde_ue_unavailable_by_code: dict[str, list[str]] | None = None,
) -> dict[str, Any]:
    code = module["code"]
    description = (description_by_code or {}).get(code) or module.get("description")

    return {
        "code": code,
        "title": module.get("title", ""),
        "au": parse_au(module.get("au")),
        "faculty": module.get("faculty"),
        "description": description,
        "level": infer_level(code),
        "categories": module.get("categories", []),
        "recommendation_tags": module.get("recommendationTags", []),
        "mpe_specialisations": (mpe_specialisations_by_code or {}).get(code, []),
        "recommendation_profile": module.get("recommendationProfile"),
        "latest_year": module.get("latestYear"),
        "latest_semester": module.get("latestSemester"),
        "is_current_semester": bool(module.get("isCurrentSemester", False)),
        "not_available_to_programme": module.get("notAvailableToProgramme"),
        "not_available_as_bde_ue_to_programme": (bde_ue_unavailable_by_code or {}).get(
            code,
            [],
        ),
    }

def include_catalog_only_mpe_modules(
    modules: list[dict[str, Any]],
    catalog_by_code: dict[str, dict[str, Any]],
    offerings_by_code: dict[str, list[dict[str, Any]]],
    mpe_specialisations_by_code: dict[str, list[str]],
) -> list[dict[str, Any]]:
    existing_codes = {module.get("code") for module in modules}
    supplemental_modules = [
        build_catalog_module_source(catalog_by_code[code], offerings_by_code.get(code, []))
        for code in sorted(mpe_specialisations_by_code)
        if code not in existing_codes and code in catalog_by_code
    ]

    return modules + supplemental_modules

def build_catalog_module_source(
    course: dict[str, Any],
    offerings: list[dict[str, Any]],
) -> dict[str, Any]:
    latest_offering = get_latest_offering(offerings)
    code = course["code"]

    return {
        "code": code,
        "title": format_catalog_title(course.get("title", "")),
        "au": course.get("no_of_credits"),
        "faculty": infer_faculty(code),
        "categories": [],
        "latestYear": latest_offering.get("acad_year") if latest_offering else None,
        "latestSemester": latest_offering.get("semester") if latest_offering else None,
        "isCurrentSemester": latest_offering is not None,
        "notAvailableToProgramme": format_catalog_restriction(
            course.get("not_available_to_programme", [])
        ),
        "recommendationTags": [],
        "description": course.get("description"),
    }

def build_catalog_module_data(
    course: dict[str, Any],
    offerings: list[dict[str, Any]],
    mpe_specialisations: list[str],
) -> dict[str, Any]:
    module = build_catalog_module_source(course, offerings)
    module_data = build_module_data(module, {}, {module["code"]: mpe_specialisations}, {})
    module_data["not_available_as_bde_ue_to_programme"] = course.get(
        "not_available_as_bde_ue_to_programme",
        [],
    )

    return module_data

def parse_au(value: Any) -> float | None:
    if value in (None, ""):
        return None

    try:
        return float(value)
    except (TypeError, ValueError):
        match = AU_NUMBER_PATTERN.search(str(value))

        return float(match.group()) if match else None

def infer_faculty(code: str) -> str | None:
    match = re.match(r"[A-Z]+", code)

    if not match:
        return None

    prefix = match.group()

    return CODE_PREFIX_FACULTY_OVERRIDES.get(prefix, prefix)

def get_latest_offering(offerings: list[dict[str, Any]]) -> dict[str, Any] | None:
    if not offerings:
        return None

    return max(
        offerings,
        key=lambda offering: (
            int(offering.get("acad_year") or 0),
            int(offering.get("semester") or 0),
        ),
    )

def format_catalog_title(title: Any) -> str:
    words = str(title or "").replace("&", "and").title().split()
    lowercase_words = {"And", "In", "Of", "Or", "The", "To"}

    return " ".join(
        word.lower() if index > 0 and word in lowercase_words else word
        for index, word in enumerate(words)
    )

def format_catalog_restriction(restrictions: list[str]) -> str | None:
    if not restrictions:
        return None

    return ", ".join(restrictions)

def infer_level(code: str) -> int | None:
    for character in code:
        if character.isdigit():
            return int(character)

    return None

def build_prerequisite_relationships(prerequisite_graph: dict[str, dict[str, list[str]]]) -> list[tuple[str, str]]:
    relationships = set()

    for module_code, graph_data in prerequisite_graph.items():
        for prerequisite_code in graph_data.get("prerequisites", []):
            relationships.add((module_code, prerequisite_code))

    return sorted(relationships)

def ensure_module_recommendation_tags_column() -> None:
    existing_columns = {
        column["name"]
        for column in inspect(engine).get_columns(ModuleModel.__tablename__)
    }

    if "recommendation_tags" in existing_columns:
        return

    column_type = "JSON DEFAULT '[]'::json"
    if engine.dialect.name == "sqlite":
        column_type = "JSON DEFAULT '[]'"

    with engine.begin() as connection:
        connection.execute(
            text(f"ALTER TABLE modules ADD COLUMN recommendation_tags {column_type}")
        )

def ensure_module_mpe_specialisations_column() -> None:
    existing_columns = {
        column["name"]
        for column in inspect(engine).get_columns(ModuleModel.__tablename__)
    }

    if "mpe_specialisations" in existing_columns:
        return

    column_type = "JSON DEFAULT '[]'::json"
    if engine.dialect.name == "sqlite":
        column_type = "JSON DEFAULT '[]'"

    with engine.begin() as connection:
        connection.execute(
            text(f"ALTER TABLE modules ADD COLUMN mpe_specialisations {column_type}")
        )

def ensure_module_recommendation_profile_column() -> None:
    existing_columns = {
        column["name"]
        for column in inspect(engine).get_columns(ModuleModel.__tablename__)
    }

    if "recommendation_profile" in existing_columns:
        return

    with engine.begin() as connection:
        connection.execute(
            text("ALTER TABLE modules ADD COLUMN recommendation_profile VARCHAR(40)")
        )

def ensure_module_bde_ue_unavailability_column() -> None:
    existing_columns = {
        column["name"]
        for column in inspect(engine).get_columns(ModuleModel.__tablename__)
    }

    if "not_available_as_bde_ue_to_programme" in existing_columns:
        return

    column_type = "JSON DEFAULT '[]'::json"
    if engine.dialect.name == "sqlite":
        column_type = "JSON DEFAULT '[]'"

    with engine.begin() as connection:
        connection.execute(
            text(
                "ALTER TABLE modules "
                f"ADD COLUMN not_available_as_bde_ue_to_programme {column_type}"
            )
        )

def main() -> None:
    parser = argparse.ArgumentParser(description="Seed module data into the app database.")
    parser.add_argument(
        "--mpe-specialisations-only",
        action="store_true",
        help="Only add/update official MPE specialisation tags and missing MPE-listed modules.",
    )
    args = parser.parse_args()

    if args.mpe_specialisations_only:
        seed_mpe_specialisations_only()
        return

    seed_database()

if __name__ == "__main__":
    main()
