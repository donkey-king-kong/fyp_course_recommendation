from typing import Optional

from pydantic import BaseModel, ConfigDict, Field

from backend.schemas.curriculum import CurriculumGuideResponse
from backend.schemas.transcript import TranscriptCourse

class CourseNode(BaseModel):
    id: str = Field(description="Stable roadmap node ID used by the frontend.")
    courseCode: str = Field(description="NTU course code or choice-slot placeholder code.")
    title: str = Field(description="Display title for the roadmap card.")
    type: str = Field(description="Curriculum category, choice-slot type, or transcript-only marker.")
    year: int = Field(description="Roadmap year. Transcript-only modules may use 0 if placement is unknown.")
    semester: int = Field(description="Roadmap semester. Transcript-only modules may use 0 if placement is unknown.")
    academicUnits: float = Field(description="Academic units assigned to this roadmap item.")
    prerequisites: list[str] = Field(description="Roadmap node IDs that must be completed before this node.")
    prerequisiteText: Optional[str] = Field(
        default=None,
        description="Raw prerequisite text from the curriculum guide or module catalog.",
    )
    isCompleted: bool = Field(description="Whether the node should be treated as completed.")
    isChoiceSlot: bool = Field(
        default=False,
        description="Whether this node is an open BDE/MPE/choice-slot placeholder.",
    )
    isTranscriptOnly: bool = Field(
        default=False,
        description="Whether this completed module came from the transcript but was not matched to the curriculum guide.",
    )
    isRecommendedPrerequisite: bool = Field(
        default=False,
        description="Whether this node is a backend-planned prerequisite for a recommendation.",
    )
    recommendedForCourseCode: Optional[str] = Field(
        default=None,
        description="Recommended module code that this planned prerequisite supports.",
    )
    jobSkills: list[str] = Field(description="Reserved skill labels for future recommendation display.")

class RoadmapEdge(BaseModel):
    source: str = Field(description="Source roadmap node ID.")
    target: str = Field(description="Target roadmap node ID.")

class RoadmapResponse(BaseModel):
    nodes: list[CourseNode] = Field(
        description="Ready-to-render roadmap nodes after backend roadmap projection.",
    )
    edges: list[RoadmapEdge] = Field(
        description="Ready-to-render prerequisite/unlock arrows normalized to RoadmapEdge objects.",
    )

class PersonalizedRoadmapRequest(BaseModel):
    curriculumGuide: CurriculumGuideResponse = Field(
        description="Parsed curriculum guide response that defines the student's roadmap structure.",
    )
    transcriptCompletedCourses: list[TranscriptCourse] = Field(
        default_factory=list,
        description="Completed transcript modules already parsed by the backend transcript endpoint.",
    )
    transcriptUnmatchedCourseCodes: list[str] = Field(
        default_factory=list,
        description="Completed transcript module codes that did not match curriculum guide rows.",
    )

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "curriculumGuide": {
                    "major": "Computer Science",
                    "cohort": "AY2025-26",
                    "totalAcademicUnits": 135,
                    "semesters": [],
                    "standingRequirements": [],
                    "nodes": [
                        {
                            "id": "y4s1-sc4xxx-1",
                            "courseCode": "SC4xxx",
                            "title": "Major Prescribed Elective",
                            "type": "MPE",
                            "year": 4,
                            "semester": 1,
                            "academicUnits": 3,
                            "prerequisites": [],
                            "prerequisiteText": "Nil",
                            "isChoiceSlot": True,
                        }
                    ],
                    "edges": [],
                },
                "transcriptCompletedCourses": [],
                "transcriptUnmatchedCourseCodes": [],
            }
        }
    )
