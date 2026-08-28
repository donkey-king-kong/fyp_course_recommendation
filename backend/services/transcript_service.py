import logging
import re
from typing import Any, Optional

import fitz

from backend.schemas.transcript import TranscriptCourse, TranscriptUploadResponse
from backend.services.roadmap_service import get_csc_roadmap

logger = logging.getLogger(__name__)

# Matches NTU-style module codes such as SC1003, MH1810, CC0001, etc
COURSE_CODE_PATTERN = re.compile(r"\b[A-Z]{2,4}\d{4}\b")
TERM_HEADER_PATTERN = re.compile(
    r"(?P<academic_year>\d{4}\s*-\s*\d{4})\s+SEMESTER\s+(?P<semester>\d+)",
    re.IGNORECASE,
)

# Grades in this set should be treated as completed modules
# EX = exempted and TC = transfer credit; both count as completed
COMPLETED_GRADES = {
    "A+",
    "A",
    "A-",
    "B+",
    "B",
    "B-",
    "C+",
    "C",
    "C-",
    "D+",
    "D",
    "EX",
    "TC",
}

# Fallback pattern for cases where PDF text extraction keeps one whole course row together
TRANSCRIPT_ROW_PATTERN = re.compile(
    r"^(?P<code>[A-Z]{2,4}\d{4})\s+"
    r"(?P<title>.+?)\s+"
    r"(?P<academic_units>\d+\.\d)\s+"
    r"(?P<grade>A\+|A-|A|B\+|B-|B|C\+|C-|C|D\+|D|EX|TC)"
    r"(?:\s+(?P<grade_point>\d+\.\d{2}))?$"
)
TOTAL_AU_EARNED_PATTERN = re.compile(
    r"TOTAL\s+ACADEMIC\s+UNITS\s+EARNED\s*:?\s*(?P<total>\d+(?:\.\d+)?)",
    re.IGNORECASE,
)

def extract_text_from_pdf(file_content: bytes) -> str:
    # Plain text extraction is used as a fallback if word-position parsing finds no rows
    with fitz.open(stream=file_content, filetype="pdf") as document:
        return "\n".join(page.get_text("text") for page in document)

# Pull individual words and their positions from the transcript
def extract_words_from_pdf(file_content: bytes) -> list[dict[str, Any]]:
    words: list[dict[str, Any]] = []

    with fitz.open(stream=file_content, filetype="pdf") as document:
        for page_number, page in enumerate(document):
            # "words" returns each word plus its PDF coordinates
            # Coordinates help rebuild table rows from Code/Course/AU/Grade columns
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

    logger.info("Extracted %s PDF word(s) from transcript.", len(words))
    return words

def normalize_line(line: str) -> str:
    # Make extracted text easier to compare by removing extra spaces and casing differences
    return " ".join(line.strip().upper().split())

def extract_total_academic_units_earned(transcript_text: str) -> Optional[float]:
    normalized_text = normalize_line(transcript_text)
    total_match = TOTAL_AU_EARNED_PATTERN.search(normalized_text)

    if total_match:
        return float(total_match.group("total"))

    return None

def parse_transcript_rows(transcript_text: str) -> list[dict[str, Any]]:
    # Fallback parser for PDFs where each course row is extracted as readable text
    lines = [normalize_line(line) for line in transcript_text.splitlines()]
    rows: list[dict[str, Any]] = []
    current_row = ""
    current_term: dict[str, Any] = {}
    study_year_by_academic_year: dict[str, int] = {}

    for line in lines:
        if not line:
            continue

        term_match = TERM_HEADER_PATTERN.search(line)

        if term_match:
            academic_year = normalize_academic_year(term_match.group("academic_year"))
            study_year_by_academic_year.setdefault(
                academic_year,
                len(study_year_by_academic_year) + 1,
            )
            current_term = {
                "academic_year": academic_year,
                "transcript_semester": int(term_match.group("semester")),
                "study_year": study_year_by_academic_year[academic_year],
            }
            current_row = ""
            continue

        # New course code = new row
        if COURSE_CODE_PATTERN.match(line):
            current_row = line
        elif current_row:
            # Course names may wrap onto the next extracted PDF text line
            current_row = f"{current_row} {line}"
        else:
            continue

        row_match = TRANSCRIPT_ROW_PATTERN.match(current_row)

        if row_match:
            rows.append({**row_match.groupdict(), **current_term})
            current_row = ""

    return rows

