export interface TranscriptCourse {
  course_code: string
  course_id: string
  title: string
  academic_units: number
  grade: string
  grade_point: number | null
  academic_year: string | null
  transcript_semester: number | null
  study_year: number | null
}

export interface TranscriptUploadResponse {
  // Roadmap-matched completed courses used to tick checkboxes.
  completed_courses: TranscriptCourse[]
  // All completed transcript rows, including modules that are not in the roadmap.
  completed_transcript_courses: TranscriptCourse[]
  // Count of all completed transcript rows.
  completed_transcript_course_count: number
  total_academic_units_earned: number
  unmatched_course_codes: string[]
}
