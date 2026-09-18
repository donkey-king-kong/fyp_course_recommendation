export interface AdminLoginRequest {
  username: string
  password: string
}

export interface AdminLoginResponse {
  isAdmin: boolean
  token: string
}

export type AdminBenchmarkCaseStatus = 'ok' | 'needs-review' | 'missing-predictions'

export interface AdminBenchmarkPredictionSummary {
  courseCode: string
  title: string
  score: number | null
  matchedChoiceSlotId: string | null
  expectedRelevance: string
}

export interface AdminBenchmarkCaseSummary {
  caseId: string
  description: string
  careerGoal: string
  studentFaculty: string | null
  preferredRecommendationTags: string[]
  completedCourseCount: number
  choiceSlotCount: number
  reviewedCandidateCount: number
  recommendationCount: number
  precisionAtK: number
  ndcgAtK: number
  slotFillRate: number
  constraintValidity: number
  status: AdminBenchmarkCaseStatus
  topPredictions: AdminBenchmarkPredictionSummary[]
}

export interface AdminBenchmarkSummaryResponse {
  schemaVersion: number | string
  benchmarkStatus: string
  predictionGeneratedAt: string | null
  predictionApiUrl: string | null
  k: number
  caseCount: number
  averagePrecisionAtK: number
  averageNdcgAtK: number
  averageSlotFillRate: number
  averageConstraintValidity: number
  oldCodeExposure: number
  cases: AdminBenchmarkCaseSummary[]
}

export interface AdminAnnotatedRecommendation {
  courseCode: string
  title: string
  score: number | null
  matchedChoiceSlot: string | null
  matchedChoiceSlotId: string | null
  readinessStatus: string | null
  reason: string | null
  expectedRelevance: string
  expectedSkillPath: string | null
  reviewNotes: string | null
  constraintValid: boolean
  scoreBreakdown: Record<string, unknown>
}

export interface AdminReviewedCandidate {
  courseCode: string
  title: string
  targetSlotId: string | null
  expectedRelevance: string
  expectedSkillPath: string | null
  oldCodeHandling: string | null
  reviewNotes: string | null
  wasRecommended: boolean
  predictedRank: number | null
  predictedScore: number | null
}

export interface AdminBenchmarkCaseDetailResponse {
  caseId: string
  description: string
  studentFaculty: string | null
  careerGoal: string
  reviewerStatus: string | null
  preferredRecommendationTags: string[]
  completedCourseCodes: string[]
  choiceSlots: Record<string, unknown>[]
  curriculumCourses: unknown[]
  metrics: Record<string, unknown>
  request: Record<string, unknown>
  rankedRecommendations: AdminAnnotatedRecommendation[]
  reviewedCandidates: AdminReviewedCandidate[]
}
