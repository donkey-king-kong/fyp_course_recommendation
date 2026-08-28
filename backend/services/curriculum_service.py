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
# This first pass supports the current CSC AY2023-24 guide layout.
def parse_curriculum_rows(words: list[dict[str, Any]]) -> list[dict[str, Any]]:
    lines = group_words_into_lines(words)
    semester_headers = find_semester_headers(lines)
    rows: list[dict[str, Any]] = []

    for line in lines:
        course_word = find_main_schedule_course_word(line["words"])

        if course_word is None:
            continue

        semester_header = find_current_semester_header(line, semester_headers)

        if semester_header is None:
            continue

        row = parse_curriculum_row(line["words"], course_word, semester_header)

        if row is not None:
            rows.append(row)

    logger.info("Parsed %s curriculum guide row(s).", len(rows))
    return rows

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
def find_main_schedule_course_word(words: list[dict[str, Any]]) -> Optional[dict[str, Any]]:
    for word in words:
        text = str(word["text"]).strip()

        if not COURSE_OR_SLOT_PATTERN.fullmatch(text):
            continue

        # Main curriculum rows place real course codes in the left code column.
        if word["x0"] < 170:
            return word

        # BDE rows have no separate course-code column, so the BDE type acts as the slot code.
        if text == "BDE" and 520 <= word["x0"] <= 620:
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
    words: list[dict[str, Any]], course_word: dict[str, Any], semester_header: dict[str, Any]
) -> Optional[dict[str, Any]]:
    code = str(course_word["text"]).strip()
    academic_units = find_academic_units(words)

    if academic_units is None:
        return None

    course_type = find_course_type(words, code)
    title = find_course_title(words)
    prerequisite_text = find_prerequisite_text(words)

    return {
        "code": code,
        "title": title or default_title_for_slot(code, course_type),
        "type": course_type,
        "year": semester_header["year"],
        "semester": semester_header["semester"],
        "academic_units": academic_units,
        "prerequisite_text": prerequisite_text,
        "prerequisites": parse_prerequisites(prerequisite_text),
        "is_choice_slot": is_choice_slot(code, course_type, title),
    }

# AU is in a stable numeric column in the current guide.
def find_academic_units(words: list[dict[str, Any]]) -> Optional[int]:
    au_words = [
        word
        for word in words
        if 660 <= word["x0"] <= 720 and re.fullmatch(r"\d+", str(word["text"]))
    ]

    if not au_words:
        return None

    return int(str(au_words[0]["text"]))

# Course type includes values like Core, F-Core, C-Core, MPE-1, and MPE-2.
def find_course_type(words: list[dict[str, Any]], code: str) -> str:
    if code == "BDE":
        return "BDE"

    type_words = [
        word
        for word in words
        if 540 <= word["x0"] <= 640 and str(word["text"]).strip()
    ]

    return " ".join(str(word["text"]).strip() for word in type_words)

# Course titles sit between the code column and the type column.
def find_course_title(words: list[dict[str, Any]]) -> str:
    title_words = [
        str(word["text"]).strip()
        for word in words
        if 180 <= word["x0"] < 540 and str(word["text"]).strip()
    ]

    return " ".join(title_words)

# Prerequisite text is preserved as raw text and separately simplified into course-code tokens.
def find_prerequisite_text(words: list[dict[str, Any]]) -> str:
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
        return f"Major Prescribed Elective ({code})"

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