# Take positioned words extracted from PDF and group into course rows
# Rebuild table rows
def parse_transcript_rows_from_words(words: list[dict[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    # Process words in visual reading order: page, top-to-bottom, then left-to-right
    sorted_words = sorted(words, key=lambda word: (word["page"], word["y0"], word["x0"]))
    term_headers = extract_term_headers_from_words(sorted_words)
    study_year_by_academic_year = build_study_year_map(term_headers)
    # Every course row starts with a module code in the first column
    code_words = [
        word
        for word in sorted_words
        if COURSE_CODE_PATTERN.fullmatch(str(word["text"]).upper())
    ]

    for code_word in code_words:
        next_code_word = find_next_code_in_same_column(code_word, code_words)
        page = code_word["page"]
        # Use the current course code and the next course code to estimate row boundaries
        row_y_start = code_word["y0"] - 2
        row_y_end = (
            next_code_word["y0"] - 2
            if next_code_word and next_code_word["page"] == page
            else code_word["y0"] + 24
        )
        column_x_start, column_x_end = get_course_column_bounds(code_word, code_words)
        row_words = [
            word
            for word in sorted_words
            if word["page"] == page
            and row_y_start <= word["y0"] < row_y_end
            and column_x_start <= word["x0"] < column_x_end
        ]

        # Parse the words within this row into code/title/AU/grade/grade point
        row = parse_course_row_from_words(code_word, row_words)
        term_header = find_term_header_for_course(
            code_word,
            term_headers,
            column_x_start,
            column_x_end,
        )

        if term_header:
            row["academic_year"] = term_header["academic_year"]
            row["transcript_semester"] = term_header["transcript_semester"]
            row["study_year"] = study_year_by_academic_year[term_header["academic_year"]]

        rows.append(row)

    logger.info("Parsed %s possible transcript course row(s).", len(rows))
    for row in rows:
        logger.info(
            "Parsed row: code=%s, term=%s S%s, study_year=%s, au=%s, grade=%s, grade_point=%s",
            row["code"],
            row["academic_year"],
            row["transcript_semester"],
            row["study_year"],
            row["academic_units"],
            row["grade"],
            row["grade_point"],
        )

    return rows

def normalize_academic_year(academic_year: str) -> str:
    return academic_year.replace(" ", "")

# Find transcript term headings such as "2024-2025 SEMESTER 2" in either one or two columns.
def extract_term_headers_from_words(words: list[dict[str, Any]]) -> list[dict[str, Any]]:
    lines_by_key: dict[tuple[int, int, int], list[dict[str, Any]]] = {}

    for word in words:
        key = (word["page"], word["block_no"], word["line_no"])
        lines_by_key.setdefault(key, []).append(word)

    term_headers: list[dict[str, Any]] = []

    for line_words in lines_by_key.values():
        ordered_line_words = sorted(line_words, key=lambda word: word["x0"])
        line_text = normalize_line(" ".join(str(word["text"]) for word in ordered_line_words))
        term_match = TERM_HEADER_PATTERN.search(line_text)

        if not term_match:
            continue

        term_headers.append(
            {
                "page": ordered_line_words[0]["page"],
                "x0": min(word["x0"] for word in ordered_line_words),
                "x1": max(word["x1"] for word in ordered_line_words),
                "y0": min(word["y0"] for word in ordered_line_words),
                "academic_year": normalize_academic_year(term_match.group("academic_year")),
                "transcript_semester": int(term_match.group("semester")),
            }
        )

    return sorted(term_headers, key=get_transcript_visual_order_key)

def get_transcript_visual_order_key(term_header: dict[str, Any]) -> tuple[int, int, float]:
    # Transcript tables read down the left column first, then down the right column.
    column_index = 0 if term_header["x0"] < 300 else 1

    return (term_header["page"], column_index, term_header["y0"])

def build_study_year_map(term_headers: list[dict[str, Any]]) -> dict[str, int]:
    study_year_by_academic_year: dict[str, int] = {}

    for term_header in term_headers:
        academic_year = term_header["academic_year"]
        study_year_by_academic_year.setdefault(
            academic_year,
            len(study_year_by_academic_year) + 1,
        )

    return study_year_by_academic_year

def find_term_header_for_course(
    code_word: dict[str, Any],
    term_headers: list[dict[str, Any]],
    column_x_start: float,
    column_x_end: float,
) -> Optional[dict[str, Any]]:
    same_column_headers = [
        term_header
        for term_header in term_headers
        if term_header["page"] == code_word["page"]
        and term_header["y0"] <= code_word["y0"]
        and column_x_start <= term_header["x0"] < column_x_end
    ]

    if same_column_headers:
        return max(same_column_headers, key=lambda term_header: term_header["y0"])

    same_page_headers = [
        term_header
        for term_header in term_headers
        if term_header["page"] == code_word["page"] and term_header["y0"] <= code_word["y0"]
    ]

    return max(same_page_headers, key=lambda term_header: term_header["y0"], default=None)

# Finds the next course code below the current code in the same transcript column.
def find_next_code_in_same_column(
    code_word: dict[str, Any], code_words: list[dict[str, Any]]
) -> Optional[dict[str, Any]]:
    same_column_codes = [
        word
        for word in code_words
        if word["page"] == code_word["page"]
        and word["y0"] > code_word["y0"]
        and abs(word["x0"] - code_word["x0"]) < 120
    ]

    return min(same_column_codes, key=lambda word: word["y0"], default=None)

# Keeps row parsing inside the current left or right transcript table.
def get_course_column_bounds(
    code_word: dict[str, Any], code_words: list[dict[str, Any]]
) -> tuple[float, float]:
    column_x_start = code_word["x0"] - 10
    next_column_code = min(
        (
            word
            for word in code_words
            if word["page"] == code_word["page"] and word["x0"] > code_word["x0"] + 120
        ),
        key=lambda word: word["x0"],
        default=None,
    )
    column_x_end = next_column_code["x0"] - 10 if next_column_code else float("inf")

    return column_x_start, column_x_end

def parse_course_row_from_words(
    code_word: dict[str, Any], row_words: list[dict[str, Any]]
) -> dict[str, Any]:
    code = str(code_word["text"]).upper()
    # Ignore anything to the left of the module code
    # Course details are on the right
    words_after_code = [
        word for word in row_words if word["x0"] > code_word["x1"] and str(word["text"]).strip()
    ]
    grade_word = next(
        (
            word
            for word in words_after_code
            if str(word["text"]).upper() in COMPLETED_GRADES
        ),
        None,
    )
    academic_unit_word = None

    if grade_word:
        # The AU value is the closest decimal number before the grade column
        academic_unit_word = max(
            (
                word
                for word in words_after_code
                if word["x0"] < grade_word["x0"]
                and re.fullmatch(r"\d+\.\d", str(word["text"]))
            ),
            key=lambda word: word["x0"],
            default=None,
        )

    title_words = [
        str(word["text"])
        for word in words_after_code
        if (
            # Course title sits between the module code and the AU/grade columns
            (academic_unit_word and word["x0"] < academic_unit_word["x0"])
            or (academic_unit_word is None and (grade_word is None or word["x0"] < grade_word["x0"]))
        )
    ]
    # Letter grades have a grade point after the grade
    # EX no grade point
    grade_point_word = next(
        (
            word
            for word in words_after_code
            if grade_word
            and word["x0"] > grade_word["x1"]
            and re.fullmatch(r"\d+\.\d{2}", str(word["text"]))
        ),
        None,
    )

    return {
        "code": code,
        "title": normalize_line(" ".join(title_words)),
        "academic_units": str(academic_unit_word["text"]) if academic_unit_word else "0.0",
        "grade": str(grade_word["text"]).upper() if grade_word else "",
        "grade_point": str(grade_point_word["text"]) if grade_point_word else None,
        "academic_year": None,
        "transcript_semester": None,
        "study_year": None,
    }

def extract_completed_courses(file_content: bytes) -> TranscriptUploadResponse:
    # Main entry point used by the upload route
    transcript_text = extract_text_from_pdf(file_content)
    transcript_rows = parse_transcript_rows_from_words(extract_words_from_pdf(file_content))

    if not transcript_rows:
        logger.info("Word-position parsing found no rows; falling back to line-based parsing.")
        transcript_rows = parse_transcript_rows(transcript_text)
    roadmap = get_csc_roadmap()
    # Build a quick lookup so transcript course codes can be matched to roadmap nodes.
    roadmap_courses_by_code = {course.courseCode: course for course in roadmap.nodes}

    completed_courses: list[TranscriptCourse] = []
    completed_transcript_courses: list[TranscriptCourse] = []
    unmatched_course_codes: list[str] = []
    # Counts completed transcript rows before roadmap matching, so the UI can show both numbers.
    completed_transcript_course_count = 0
    completed_transcript_academic_units = 0.0

    for transcript_row in transcript_rows:
        course_code = transcript_row["code"]
        grade = transcript_row["grade"]
        academic_units = float(transcript_row["academic_units"])

        # Only completed/exempted modules should affect roadmap progress.
        if grade not in COMPLETED_GRADES:
            logger.info("Skipping %s because grade %s is not marked completed.", course_code, grade)
            continue

        completed_transcript_course_count += 1
        completed_transcript_academic_units += academic_units
        roadmap_course = roadmap_courses_by_code.get(course_code)
        transcript_course = TranscriptCourse(
            course_code=course_code,
            course_id=roadmap_course.id if roadmap_course else f"transcript-{course_code.lower()}",
            title=roadmap_course.title if roadmap_course else transcript_row["title"],
            academic_units=academic_units,
            grade=grade,
            grade_point=(
                float(transcript_row["grade_point"])
                if transcript_row["grade_point"]
                else None
            ),
            academic_year=transcript_row.get("academic_year"),
            transcript_semester=transcript_row.get("transcript_semester"),
            study_year=transcript_row.get("study_year"),
        )
        completed_transcript_courses.append(transcript_course)

        if roadmap_course is None:
            # The transcript can contain non-roadmap modules such as business/common-core courses.
            logger.info("Parsed course %s but it is not in the CSC roadmap.", course_code)
            unmatched_course_codes.append(course_code)
            continue

        logger.info("Matched completed roadmap course: %s (%s).", course_code, grade)
        completed_courses.append(transcript_course)

    logger.info(
        "Transcript parsing complete: %s completed roadmap course(s), %s unmatched course code(s).",
        len(completed_courses),
        len(unmatched_course_codes),
    )

    total_academic_units_earned = (
        extract_total_academic_units_earned(transcript_text)
        or completed_transcript_academic_units
    )

    return TranscriptUploadResponse(
        completed_courses=completed_courses,
        completed_transcript_courses=completed_transcript_courses,
        completed_transcript_course_count=completed_transcript_course_count,
        total_academic_units_earned=total_academic_units_earned,
        unmatched_course_codes=unmatched_course_codes,
    )
