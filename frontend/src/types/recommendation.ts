export interface RecommendationChoiceSlot {
  slotId: string
  courseCode: string
  year: number
  semester: number
}

export interface RecommendationCurriculumCourse {
  nodeId: string
  courseCode: string
  title: string
  year: number
  semester: number
  isChoiceSlot: boolean
}

export interface RecommendationRequest {
  careerGoal: string
  preferredRecommendationTags: string[]
  studentFaculty: string | null
  completedCourseCodes: string[]
  choiceSlotCodes: string[]
  choiceSlots: RecommendationChoiceSlot[]
  curriculumCourses: RecommendationCurriculumCourse[]
  excludedCourseCodes: string[]
  excludedCourseTitles: string[]
  limit: number
}

export type RecommendationReadinessStatus = 'ready' | 'needs-prerequisite-planning'

export interface RecommendationCareerSkillEvidence {
  careerGoal: string
  skillArea: string
  skillAreaWeight: number
  tag: string
  relationshipWeight: number
  tagConfidence: number
  contributionScore: number
  rationale: string
}

export interface RecommendationScoreBreakdown {
  careerTagScore: number
  careerSkillScore: number
  careerSkillEvidence: RecommendationCareerSkillEvidence | null
  currentSemesterBonus: number
  preferenceBoost: number
  sameFacultyBoost: number
  legacyCodePenalty: number
  defaultProfileAdjustment: number
  unlockContribution: number
  finalScore: number
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
  prerequisites: string[]
  missingPrerequisites: string[]
  existingPrerequisiteCourseCodes: string[]
  plannedPrerequisiteCourseCodes: string[]
  prerequisiteRecommendations: RecommendationPrerequisite[]
  plannedRoadmapNodes?: RecommendationPlannedRoadmapNode[]
  plannedRoadmapEdges?: RecommendationPlannedRoadmapEdge[]
  readinessStatus: RecommendationReadinessStatus
  unlockValue: number
  score: number
  scoreBreakdown: RecommendationScoreBreakdown
  reason: string
}

export interface RecommendationPrerequisite {
  courseCode: string
  title: string
  academicUnits: number | null
  faculty: string | null
  level: number | null
}

export interface RecommendationPlannedRoadmapNode {
  id: string
  courseCode: string
  title: string
  type: string
  year: number
  semester: number
  academicUnits: number
  prerequisiteText: string
  recommendedForCourseCode: string
}

export interface RecommendationPlannedRoadmapEdge {
  source: string
  target: string
}

export interface RecommendationResponse {
  careerGoal: string
  recommendations: CourseRecommendation[]
}
