from typing import Optional

from pydantic import BaseModel, Field

from backend.schemas.curriculum import CurriculumGuideResponse
from backend.schemas.transcript import TranscriptCourse

class CourseNode(BaseModel):
    id: str
    courseCode: str
    title: str
    type: str
    year: int
    semester: int
    academicUnits: float
    prerequisites: list[str]
    prerequisiteText: Optional[str] = None
    isCompleted: bool
    isChoiceSlot: bool = False
    isTranscriptOnly: bool = False
    isRecommendedPrerequisite: bool = False
    recommendedForCourseCode: Optional[str] = None
    jobSkills: list[str]

class RoadmapEdge(BaseModel):
    source: str
    target: str

class RoadmapResponse(BaseModel):
    nodes: list[CourseNode]
    edges: list[RoadmapEdge]

class PersonalizedRoadmapRequest(BaseModel):
    curriculumGuide: CurriculumGuideResponse
    transcriptCompletedCourses: list[TranscriptCourse] = Field(default_factory=list)
    transcriptUnmatchedCourseCodes: list[str] = Field(default_factory=list)
