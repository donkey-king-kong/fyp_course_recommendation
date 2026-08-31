from typing import Literal, Optional

from pydantic import BaseModel, ConfigDict, Field

RoadmapReadinessStatus = Literal["completed", "available", "locked"]

class RoadmapReadinessCourse(BaseModel):
    id: str = Field(description="Roadmap node ID shown in the frontend.")
    courseCode: str = Field(description="Course code or choice-slot placeholder.")
    type: str = Field(description="Course type label from the roadmap.")
    prerequisites: list[str] = Field(
        default_factory=list,
        description="Roadmap node IDs that must be completed before this course.",
    )
    prerequisiteText: Optional[str] = Field(
        default=None,
        description="Raw prerequisite text from the uploaded curriculum guide.",
    )

class RoadmapStandingRequirement(BaseModel):
    standingYear: int = Field(description="Required standing year, such as 4 for Year 4 standing.")
    minimumAcademicUnits: int = Field(description="Minimum completed AU required for this standing.")

class RoadmapReadinessRequest(BaseModel):
    courses: list[RoadmapReadinessCourse] = Field(
        description="Displayed roadmap courses to evaluate.",
    )
    completedCourseIds: list[str] = Field(
        default_factory=list,
        description="Roadmap node IDs currently treated as completed.",
    )
    completedAcademicUnits: float = Field(
        ge=0,
        description="Completed AU used for academic-standing requirements.",
    )
    standingRequirements: list[RoadmapStandingRequirement] = Field(
        default_factory=list,
        description="Parsed academic-standing rules from the uploaded curriculum guide.",
    )

class RoadmapCourseReadiness(BaseModel):
    courseId: str
    status: RoadmapReadinessStatus
    missingRequirements: list[str]

class RoadmapReadinessResponse(BaseModel):
    courses: list[RoadmapCourseReadiness]

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "courses": [
                    {
                        "courseId": "year4-sem1-sc4079",
                        "status": "locked",
                        "missingRequirements": [
                            "Year 4 standing requires 101 AU; you have 86 AU"
                        ],
                    }
                ]
            }
        }
    )
