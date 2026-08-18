from typing import Optional

from pydantic import BaseModel


# Object of one course returned extracted from transcript
class TranscriptCourse(BaseModel):
    course_code: str
    course_id: str
    title: str
    academic_units: float
    grade: str # Transcript grade; EX counts as completed
    grade_point: Optional[float] # EX rows do not have a grade point, so this can be None


# API response returned by POST /transcript.
class TranscriptUploadResponse(BaseModel):
    completed_courses: list[TranscriptCourse]
    # Parsed transcript course codes that are not in the current CSC roadmap
    unmatched_course_codes: list[str]
