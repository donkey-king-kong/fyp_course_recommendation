import logging
import re
from collections import defaultdict
from typing import Any, Optional

import fitz

from backend.schemas.curriculum import (
    CurriculumCourse,
    CurriculumEdge,
    CurriculumGuideResponse,
    CurriculumSemester,
    StandingRequirement,
)

logger = logging.getLogger(__name__)

COURSE_OR_SLOT_PATTERN = re.compile(r"^(?:[A-Z]{2,4}\d{4}|[A-Z]{2}\dxxx|BDE)$")
COURSE_CODE_PATTERN = re.compile(r"\b[A-Z]{2,4}\d{4}\b")
COHORT_PATTERN = re.compile(r"\bAY\s*(\d{4})[‐‑‒–—-](\d{2})\b", re.IGNORECASE)
SEMESTER_PATTERN = re.compile(r"\bYEAR\s+(\d)\s+SEMESTER\s+(\d)\b", re.IGNORECASE)

# Main service entry point used by the upload route.
# It keeps the parser output close to the existing roadmap shape for frontend reuse.
def extract_curriculum_guide(file_content: bytes) -> CurriculumGuideResponse:
    words = extract_words_from_pdf(file_content)
    text = extract_text_from_pdf(file_content)
    rows = parse_curriculum_rows(words)

    if not rows:
        raise ValueError("No curriculum guide rows could be parsed from this PDF.")

    nodes = build_curriculum_courses(rows)
    semesters = build_semesters(nodes)
    edges = build_prerequisite_edges(nodes)

    return CurriculumGuideResponse(
        major=extract_major(text),
        cohort=extract_cohort(text),
        totalAcademicUnits=extract_total_academic_units(text, nodes),
        semesters=semesters,
        standingRequirements=build_standing_requirements(semesters),
        nodes=nodes,
        edges=edges,
    )

# Plain text is useful for document-level metadata such as major, cohort, and total AU.
def extract_text_from_pdf(file_content: bytes) -> str:
    with fitz.open(stream=file_content, filetype="pdf") as document:
        return "\n".join(page.get_text("text") for page in document)

# Positioned words are needed because the curriculum guide is table-like.
# The extracted plain text order is not reliable enough to rebuild rows.
def extract_words_from_pdf(file_content: bytes) -> list[dict[str, Any]]:
    words: list[dict[str, Any]] = []

    with fitz.open(stream=file_content, filetype="pdf") as document:
        for page_number, page in enumerate(document):
            for word in page.get_text("words"):
                x0, y0, x1, y1, text, block_no, line_no, word_no = word
                words.append(
                    {
                        "page": page_number,
                        "x0": x0,
                        "y0": y0,
                        "x1": x1,
                        "y1": y1,
                        "text": text,
                        "block_no": block_no,
                        "line_no": line_no,
                        "word_no": word_no,
                    }
                )

    logger.info("Extracted %s PDF word(s) from curriculum guide.", len(words))
    return words

# Convert raw positioned words into candidate curriculum rows.
# Column positions are inferred from table headers so similar NTU guide variants can be parsed.
def parse_curriculum_rows(words: list[dict[str, Any]]) -> list[dict[str, Any]]:
    lines = group_words_into_lines(words)
    semester_headers = find_semester_headers(lines)
    column_headers = find_curriculum_column_headers(lines)
    section_end = find_first_curriculum_section_end(lines)
    rows: list[dict[str, Any]] = []

    for line in lines:
        if is_after_position(line, section_end):
            continue

        column_header = find_current_column_header(line, column_headers)
        course_word = find_main_schedule_course_word(line["words"], column_header)

        if course_word is None:
            continue

        semester_header = find_current_semester_header(line, semester_headers)

        if semester_header is None:
            continue

        row = parse_curriculum_row(line["words"], course_word, semester_header, column_header)

        if row is not None:
            rows.append(row)

    logger.info("Parsed %s curriculum guide row(s).", len(rows))
    return rows

