from __future__ import annotations

import re
from dataclasses import asdict, dataclass
from typing import Any

import requests
from bs4 import BeautifulSoup, Tag

NTU_COURSE_URL = "https://wis.ntu.edu.sg/webexe/owa/AUS_SUBJ_CONT.main_display1"
COURSE_CODE_PATTERN = re.compile(r"^[A-Z]{2,4}\d{4}[A-Z]?$")

@dataclass
class ScrapedCourse:
    code: str
    title: str | None
    no_of_credits: str | None
    mutually_exclusive: list[str]
    description: str | None

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

def scrape_courses(acadsem: str, course_yr: str) -> list[ScrapedCourse]:
    response_text = fetch_course_page(acadsem=acadsem, course_yr=course_yr)
    return parse_courses(response_text)

def fetch_course_page(acadsem: str, course_yr: str) -> str:
    acad, semester = acadsem.split("_", maxsplit=1)

    payload = {
        "acadsem": acadsem,
        "r_course_yr": course_yr,
        "boption": "CLoad",
        "acad": acad,
        "semester": semester,
    }

    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
            "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36"
        ),
    }

    response = requests.post(
        NTU_COURSE_URL,
        data=payload,
        headers=headers,
        timeout=20,
    )
    response.raise_for_status()
    return response.text

def parse_courses(html: str) -> list[ScrapedCourse]:
    soup = BeautifulSoup(html, "html.parser")
    course_fonts = soup.find_all("font", color="#0000FF")

    courses: list[ScrapedCourse] = []
    seen_codes: set[str] = set()

    for font in course_fonts:
        course_code = _clean_text(font.get_text())

        if not COURSE_CODE_PATTERN.match(course_code):
            continue

        if course_code in seen_codes:
            continue

        seen_codes.add(course_code)
        course_table = font.find_parent("table")

        courses.append(
            ScrapedCourse(
                code=course_code,
                title=_extract_title(course_code, course_table),
                description=_extract_description(course_table),
                no_of_credits=_extract_no_of_credits(course_table),
                mutually_exclusive=_extract_mutually_exclusive(course_table),
            )
        )

    return courses

def _extract_title(course_code: str, course_table: Tag | None) -> str | None:
    if course_table is None:
        return None

    row = course_table.find("tr")
    if row is None:
        return None

    cells = [_clean_text(cell.get_text(" ")) for cell in row.find_all("td")]
    cells = [cell for cell in cells if cell]

    for index, cell in enumerate(cells):
        if cell == course_code and index + 1 < len(cells):
            title = cells[index + 1]
            return title or None

    row_text = _clean_text(row.get_text(" "))
    title = row_text.replace(course_code, "", 1).strip(" -:")
    return title or None

def _extract_description(course_table: Tag | None) -> str | None:
    if course_table is None:
        return None

    for cell in course_table.find_all("td"):
        colspan = cell.get("colspan")
        text = _clean_text(cell.get_text(" "))

        if colspan == "3" and text and not _is_metadata_label(text):
            return text

    return None


def _extract_no_of_credits(course_table: Tag | None) -> str | None:
    if course_table is None:
        return None

    first_row = course_table.find("tr")
    if first_row is None:
        return None

    for cell in first_row.find_all("td"):
        text = _clean_text(cell.get_text(" "))
        match = re.search(r"\b\d+(?:\.\d+)?\s*AU\b", text, re.IGNORECASE)
        if match:
            return match.group(0)

    return None


def _extract_mutually_exclusive(course_table: Tag | None) -> list[str]:
    if course_table is None:
        return []

    label = course_table.find(
        "font",
        string=lambda value: value is not None and "Mutually exclusive with" in value,
    )
    if label is None:
        return []

    label_cell = label.find_parent("td")
    if label_cell is None:
        return []

    value_cell = label_cell.find_next_sibling("td")
    if value_cell is None:
        return []

    value_text = _clean_text(value_cell.get_text(" "))
    if not value_text:
        return []

    return [code.strip() for code in value_text.split(",") if code.strip()]


def _is_metadata_label(text: str) -> bool:
    metadata_labels = (
        "Mutually exclusive with:",
        "Not available to all Programme with:",
    )
    return text in metadata_labels


def _clean_text(value: str) -> str:
    return " ".join(value.split())


def _clean_text(value: str) -> str:
    return " ".join(value.split())
