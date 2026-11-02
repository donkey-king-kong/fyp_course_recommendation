import type { CurriculumGuideResponse } from '../types/curriculum'
import { API_BASE_URL } from './apiConfig'

export async function uploadCurriculumGuide(file: File): Promise<CurriculumGuideResponse> {
  const formData = new FormData()

  formData.append('file', file)

  // File uploads use FormData; don't set Content-Type (browser sets multipart boundary).
  const response = await fetch(`${API_BASE_URL}/curriculum-guide`, {
    method: 'POST',
    credentials: 'include',
    body: formData,
  })

  if (!response.ok) {
    throw new Error('Failed to upload curriculum guide')
  }

  return response.json() as Promise<CurriculumGuideResponse>
}
