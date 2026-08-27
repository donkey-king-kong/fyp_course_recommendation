import type { CurriculumGuideResponse } from '../types/curriculum'

const CURRICULUM_GUIDE_API_URL = 'http://127.0.0.1:8000/curriculum-guide'

export async function uploadCurriculumGuide(file: File): Promise<CurriculumGuideResponse> {
  const formData = new FormData()

  formData.append('file', file)

  const response = await fetch(CURRICULUM_GUIDE_API_URL, {
    method: 'POST',
    body: formData,
  })

  if (!response.ok) {
    throw new Error('Failed to upload curriculum guide')
  }

  return response.json() as Promise<CurriculumGuideResponse>
}
