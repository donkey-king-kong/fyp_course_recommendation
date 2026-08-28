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
    limit: int = Field(
        default=8,
        ge=1,
        le=20,
        description="Maximum number of recommendations to return.",
    )


class CourseRecommendation(BaseModel):
    courseCode: str
    title: str
    academicUnits: Optional[float]
    faculty: Optional[str]
    level: Optional[int]
    matchedChoiceSlot: str
    matchedKeywords: list[str]
    missingPrerequisites: list[str]
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
                        "score": 9,
                        "reason": "Matches Software Engineer keywords: software, engineering.",
                    }
                ],
            }
        }
    )
