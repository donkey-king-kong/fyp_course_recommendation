import type { CurriculumGuideResponse } from '../types/curriculum'
import type { RoadmapResponse } from '../types/roadmap'
import type { TranscriptCourse } from '../types/transcript'
import { apiFetch } from './apiConfig'

export async function fetchPersonalizedRoadmap(
  curriculumGuide: CurriculumGuideResponse,
  transcriptCompletedCourses: TranscriptCourse[],
  transcriptUnmatchedCourseCodes: string[],
): Promise<RoadmapResponse> {
  const response = await apiFetch('/roadmap/personalized', {
    method: 'POST',
    body: JSON.stringify({
      curriculumGuide,
      transcriptCompletedCourses,
      transcriptUnmatchedCourseCodes,
    }),
  })

  if (!response.ok) {
    throw new Error('Failed to build personalized roadmap')
  }

  return response.json() as Promise<RoadmapResponse>
}
