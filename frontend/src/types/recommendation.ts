export interface RecommendationRequest {
  careerGoal: string
  completedCourseCodes: string[]
  choiceSlotCodes: string[]
  limit: number
}

export interface CourseRecommendation {
  courseCode: string
  title: string
  academicUnits: number | null
  faculty: string | null
  level: number | null
  matchedChoiceSlot: string
  matchedKeywords: string[]
  missingPrerequisites: string[]
  score: number
  reason: string
}

export interface RecommendationResponse {
  careerGoal: string
  recommendations: CourseRecommendation[]
}