# Some guides bundle multiple curriculum variants; use the first section until selection UI exists.
def find_first_curriculum_section_end(lines: list[dict[str, Any]]) -> Optional[dict[str, Any]]:
    curriculum_starts = [
        line
        for line in lines
        if build_line_text(line["words"]).upper().startswith("CURRICULUM FOR")
    ]

    if len(curriculum_starts) < 2:
        return None

    return curriculum_starts[1]

def is_after_position(line: dict[str, Any], position: Optional[dict[str, Any]]) -> bool:
    if position is None:
        return False

    return (line["page"], line["y0"]) >= (position["page"], position["y0"])

# PyMuPDF can give slightly different y-values for words on the same visual row.
# Group with a small tolerance so course codes, titles, AU, and prerequisites stay together.
def group_words_into_lines(words: list[dict[str, Any]]) -> list[dict[str, Any]]:
    lines: list[dict[str, Any]] = []
    sorted_words = sorted(words, key=lambda word: (word["page"], word["y0"], word["x0"]))

    for word in sorted_words:
        current_line = next(
            (
                line
                for line in reversed(lines)
                if line["page"] == word["page"] and abs(line["y0"] - word["y0"]) <= 2
            ),
            None,
        )

        if current_line is None:
            lines.append({"page": word["page"], "y0": word["y0"], "words": [word]})
            continue

        current_line["words"].append(word)
        current_line["y0"] = min(current_line["y0"], word["y0"])

    for line in lines:
        line["words"] = sorted(line["words"], key=lambda word: word["x0"])

    return sorted(lines, key=lambda line: (line["page"], line["y0"]))

# Full curriculum tables expose the column positions that differ across guide PDFs.
def find_curriculum_column_headers(lines: list[dict[str, Any]]) -> list[dict[str, Any]]:
    column_headers: list[dict[str, Any]] = []

    for line in lines:
        words = line["words"]
        line_text = build_line_text(words)

        if not all(label in line_text for label in ["Course Code", "Course Title", "Type", "AU"]):
            continue

        code_word = find_header_word_pair_start(words, "Course", "Code")
        title_word = find_header_word_pair_start(words, "Course", "Title")
        type_word = find_header_word(words, "Type")
        au_word = find_header_word(words, "AU")
        prerequisite_word = find_header_word(words, "Pre-requisite")

        if None in [code_word, title_word, type_word, au_word]:
            continue

        column_headers.append(
            {
                "page": line["page"],
                "y0": line["y0"],
                "code_x": code_word["x0"],
                "title_x": title_word["x0"],
                "type_x": type_word["x0"],
                "au_x": au_word["x0"],
                "prerequisite_x": prerequisite_word["x0"] if prerequisite_word else au_word["x1"],
            }
        )

    return column_headers

def find_header_word(words: list[dict[str, Any]], label: str) -> Optional[dict[str, Any]]:
    return next((word for word in words if str(word["text"]).strip() == label), None)

def find_header_word_pair_start(
    words: list[dict[str, Any]],
    first_label: str,
    second_label: str,
) -> Optional[dict[str, Any]]:
    for index, word in enumerate(words[:-1]):
        current_text = str(word["text"]).strip()
        next_text = str(words[index + 1]["text"]).strip()

        if current_text == first_label and next_text == second_label:
            return word

    return None

# Uses the nearest full curriculum table header above the row on the same page.
def find_current_column_header(
    line: dict[str, Any],
    column_headers: list[dict[str, Any]],
) -> Optional[dict[str, Any]]:
    matching_headers = [
        header
        for header in column_headers
        if header["page"] == line["page"] and header["y0"] < line["y0"]
    ]

    return max(matching_headers, key=lambda header: header["y0"], default=None)

# Semester headers define which year/semester each following curriculum row belongs to.
def find_semester_headers(lines: list[dict[str, Any]]) -> list[dict[str, Any]]:
    semester_headers: list[dict[str, Any]] = []

    for line in lines:
        line_text = build_line_text(line["words"])
        semester_match = SEMESTER_PATTERN.search(line_text)

        if semester_match:
            semester_headers.append(
                {
                    "page": line["page"],
                    "y0": line["y0"],
                    "year": int(semester_match.group(1)),
                    "semester": int(semester_match.group(2)),
                }
            )

    return semester_headers

