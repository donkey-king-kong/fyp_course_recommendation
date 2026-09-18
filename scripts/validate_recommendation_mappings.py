import json
import sys
from pathlib import Path

from backend.services.career_skill_mappings import CAREER_SKILL_MAPPINGS
from backend.services.recommendation_service import RECOMMENDATION_TAG_ALIASES


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


def find_invalid_preference_aliases(catalog_tags: set[str]) -> list[str]:
    invalid_aliases: list[str] = []

    for alias, resolved_tags in RECOMMENDATION_TAG_ALIASES.items():
        if not resolved_tags:
            invalid_aliases.append(f"{alias} resolves to no catalog tags")
            continue

        for resolved_tag in resolved_tags:
            if resolved_tag not in catalog_tags:
                invalid_aliases.append(
                    f"{alias} resolves to missing catalog tag {resolved_tag}"
                )

    return invalid_aliases


def main() -> int:
    catalog_tags = load_catalog_tags()
    missing_tags = find_missing_mapping_tags(catalog_tags)
    invalid_aliases = find_invalid_preference_aliases(catalog_tags)

    if not missing_tags and not invalid_aliases:
        print("All career-skill mapping tags and preference aliases are valid.")
        return 0

    if missing_tags:
        print("Missing career-skill mapping tags:")
        for missing_tag in missing_tags:
            print(f"- {missing_tag}")

    if invalid_aliases:
        print("Invalid preference aliases:")
        for invalid_alias in invalid_aliases:
            print(f"- {invalid_alias}")

    return 1


if __name__ == "__main__":
    sys.exit(main())
