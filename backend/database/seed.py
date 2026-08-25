from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from backend.database.connection import SessionLocal, engine
from backend.models import Base, ModuleModel, ModulePrerequisiteModel

# Source dataset downloaded from NTUMods and committed under the repo data folder.
MODULES_JSON_PATH = Path(__file__).resolve().parents[2] / "data" / "modules.json"
PREREQUISITE_GRAPH_JSON_PATH = Path(__file__).resolve().parents[2] / "data" / "ntu_prerequisite_unlock_graph.json"

def seed_database() -> None:
    # Create missing tables before inserting data so local setup stays simple.
    Base.metadata.create_all(bind=engine)

    modules = load_modules(MODULES_JSON_PATH)
    prerequisite_graph = load_prerequisite_graph(PREREQUISITE_GRAPH_JSON_PATH)
    db = SessionLocal()

    try:
        inserted_count, updated_count = seed_modules(db, modules)
        prerequisite_count = seed_prerequisite_relationships(db, prerequisite_graph)
        db.commit()

        print(f"Inserted {inserted_count} modules.")
        print(f"Updated {updated_count} modules.")
        print(f"Seeded {prerequisite_count} prerequisite relationships.")
        print("Successfully seeded module data into PostgreSQL.")
    finally:
        db.close()

def seed_modules(db: Any, modules: list[dict[str, Any]]) -> tuple[int, int]:
    inserted_count = 0
    updated_count = 0

    print(f"Found {len(modules)} modules to seed...")

    for module in modules:
        code = module.get("code")

        if not code:
            continue

        existing = db.query(ModuleModel).filter_by(code=code).first()
        module_data = build_module_data(module)

        if existing:
            # Update existing rows so the seed script can be rerun safely.
            for key, value in module_data.items():
                setattr(existing, key, value)
            updated_count += 1
            continue

        db.add(ModuleModel(**module_data))
        inserted_count += 1

    return inserted_count, updated_count

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

def build_module_data(module: dict[str, Any]) -> dict[str, Any]:
    code = module["code"]

    return {
        "code": code,
        "title": module.get("title", ""),
        "au": parse_au(module.get("au")),
        "faculty": module.get("faculty"),
        "description": module.get("description"),
        "level": infer_level(code),
        "categories": module.get("categories", []),
        "latest_year": module.get("latestYear"),
        "latest_semester": module.get("latestSemester"),
        "is_current_semester": bool(module.get("isCurrentSemester", False)),
        "not_available_to_programme": module.get("notAvailableToProgramme"),
    }

def parse_au(value: Any) -> float | None:
    if value in (None, ""):
        return None

    try:
        return float(value)
    except (TypeError, ValueError):
        return None

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

if __name__ == "__main__":
    seed_database()