# Joins words back into a readable line for regex matching.
def build_line_text(words: list[dict[str, Any]]) -> str:
    return " ".join(str(word["text"]).strip() for word in words if str(word["text"]).strip())

# Finds the row anchor: either a real module code like SC1003 or a choice slot like BDE.
def find_main_schedule_course_word(
    words: list[dict[str, Any]],
    column_header: Optional[dict[str, Any]] = None,
) -> Optional[dict[str, Any]]:
    for word in words:
        text = str(word["text"]).strip()

        if not COURSE_OR_SLOT_PATTERN.fullmatch(text):
            continue

        if column_header is not None:
            code_column_limit = (column_header["code_x"] + column_header["title_x"]) / 2
            is_in_code_column = word["x0"] <= code_column_limit
            is_bde_type = text == "BDE" and abs(word["x0"] - column_header["type_x"]) <= 40

            if is_in_code_column or is_bde_type:
                return word

            continue

        # Main curriculum rows place real course codes in the left code column.
        if word["x0"] < 250:
            return word

        # BDE rows have no separate course-code column, so the BDE type acts as the slot code.
        if text == "BDE" and 300 <= word["x0"] <= 620:
            return word

    return None

# Uses the nearest semester header above the row on the same page.
def find_current_semester_header(
    line: dict[str, Any], semester_headers: list[dict[str, Any]]
) -> Optional[dict[str, Any]]:
    matching_headers = [
        header
        for header in semester_headers
        if header["page"] == line["page"] and header["y0"] < line["y0"]
    ]

    return max(matching_headers, key=lambda header: header["y0"], default=None)

# Pulls one visual table row into the normalized course/slot fields.
def parse_curriculum_row(
    words: list[dict[str, Any]],
    course_word: dict[str, Any],
    semester_header: dict[str, Any],
    column_header: Optional[dict[str, Any]] = None,
) -> Optional[dict[str, Any]]:
    code = str(course_word["text"]).strip()
    course_type_word = find_course_type_word(words, code, column_header)
    academic_unit_word = find_academic_unit_word(words, course_type_word, column_header)

    if academic_unit_word is None:
        return None

    course_type = get_course_type_from_word(course_type_word, code)
    title = find_course_title(words, course_word, course_type_word, column_header)
    prerequisite_text = find_prerequisite_text(words, academic_unit_word, column_header)

    return {
        "code": code,
        "title": normalize_course_title(code, course_type, title),
        "type": course_type,
        "year": semester_header["year"],
        "semester": semester_header["semester"],
        "academic_units": int(str(academic_unit_word["text"])),
        "prerequisite_text": prerequisite_text,
        "prerequisites": parse_prerequisites(prerequisite_text),
        "is_choice_slot": is_choice_slot(code, course_type, title),
    }

# Course type includes values like Core, F-Core, C-Core, MPE-1, MPE-2, and BDE.
def find_course_type_word(
    words: list[dict[str, Any]],
    code: str,
    column_header: Optional[dict[str, Any]] = None,
) -> Optional[dict[str, Any]]:
    if code == "BDE":
        return next(
            (
                word
                for word in words
                if (
                    str(word["text"]).strip() == "BDE" and
                    is_near_column(word, column_header, "type_x", fallback_min_x=300)
                )
            ),
            None,
        )

    valid_types = {"Core", "F-Core", "C-Core", "MPE-1", "MPE-2", "Business"}

    return next(
        (
            word
            for word in words
            if (
                str(word["text"]).strip() in valid_types and
                is_near_column(word, column_header, "type_x", fallback_min_x=0)
            )
        ),
        None,
    )

def is_near_column(
    word: dict[str, Any],
    column_header: Optional[dict[str, Any]],
    column_key: str,
    fallback_min_x: float,
) -> bool:
    if column_header is None:
        return word["x0"] >= fallback_min_x

    return abs(word["x0"] - column_header[column_key]) <= 45

