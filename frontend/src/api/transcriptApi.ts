import type { CurriculumGuideResponse } from '../types/curriculum'
import type {
  TranscriptCourse,
  TranscriptCurriculumMatchResponse,
  TranscriptUploadResponse,
} from '../types/transcript'
import { API_BASE_URL, apiFetch } from './apiConfig'

export async function uploadTranscript(file: File): Promise<TranscriptUploadResponse> {
  // File uploads must be sent as multipart/form-data, not JSON
  const formData = new FormData()

  // The key must be "file" because the FastAPI route parameter is named file
  formData.append('file', file)

  // File uploads use FormData; don't set Content-Type (browser sets multipart boundary).
  const response = await fetch(`${API_BASE_URL}/transcript`, {
    method: 'POST',
    credentials: 'include',
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
  const response = await apiFetch('/transcript/match-curriculum', {
    method: 'POST',
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
