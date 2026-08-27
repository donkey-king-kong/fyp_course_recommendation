export interface CurriculumCourse {
  id: string
  courseCode: string
  title: string
  type: string
  year: number
  semester: number
  academicUnits: number
  prerequisites: string[]
  prerequisiteText: string
  isChoiceSlot: boolean
}

export interface CurriculumSemester {
  year: number
  semester: number
  totalAcademicUnits: number
  courses: CurriculumCourse[]
}

export interface CurriculumEdge {
  source: string
  target: string
}

export interface CurriculumGuideResponse {
  major: string
  cohort: string
  totalAcademicUnits: number
  semesters: CurriculumSemester[]
  nodes: CurriculumCourse[]
  edges: CurriculumEdge[]
}
