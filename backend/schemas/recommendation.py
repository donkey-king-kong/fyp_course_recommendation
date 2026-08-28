from typing import Optional

from pydantic import BaseModel, ConfigDict, Field

class RecommendationChoiceSlot(BaseModel):
    slotId: Optional[str] = Field(
        default=None,
        description="Frontend roadmap node ID for this exact open choice slot.",
        examples=["year3-sem1-slot2"],
    )
    courseCode: str = Field(
        description="Choice slot placeholder code, such as BDE, SC3xxx, or SC4xxx.",
        examples=["BDE"],
    )
    year: Optional[int] = Field(
        default=None,
        description="Roadmap year where this open choice slot appears.",
        examples=[3],
    )
    semester: Optional[int] = Field(
        default=None,
        description="Roadmap semester where this open choice slot appears.",
        examples=[1],
    )

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
        description="Legacy open curriculum choice slot codes, such as SC3xxx or SC4xxx.",
        examples=[["SC3xxx", "SC4xxx"]],
    )
    choiceSlots: list[RecommendationChoiceSlot] = Field(
        default_factory=list,
        description="Open curriculum choice slots with roadmap position details for backend slot-fit ranking.",
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
    matchedChoiceSlotId: Optional[str] = None
    matchedChoiceSlotYear: Optional[int] = None
    matchedChoiceSlotSemester: Optional[int] = None
    matchedKeywords: list[str]
    prerequisites: list[str]
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
                        "matchedChoiceSlotId": "year3-sem1-slot2",
                        "matchedChoiceSlotYear": 3,
                        "matchedChoiceSlotSemester": 1,
                        "matchedKeywords": ["software", "engineering"],
                        "prerequisites": ["SC2006"],
                        "missingPrerequisites": [],
                        "prerequisiteRecommendations": [],
                        "score": 9,
                        "reason": "Matches Software Engineer keywords: software, engineering.",
                    }
                ],
            }
        }
    )
