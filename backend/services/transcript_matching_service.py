import re

from backend.schemas.curriculum import CurriculumCourse
from backend.schemas.transcript import (
    TranscriptCourse,
    TranscriptCurriculumMatchResponse,
    TranscriptMatchedCourse,
)

TITLE_SIGNATURE_STOP_WORDS = {"principle", "principles"}
TITLE_SIGNATURE_TOKEN_REPLACEMENTS = {
    "databases": "database",
    "systems": "system",
}

def match_transcript_to_curriculum(
    completed_course_codes: list[str],
    transcript_completed_courses: list[TranscriptCourse],
    curriculum_courses: list[CurriculumCourse],
) -> TranscriptCurriculumMatchResponse:
    completed_code_set = set(completed_course_codes)
    transcript_course_keys = {
        key
        for course in transcript_completed_courses
        for key in get_transcript_course_keys(course)
    }
    matched_courses = [
        TranscriptMatchedCourse(courseCode=course.courseCode, title=course.title)
        for course in curriculum_courses
        if (
            course.courseCode in completed_code_set or
            normalize_course_title(course.title) in transcript_course_keys or
            get_course_title_signature(course.title) in transcript_course_keys
        )
    ]
    matched_course_keys = {
        key
        for course in curriculum_courses
        if any(matched.courseCode == course.courseCode for matched in matched_courses)
        for key in [
            course.courseCode,
            normalize_course_title(course.title),
            get_course_title_signature(course.title),
        ]
    }
    unmatched_course_codes = [
        course_code
        for course_code in completed_course_codes
        if is_unmatched_transcript_code(
            course_code,
            transcript_completed_courses,
            matched_course_keys,
        )
    ]

    return TranscriptCurriculumMatchResponse(
        completedCourseIds=[
            course.id
            for course in curriculum_courses
            if any(matched.courseCode == course.courseCode for matched in matched_courses)
        ],
        transcriptMatchedCourses=matched_courses,
        transcriptUnmatchedCourseCodes=unmatched_course_codes,
    )

def is_unmatched_transcript_code(
    course_code: str,
    transcript_completed_courses: list[TranscriptCourse],
    matched_course_keys: set[str],
) -> bool:
    transcript_course = next(
        (
            course
            for course in transcript_completed_courses
            if course.course_code == course_code
        ),
        None,
    )

    if not transcript_course:
        return course_code not in matched_course_keys

    return not any(
        key in matched_course_keys
        for key in get_transcript_course_keys(transcript_course)
    )

def get_transcript_course_keys(course: TranscriptCourse) -> set[str]:
    return {
        course.course_code,
        normalize_course_title(course.title),
        get_course_title_signature(course.title),
    }

def normalize_course_title(title: str) -> str:
    normalized_title = title.lower().replace("&", " and ")
    normalized_title = re.sub(r"[^a-z0-9]+", " ", normalized_title)

    return " ".join(normalized_title.split())

def get_course_title_signature(title: str) -> str:
    tokens = [
        TITLE_SIGNATURE_TOKEN_REPLACEMENTS.get(token, token)
        for token in normalize_course_title(title).split()
    ]
    meaningful_tokens = [
        token
        for token in tokens
        if token not in TITLE_SIGNATURE_STOP_WORDS
    ]

    return " ".join(meaningful_tokens)
