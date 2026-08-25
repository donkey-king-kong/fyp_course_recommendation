from __future__ import annotations

import argparse
import json
from pathlib import Path

from ntu_course_scraper import fetch_course_page, parse_courses

def main() -> None:
    parser = argparse.ArgumentParser(description="Scrape NTU course information.")
    parser.add_argument("--acadsem", default="2026_1", help="Academic year and semester, e.g. 2026_1.")
    parser.add_argument("--course-yr", default="CSC;;1;F", help="NTU course year value, e.g. CSC;;1;F.")
    parser.add_argument("--output", type=Path, help="Optional JSON output path.")
    parser.add_argument("--raw-html-output", type=Path, help="Optional raw HTML output path for debugging.")
    args = parser.parse_args()

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

if __name__ == "__main__":
    main()
