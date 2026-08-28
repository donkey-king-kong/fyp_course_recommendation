export interface CourseNode {
  id: string
  courseCode: string
  title: string
  type: string
  year: number
  semester: number
  academicUnits: number
  prerequisites: string[]
  prerequisiteText?: string
  isCompleted: boolean
  isChoiceSlot?: boolean
  isTranscriptOnly?: boolean
  isRecommendedPrerequisite?: boolean
  recommendedForCourseCode?: string
  jobSkills: string[]
}

export interface RoadmapEdge {
  source: string
  target: string
}

export interface RoadmapResponse {
  nodes: CourseNode[]
  edges: RoadmapEdge[]
}
