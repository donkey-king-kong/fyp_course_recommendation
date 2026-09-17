import json
import sys
from pathlib import Path

from backend.services.career_skill_mappings import CAREER_SKILL_MAPPINGS


PROJECT_ROOT = Path(__file__).resolve().parents[1]
MODULES_PATH = PROJECT_ROOT / "data" / "modules.json"


def load_catalog_tags() -> set[str]:
    modules = json.loads(MODULES_PATH.read_text())["modules"]

    return {
        tag
        for module in modules
        for tag in (module.get("recommendationTags") or [])
    }


def find_missing_mapping_tags(catalog_tags: set[str]) -> list[str]:
    missing_tags: list[str] = []

    for career_goal, mappings in CAREER_SKILL_MAPPINGS.items():
        for mapping in mappings:
            for relationship in mapping.tag_relationships:
                if relationship.tag not in catalog_tags:
                    missing_tags.append(
                        f"{career_goal} / {mapping.skill} / {relationship.tag}"
                    )

    return missing_tags


def main() -> int:
    missing_tags = find_missing_mapping_tags(load_catalog_tags())

    if not missing_tags:
        print("All career-skill mapping tags exist in the module catalog.")
        return 0

    print("Missing career-skill mapping tags:")
    for missing_tag in missing_tags:
        print(f"- {missing_tag}")

    return 1


if __name__ == "__main__":
    sys.exit(main())
