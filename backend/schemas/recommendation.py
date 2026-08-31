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
        description=(
            "Open curriculum choice slots with roadmap position details. The backend "
            "uses these slots for final exact-slot assignment."
        ),
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
        description=(
            "Maximum number of assigned recommendations to return. The frontend "
            "currently sends one slot per open choice slot."
        ),
    )

class RecommendationPrerequisite(BaseModel):
    courseCode: str
    title: str
    academicUnits: Optional[float]
    faculty: Optional[str]
    level: Optional[int]

class RecommendationPlannedRoadmapNode(BaseModel):
    id: str = Field(description="Backend-generated roadmap node ID for the planned prerequisite.")
    courseCode: str = Field(description="Course code of the planned prerequisite module.")
    title: str = Field(description="Display title of the planned prerequisite module.")
    type: str = Field(description="Roadmap card type, usually Recommended Pre-Requisite.")
    year: int = Field(description="Suggested roadmap year for this planned prerequisite card.")
    semester: int = Field(description="Suggested roadmap semester for this planned prerequisite card.")
    academicUnits: float = Field(description="Academic units for the planned prerequisite module.")
    prerequisiteText: str = Field(description="Raw prerequisite text for the planned prerequisite module.")
    recommendedForCourseCode: str = Field(
        description="Recommended module code that this planned prerequisite supports.",
    )

class RecommendationPlannedRoadmapEdge(BaseModel):
    source: str = Field(description="Source roadmap node ID for the planned prerequisite arrow.")
    target: str = Field(description="Target roadmap node ID for the planned prerequisite arrow.")

class RecommendationScoreBreakdown(BaseModel):
    careerTagScore: int = Field(
        description="Base relevance score from career keywords and curated recommendation tags.",
        examples=[13],
    )
    currentSemesterBonus: int = Field(
        description="Small bonus when the module is available in the current catalog semester.",
        examples=[1],
    )
    preferenceBoost: int = Field(
        description="Soft boost from matching the student's selected topic preferences.",
        examples=[30],
    )
    sameFacultyBoost: int = Field(
        description="Soft boost when the module faculty matches the student's profile faculty.",
        examples=[8],
    )
    legacyCodePenalty: int = Field(
        description="Negative adjustment for older CSC/CZ course codes when the student is in CSC.",
        examples=[0],
    )
    unlockContribution: int = Field(
        description="Small pathway boost from unlocking later fixed curriculum modules.",
        examples=[1],
    )
    finalScore: int = Field(
        description="Final score used for ranking after all deterministic components are applied.",
        examples=[53],
    )

class CourseRecommendation(BaseModel):
    courseCode: str
    title: str
    academicUnits: Optional[float]
    faculty: Optional[str]
    level: Optional[int]
    matchedChoiceSlot: str = Field(description="Choice-slot code that this recommendation satisfies.")
    matchedChoiceSlotId: Optional[str] = Field(
        default=None,
        description="Exact open roadmap choice-slot node ID assigned by the backend.",
    )
    matchedChoiceSlotYear: Optional[int] = Field(
        default=None,
        description="Roadmap year of the assigned choice slot.",
    )
    matchedChoiceSlotSemester: Optional[int] = Field(
        default=None,
        description="Roadmap semester of the assigned choice slot.",
    )
    matchedKeywords: list[str]
    prerequisites: list[str]
    missingPrerequisites: list[str]
    existingPrerequisiteCourseCodes: list[str]
    plannedPrerequisiteCourseCodes: list[str]
    prerequisiteRecommendations: list[RecommendationPrerequisite]
    plannedRoadmapNodes: list[RecommendationPlannedRoadmapNode] = Field(
        default_factory=list,
        description="Backend-planned prerequisite nodes that the frontend can render with the assignment.",
    )
    plannedRoadmapEdges: list[RecommendationPlannedRoadmapEdge] = Field(
        default_factory=list,
        description="Backend-planned prerequisite arrows that connect planned nodes to the assignment.",
    )
    readinessStatus: RecommendationReadinessStatus = Field(
        description="Whether the recommendation is ready now or needs prerequisite planning.",
    )
    unlockValue: int
    score: int
    scoreBreakdown: RecommendationScoreBreakdown
    reason: str

class RecommendationResponse(BaseModel):
    careerGoal: str
    recommendations: list[CourseRecommendation] = Field(
        description=(
            "Backend-assigned recommendations. Each item should be rendered using "
            "`matchedChoiceSlotId`; the frontend should not re-rank or reassign them."
        ),
    )

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
                        "plannedRoadmapNodes": [],
                        "plannedRoadmapEdges": [],
                        "readinessStatus": "ready",
                        "unlockValue": 1,
                        "score": 9,
                        "scoreBreakdown": {
                            "careerTagScore": 7,
                            "currentSemesterBonus": 1,
                            "preferenceBoost": 0,
                            "sameFacultyBoost": 0,
                            "legacyCodePenalty": 0,
                            "unlockContribution": 1,
                            "finalScore": 9,
                        },
                        "reason": "Matches Software Engineer keywords: software, engineering.",
                    }
                ],
            }
        }
    )
