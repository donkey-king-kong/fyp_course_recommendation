from typing import Literal, Optional

from pydantic import BaseModel, ConfigDict, Field

RecommendationReadinessStatus = Literal["ready", "needs-prerequisite-planning"]

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

class RecommendationCurriculumCourse(BaseModel):
    nodeId: Optional[str] = Field(
        default=None,
        description="Frontend roadmap node ID for this curriculum course.",
        examples=["year1-sem2-sc1004"],
    )
    courseCode: str = Field(
        description="Course code or choice-slot placeholder shown in the uploaded curriculum guide.",
        examples=["SC1004"],
    )
    title: Optional[str] = Field(
        default=None,
        description="Course title from the uploaded curriculum guide.",
        examples=["Linear Algebra for Computing"],
    )
    year: Optional[int] = Field(
        default=None,
        description="Roadmap year where this course appears.",
        examples=[1],
    )
    semester: Optional[int] = Field(
        default=None,
        description="Roadmap semester where this course appears.",
        examples=[2],
    )
    isChoiceSlot: bool = Field(
        default=False,
        description="Whether this curriculum item is an open BDE/MPE choice slot.",
    )

class RecommendationRequest(BaseModel):
    careerGoal: str = Field(
        description="Career goal selected by the student.",
        examples=["software-engineer"],
    )
    preferredRecommendationTags: list[str] = Field(
        default_factory=list,
        description="Optional student topic preferences used as a soft ranking boost.",
        examples=[["backend-engineering", "database"]],
    )
    studentFaculty: Optional[str] = Field(
        default=None,
        description="Student's home faculty/major code used as a soft same-faculty ranking boost.",
        examples=["CSC"],
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
    curriculumCourses: list[RecommendationCurriculumCourse] = Field(
        default_factory=list,
        description="Uploaded curriculum courses with roadmap positions for prerequisite readiness checks.",
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
    existingPrerequisiteCourseCodes: list[str]
    plannedPrerequisiteCourseCodes: list[str]
    prerequisiteRecommendations: list[RecommendationPrerequisite]
    readinessStatus: RecommendationReadinessStatus
    unlockValue: int
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
                        "existingPrerequisiteCourseCodes": ["SC2006"],
                        "plannedPrerequisiteCourseCodes": [],
                        "prerequisiteRecommendations": [],
                        "readinessStatus": "ready",
                        "unlockValue": 1,
                        "score": 9,
                        "reason": "Matches Software Engineer keywords: software, engineering.",
                    }
                ],
            }
        }
    )
