import json
from pathlib import Path

CATALOG_PATH = Path(__file__).resolve().parents[2] / "data" / "course_catalog.json"

# Only reciprocal, exact-code catalog declarations are strong enough for this prototype filter.
def load_reciprocal_exclusions() -> dict[str, frozenset[str]]:
    catalog = json.loads(CATALOG_PATH.read_text(encoding="utf-8"))
    declared = {
        course["code"]: set(course.get("mutually_exclusive") or [])
        for course in catalog
    }
    return {
        code: frozenset(
            other for other in exclusions
            if code in declared.get(other, set())
        )
        for code, exclusions in declared.items()
    }

RECIPROCAL_EXCLUSIONS = load_reciprocal_exclusions()

def conflicts_with_completed_course(course_code: str, completed_codes: set[str]) -> bool:
    return bool(RECIPROCAL_EXCLUSIONS.get(course_code, frozenset()) & completed_codes)