# AU is the first numeric value after the detected course type in supported guide layouts.
def find_academic_unit_word(
    words: list[dict[str, Any]],
    course_type_word: Optional[dict[str, Any]],
    column_header: Optional[dict[str, Any]] = None,
) -> Optional[dict[str, Any]]:
    au_words = [
        word
        for word in words
        if (
            re.fullmatch(r"\d+", str(word["text"])) and
            (
                (
                    column_header is not None and
                    abs(word["x0"] - column_header["au_x"]) <= 45
                ) or (
                    column_header is None and
                    course_type_word is not None and
                    word["x0"] > course_type_word["x1"]
                )
            )
        )
    ]

    if au_words:
        return min(au_words, key=lambda word: word["x0"])

    return next(
        (
            word
            for word in words
            if 350 <= word["x0"] <= 720 and re.fullmatch(r"\d+", str(word["text"]))
        ),
        None,
    )

def get_course_type_from_word(course_type_word: Optional[dict[str, Any]], code: str) -> str:
    if code == "BDE":
        return "BDE"

    return str(course_type_word["text"]).strip() if course_type_word is not None else ""

# Kept for older call sites and simple tests that only need the parsed AU value.
def find_academic_units(words: list[dict[str, Any]]) -> Optional[int]:
    au_word = find_academic_unit_word(words, find_course_type_word(words, ""), None)

    return int(str(au_word["text"])) if au_word is not None else None

# Course types are detected by label text, not only x-position, because NTU guides vary in width.
def find_course_type(words: list[dict[str, Any]], code: str) -> str:
    return get_course_type_from_word(find_course_type_word(words, code), code)

# Course titles sit between the code column and type column; BDE rows use the text before `BDE`.
def find_course_title(
    words: list[dict[str, Any]],
    course_word: Optional[dict[str, Any]] = None,
    course_type_word: Optional[dict[str, Any]] = None,
    column_header: Optional[dict[str, Any]] = None,
) -> str:
    if course_type_word is None:
        course_type_word = find_course_type_word(words, "")

    if course_type_word is None:
        title_words = [
            str(word["text"]).strip()
            for word in words
            if 180 <= word["x0"] < 540 and str(word["text"]).strip()
        ]

        return " ".join(title_words)

    is_bde_slot = course_word is not None and str(course_word["text"]).strip() == "BDE"
    title_start = 100 if is_bde_slot else (course_word["x1"] if course_word is not None else 100) + 1
    title_words = [
        str(word["text"]).strip()
        for word in words
        if title_start <= word["x0"] < course_type_word["x0"] and str(word["text"]).strip()
    ]

    return " ".join(title_words)

def normalize_course_title(code: str, course_type: str, title: str) -> str:
    if "xxx" in code and "MPE" in course_type:
        return "Major Prescribed Elective"

    return title or default_title_for_slot(code, course_type)


# Prerequisite text starts in the header's prerequisite column when available.
def find_prerequisite_text(
    words: list[dict[str, Any]],
    academic_unit_word: Optional[dict[str, Any]] = None,
    column_header: Optional[dict[str, Any]] = None,
) -> str:
    if column_header is not None:
        prerequisite_words = [
            str(word["text"]).strip()
            for word in words
            if word["x0"] >= column_header["prerequisite_x"] - 25 and str(word["text"]).strip()
        ]

        return " ".join(prerequisite_words)

    if academic_unit_word is not None:
        prerequisite_words = [
            str(word["text"]).strip()
            for word in words
            if word["x0"] > academic_unit_word["x1"] and str(word["text"]).strip()
        ]

        return " ".join(prerequisite_words)

    prerequisite_words = [
        str(word["text"]).strip()
        for word in words
        if word["x0"] >= 740 and str(word["text"]).strip()
    ]

    return " ".join(prerequisite_words)

# Some choice-slot rows need a fallback label because the PDF does not always expose a title cleanly.
def default_title_for_slot(code: str, course_type: str) -> str:
    if code == "BDE":
        return "Broadening and Deepening Electives"

    if "MPE" in course_type:
        return "Major Prescribed Elective"

    return ""

