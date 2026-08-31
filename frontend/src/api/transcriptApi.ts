import type { CurriculumGuideResponse } from '../types/curriculum'
import type {
  TranscriptCourse,
  TranscriptCurriculumMatchResponse,
  TranscriptUploadResponse,
} from '../types/transcript'

// Backend endpoint that accepts the uploaded transcript PDF
const TRANSCRIPT_API_URL = 'http://127.0.0.1:8000/transcript'
const TRANSCRIPT_MATCH_API_URL = 'http://127.0.0.1:8000/transcript/match-curriculum'

export async function uploadTranscript(file: File): Promise<TranscriptUploadResponse> {
  // File uploads must be sent as multipart/form-data, not JSON
  const formData = new FormData()

  // The key must be "file" because the FastAPI route parameter is named file
  formData.append('file', file)

  const response = await fetch(TRANSCRIPT_API_URL, {
    method: 'POST',
    body: formData,
  })

  if (!response.ok) {
    // ProfilePage catches this and shows a user-friendly upload error
    throw new Error('Failed to upload transcript')
  }

  // Return the parsed transcript result from the backend
  return response.json() as Promise<TranscriptUploadResponse>
}

export async function matchTranscriptToCurriculum(
  completedCourseCodes: string[],
  transcriptCompletedCourses: TranscriptCourse[],
  curriculumGuide: CurriculumGuideResponse,
): Promise<TranscriptCurriculumMatchResponse> {
  const response = await fetch(TRANSCRIPT_MATCH_API_URL, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      completedCourseCodes,
      transcriptCompletedCourses,
      curriculumCourses: curriculumGuide.nodes,
    }),
  })

  if (!response.ok) {
    throw new Error('Failed to match transcript to curriculum')
  }

  return response.json() as Promise<TranscriptCurriculumMatchResponse>
}
