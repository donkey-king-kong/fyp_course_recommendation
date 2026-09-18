from typing import Any, Literal, Optional, Union

from pydantic import BaseModel, Field

AdminBenchmarkCaseStatus = Literal["ok", "needs-review", "missing-predictions"]

class AdminLoginRequest(BaseModel):
    username: str = Field(description="Local development admin username.", examples=["admin"])
    password: str = Field(description="Local development admin password.", examples=["admin-password"])

class AdminLoginResponse(BaseModel):
    isAdmin: bool = Field(description="Whether the submitted credentials matched the configured admin login.")
    token: str = Field(description="Prototype admin token to send with later admin API requests.")

class AdminBenchmarkPredictionSummary(BaseModel):
    courseCode: str
    title: str
    score: Optional[float]
    matchedChoiceSlotId: Optional[str]
    expectedRelevance: str

class AdminBenchmarkCaseSummary(BaseModel):
    caseId: str
    description: str
    careerGoal: str
    studentFaculty: Optional[str]
    preferredRecommendationTags: list[str]
    completedCourseCount: int
    choiceSlotCount: int
    reviewedCandidateCount: int
    recommendationCount: int
    precisionAtK: float
    ndcgAtK: float
    slotFillRate: float
    constraintValidity: float
    status: AdminBenchmarkCaseStatus
    topPredictions: list[AdminBenchmarkPredictionSummary]

class AdminBenchmarkSummaryResponse(BaseModel):
    schemaVersion: Union[int, str]
    benchmarkStatus: str
    predictionGeneratedAt: Optional[str]
    predictionApiUrl: Optional[str]
    k: int
    caseCount: int
    averagePrecisionAtK: float
    averageNdcgAtK: float
    averageSlotFillRate: float
    averageConstraintValidity: float
    oldCodeExposure: int
    cases: list[AdminBenchmarkCaseSummary]

class AdminAnnotatedRecommendation(BaseModel):
    courseCode: str
    title: str
    score: Optional[float]
    matchedChoiceSlot: Optional[str]
    matchedChoiceSlotId: Optional[str]
    readinessStatus: Optional[str]
    reason: Optional[str]
    expectedRelevance: str
    expectedSkillPath: Optional[str]
    reviewNotes: Optional[str]
    constraintValid: bool
    scoreBreakdown: dict[str, Any]

class AdminReviewedCandidate(BaseModel):
    courseCode: str
    title: str
    targetSlotId: Optional[str]
    expectedRelevance: str
    expectedSkillPath: Optional[str]
    oldCodeHandling: Optional[str]
    reviewNotes: Optional[str]
    wasRecommended: bool
    predictedRank: Optional[int]
    predictedScore: Optional[float]

class AdminBenchmarkCaseDetailResponse(BaseModel):
    caseId: str
    description: str
    studentFaculty: Optional[str]
    careerGoal: str
    reviewerStatus: Optional[str]
    preferredRecommendationTags: list[str]
    completedCourseCodes: list[str]
    choiceSlots: list[dict[str, Any]]
    curriculumCourses: list[Any]
    metrics: dict[str, Any]
    request: dict[str, Any]
    rankedRecommendations: list[AdminAnnotatedRecommendation]
    reviewedCandidates: list[AdminReviewedCandidate]
