export interface RecommendationRequest {
  careerGoal: string
  completedCourseCodes: string[]
  choiceSlotCodes: string[]
  excludedCourseCodes: string[]
  excludedCourseTitles: string[]
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
  prerequisiteRecommendations: RecommendationPrerequisite[]
  score: number
  reason: string
}

export interface RecommendationPrerequisite {
  courseCode: string
  title: string
  academicUnits: number | null
  faculty: string | null
  level: number | null
}

export interface RecommendationResponse {
  careerGoal: string
  recommendations: CourseRecommendation[]
}
