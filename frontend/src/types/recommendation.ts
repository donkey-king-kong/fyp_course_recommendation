export interface RecommendationChoiceSlot {
  slotId: string
  courseCode: string
  year: number
  semester: number
}

export interface RecommendationRequest {
  careerGoal: string
  completedCourseCodes: string[]
  choiceSlotCodes: string[]
  choiceSlots: RecommendationChoiceSlot[]
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
  matchedChoiceSlotId: string | null
  matchedChoiceSlotYear: number | null
  matchedChoiceSlotSemester: number | null
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
