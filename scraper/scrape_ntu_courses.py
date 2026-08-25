from __future__ import annotations

import argparse
import json
from pathlib import Path

from ntu_course_scraper import fetch_course_page, parse_courses


ACADEMIC_SEMESTERS = [
    ("2022_1", "2022-semester-1"),
    ("2022_2", "2022-semester-2"),
    ("2023_1", "2023-semester-1"),
    ("2023_2", "2023-semester-2"),
    ("2024_1", "2024-semester-1"),
    ("2024_2", "2024-semester-2"),
    ("2025_1", "2025-semester-1"),
    ("2025_2", "2025-semester-2"),
    ("2026_1", "2026-semester-1"),
]

COURSE_YEAR_OPTIONS = [
    ("CSC;;1;F", "computer-science-year-1"),
    ("CSC;;2;F", "computer-science-year-2"),
    ("CSC;;3;F", "computer-science-year-3"),
    ("CSC;;4;F", "computer-science-year-4"),
    ("COMP;;1;F", "computing-year-1"),
    ("COMP;;2;F", "computing-year-2"),
    ("COMP;;3;F", "computing-year-3"),
    ("DSAI;;1;F", "data-science-ai-year-1"),
    ("DSAI;;2;F", "data-science-ai-year-2"),
    ("DSAI;;3;F", "data-science-ai-year-3"),
    ("DSAI;;4;F", "data-science-ai-year-4"),
    ("ECDS;;1;F", "economics-data-science-year-1"),
    ("ECDS;;2;F", "economics-data-science-year-2"),
    ("ECDS;;3;F", "economics-data-science-year-3"),
    ("ECDS;;4;F", "economics-data-science-year-4"),
    ("CE;;1;F", "computer-engineering-year-1"),
    ("CE;;2;F", "computer-engineering-year-2"),
    ("CE;;3;F", "computer-engineering-year-3"),
    ("CE;;4;F", "computer-engineering-year-4"),
    ("REP;CE;2;F", "renaissance-engineering-ce-year-2"),
    ("REP;CE;3;F", "renaissance-engineering-ce-year-3"),
    ("REP;CE;4;F", "renaissance-engineering-ce-year-4"),
    ("REP;CSC;2;F", "renaissance-engineering-csc-year-2"),
    ("REP;CSC;3;F", "renaissance-engineering-csc-year-3"),
    ("REP;CSC;4;F", "renaissance-engineering-csc-year-4"),
    ("ACDA;;1;F", "accountancy-data-science-ai-year-1"),
    ("ACDA;;2;F", "accountancy-data-science-ai-year-2"),
    ("ACDA;;3;F", "accountancy-data-science-ai-year-3"),
    ("ACDA;;4;F", "accountancy-data-science-ai-year-4"),
    ("ACDA;;5;F", "accountancy-data-science-ai-year-5"),
    ("BCE;;1;F", "business-computer-engineering-year-1"),
    ("BCE;;4;F", "business-computer-engineering-year-4"),
    ("BCG;;1;F", "business-computing-year-1"),
    ("BCG;;2;F", "business-computing-year-2"),
    ("BCG;;3;F", "business-computing-year-3"),
    ("BCG;;4;F", "business-computing-year-4"),
    ("CEEC;;1;F", "computer-engineering-economics-year-1"),
    ("CEEC;;2;F", "computer-engineering-economics-year-2"),
    ("CEEC;;3;F", "computer-engineering-economics-year-3"),
    ("CEEC;;4;F", "computer-engineering-economics-year-4"),
    ("CEEC;;5;F", "computer-engineering-economics-year-5"),
    ("CSEC;;1;F", "computer-science-economics-year-1"),
    ("CSEC;;2;F", "computer-science-economics-year-2"),
    ("CSEC;;3;F", "computer-science-economics-year-3"),
    ("CSEC;;4;F", "computer-science-economics-year-4"),
    ("CSEC;;5;F", "computer-science-economics-year-5"),
]


def main() -> None:
    parser = argparse.ArgumentParser(description="Scrape NTU course information.")
    parser.add_argument("--acadsem", default="2026_1", help="Academic year and semester, e.g. 2026_1.")
    parser.add_argument("--course-yr", default="CSC;;1;F", help="NTU course year value, e.g. CSC;;1;F.")
    parser.add_argument("--output", type=Path, help="Optional JSON output path.")
    parser.add_argument("--raw-html-output", type=Path, help="Optional raw HTML output path for debugging.")
    parser.add_argument("--all", action="store_true", help="Scrape all configured academic semester and course-year combinations.")
    parser.add_argument("--output-dir", type=Path, default=Path("scraper/output"), help="Directory for --all JSON output files.")
    args = parser.parse_args()

    if args.all:
        scrape_all(output_dir=args.output_dir)
        return

    html = fetch_course_page(acadsem=args.acadsem, course_yr=args.course_yr)

    if args.raw_html_output:
        args.raw_html_output.parent.mkdir(parents=True, exist_ok=True)
        args.raw_html_output.write_text(html, encoding="utf-8")

    courses = parse_courses(html)
    data = [course.to_dict() for course in courses]

    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(data, indent=2), encoding="utf-8")
        print(f"Saved {len(data)} courses to {args.output}")
        return

    print(json.dumps(data, indent=2))


def scrape_all(output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)

    for acadsem, acad_label in ACADEMIC_SEMESTERS:
        for course_yr, course_label in COURSE_YEAR_OPTIONS:
            output_path = output_dir / f"{acad_label}-{course_label}.json"
            html = fetch_course_page(acadsem=acadsem, course_yr=course_yr)
            courses = parse_courses(html)
            data = [course.to_dict() for course in courses]

            output_path.write_text(json.dumps(data, indent=2), encoding="utf-8")
            print(f"Saved {len(data)} courses to {output_path}")


if __name__ == "__main__":
    main()