# Keep real module prerequisites as course codes, while preserving standing requirements as text.
def parse_prerequisites(prerequisite_text: str) -> list[str]:
    cleaned_text = prerequisite_text.strip()

    if not cleaned_text or cleaned_text.lower() == "nil":
        return []

    course_codes = COURSE_CODE_PATTERN.findall(cleaned_text)

    if course_codes:
        return course_codes

    return [cleaned_text]

# Choice slots are placeholders that students can fill later with recommended real modules.
def is_choice_slot(code: str, course_type: str, title: str) -> bool:
    normalized_title = title.upper()

    return (
        "XXX" in code.upper()
        or code == "BDE"
        or course_type == "BDE"
        or "CHOOSE" in normalized_title
    )

# Builds stable frontend IDs while allowing repeated placeholders such as SC3xxx and BDE.
def build_curriculum_courses(rows: list[dict[str, Any]]) -> list[CurriculumCourse]:
    nodes: list[CurriculumCourse] = []
    code_counts: dict[str, int] = defaultdict(int)

    for row in rows:
        code_counts[row["code"]] += 1
        course_id = (
            f"y{row['year']}s{row['semester']}-"
            f"{row['code'].lower()}-{code_counts[row['code']]}"
        )
        nodes.append(
            CurriculumCourse(
                id=course_id,
                courseCode=row["code"],
                title=row["title"],
                type=row["type"],
                year=row["year"],
                semester=row["semester"],
                academicUnits=row["academic_units"],
                prerequisites=row["prerequisites"],
                prerequisiteText=row["prerequisite_text"],
                isChoiceSlot=row["is_choice_slot"],
            )
        )

    return nodes

# Groups flat parsed courses back into semester sections for the roadmap UI.
def build_semesters(nodes: list[CurriculumCourse]) -> list[CurriculumSemester]:
    semester_courses: dict[tuple[int, int], list[CurriculumCourse]] = defaultdict(list)

    for node in nodes:
        semester_courses[(node.year, node.semester)].append(node)

    return [
        CurriculumSemester(
            year=year,
            semester=semester,
            totalAcademicUnits=sum(course.academicUnits for course in courses),
            courses=courses,
        )
        for (year, semester), courses in sorted(semester_courses.items())
    ]

# Creates prerequisite arrows only when a prerequisite exists in the parsed curriculum.
def build_standing_requirements(semesters: list[CurriculumSemester]) -> list[StandingRequirement]:
    academic_units_by_year: dict[int, int] = defaultdict(int)

    for semester in semesters:
        academic_units_by_year[semester.year] += semester.totalAcademicUnits

    requirements: list[StandingRequirement] = []

    for standing_year in [2, 3, 4]:
        included_years = list(range(1, standing_year))
        minimum_academic_units = sum(academic_units_by_year[year] for year in included_years)

        if minimum_academic_units == 0:
            continue

        requirements.append(
            StandingRequirement(
                standingYear=standing_year,
                minimumAcademicUnits=minimum_academic_units,
                includedYears=included_years,
            )
        )

    return requirements


def build_prerequisite_edges(nodes: list[CurriculumCourse]) -> list[CurriculumEdge]:
    course_ids_by_code = {node.courseCode: node.id for node in nodes if "xxx" not in node.courseCode}
    edges: list[CurriculumEdge] = []

    for node in nodes:
        for prerequisite in node.prerequisites:
            source_id = course_ids_by_code.get(prerequisite)

            if source_id:
                edges.append(CurriculumEdge(source=source_id, target=node.id))

    return edges

# The first parser supports the uploaded CSC guide before generalizing to other majors.
def extract_major(text: str) -> str:
    if "COMPUTER SCIENCE" in text.upper():
        return "Computer Science"

    return "Unknown"

# Extract the cohort label from the guide title, for example AY2023-24.
def extract_cohort(text: str) -> str:
    cohort_match = COHORT_PATTERN.search(text)

    if cohort_match:
        return f"AY{cohort_match.group(1)}-{cohort_match.group(2)}"

    return "Unknown"

# Prefer the guide's total AU when known; otherwise fall back to summing parsed rows.
def extract_total_academic_units(text: str, nodes: list[CurriculumCourse]) -> int:
    if "135" in text:
        return 135

    return sum(node.academicUnits for node in nodes)
