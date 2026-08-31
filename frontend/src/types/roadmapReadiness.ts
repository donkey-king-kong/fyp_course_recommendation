export type RoadmapReadinessStatus = 'completed' | 'available' | 'locked'

export interface RoadmapReadinessCourse {
  id: string
  courseCode: string
  type: string
  prerequisites: string[]
  prerequisiteText?: string
}

export interface RoadmapStandingRequirement {
  standingYear: number
  minimumAcademicUnits: number
}

export interface RoadmapReadinessRequest {
  courses: RoadmapReadinessCourse[]
  completedCourseIds: string[]
  completedAcademicUnits: number
  standingRequirements: RoadmapStandingRequirement[]
}

export interface RoadmapCourseReadiness {
  courseId: string
  status: RoadmapReadinessStatus
  missingRequirements: string[]
}

export interface RoadmapReadinessResponse {
  courses: RoadmapCourseReadiness[]
}
