export interface TranscriptCourse {
  course_code: string
  course_id: string
  title: string
  academic_units: number
  grade: string
  grade_point: number | null
}

export interface TranscriptUploadResponse {
  completed_courses: TranscriptCourse[]
  unmatched_course_codes: string[]
}
