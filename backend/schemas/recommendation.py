from typing import Optional

from pydantic import BaseModel, ConfigDict, Field

class RecommendationRequest(BaseModel):
    careerGoal: str = Field(
        description="Career goal selected by the student.",
        examples=["software-engineer"],
    )
    completedCourseCodes: list[str] = Field(
        default_factory=list,
        description="Completed module codes parsed from the transcript.",
        examples=[["SC1003", "SC2002"]],
    )
    choiceSlotCodes: list[str] = Field(
        default_factory=list,
        description="Open curriculum choice slots, such as SC3xxx or SC4xxx.",
        examples=[["SC3xxx", "SC4xxx"]],
    )
    excludedCourseCodes: list[str] = Field(
        default_factory=list,
        description="Module codes already present in the student's curriculum roadmap.",
        examples=[["SC1003", "SC2006"]],
    )
    excludedCourseTitles: list[str] = Field(
        default_factory=list,
        description="Module titles already present in the student's curriculum roadmap.",
        examples=[["Software Engineering", "Computer Networks"]],
    )
    # Keep this high enough for several BDE/MPE slots, but still bounded for a simple MVP API.
    limit: int = Field(
        default=12,
        ge=1,
        le=120,
        description="Maximum number of recommendations to return.",
    )

class RecommendationPrerequisite(BaseModel):
    courseCode: str
    title: str
    academicUnits: Optional[float]
    faculty: Optional[str]
    level: Optional[int]

class CourseRecommendation(BaseModel):
    courseCode: str
    title: str
    academicUnits: Optional[float]
    faculty: Optional[str]
    level: Optional[int]
    matchedChoiceSlot: str
    matchedKeywords: list[str]
    missingPrerequisites: list[str]
    prerequisiteRecommendations: list[RecommendationPrerequisite]
    score: int
    reason: str

class RecommendationResponse(BaseModel):
    careerGoal: str
    recommendations: list[CourseRecommendation]

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "careerGoal": "software-engineer",
                "recommendations": [
                    {
                        "courseCode": "SC3002",
                        "title": "Software Engineering",
                        "academicUnits": 3.0,
                        "faculty": "CSC",
                        "level": 3,
                        "matchedChoiceSlot": "SC3xxx",
                        "matchedKeywords": ["software", "engineering"],
                        "missingPrerequisites": [],
                        "prerequisiteRecommendations": [],
                        "score": 9,
                        "reason": "Matches Software Engineer keywords: software, engineering.",
                    }
                ],
            }
        }
    )
