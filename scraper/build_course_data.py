from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any

DEFAULT_INPUT_DIR = Path("scraper/output")
DEFAULT_CATALOG_OUTPUT = Path("data/course_catalog.json")
DEFAULT_OFFERINGS_OUTPUT = Path("data/course_offerings.json")
FILENAME_PATTERN = re.compile(
    r"^(?P<acad_year>\d{4})-semester-(?P<semester>\d)-(?P<programme>.+)-year-(?P<study_year>\d)\.json$"
)

def main() -> None:
    parser = argparse.ArgumentParser(description="Build normalized course data from scraped NTU output.")
    parser.add_argument("--input-dir", type=Path, default=DEFAULT_INPUT_DIR)
    parser.add_argument("--catalog-output", type=Path, default=DEFAULT_CATALOG_OUTPUT)
    parser.add_argument("--offerings-output", type=Path, default=DEFAULT_OFFERINGS_OUTPUT)
    args = parser.parse_args()

    catalog, offerings = build_course_data(input_dir=args.input_dir)

    write_json(args.catalog_output, catalog)
    write_json(args.offerings_output, offerings)

    print(f"Saved {len(catalog)} unique courses to {args.catalog_output}")
    print(f"Saved {len(offerings)} course offerings to {args.offerings_output}")

def build_course_data(input_dir: Path) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    catalog_by_code: dict[str, dict[str, Any]] = {}
    offerings: list[dict[str, Any]] = []

    for input_path in sorted(input_dir.glob("*.json")):
        metadata = parse_output_filename(input_path.name)

        if metadata is None:
            continue

        courses = json.loads(input_path.read_text(encoding="utf-8"))

        for course in courses:
            course_code = course["code"]
            catalog_by_code[course_code] = merge_course_records(
                existing=catalog_by_code.get(course_code),
                incoming=course,
            )
            offerings.append(
                {
                    "acad_year": metadata["acad_year"],
                    "semester": metadata["semester"],
                    "programme": metadata["programme"],
                    "study_year": metadata["study_year"],
                    "course_code": course_code,
                }
            )

    return sorted(catalog_by_code.values(), key=lambda course: course["code"]), offerings


def parse_output_filename(filename: str) -> dict[str, Any] | None:
    match = FILENAME_PATTERN.match(filename)
    if match is None:
        return None

    return {
        "acad_year": match.group("acad_year"),
        "semester": match.group("semester"),
        "programme": match.group("programme"),
        "study_year": int(match.group("study_year")),
    }


def merge_course_records(existing: dict[str, Any] | None, incoming: dict[str, Any]) -> dict[str, Any]:
    if existing is None:
        return incoming

    merged = existing.copy()

    for key, incoming_value in incoming.items():
        existing_value = merged.get(key)

        if isinstance(existing_value, list) and isinstance(incoming_value, list):
            merged[key] = sorted({*existing_value, *incoming_value})
            continue

        if not existing_value and incoming_value:
            merged[key] = incoming_value

    return merged


def write_json(output_path: Path, data: list[dict[str, Any]]) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(data, indent=2), encoding="utf-8")


if __name__ == "__main__":
    main()
