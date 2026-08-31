import type { CurriculumGuideResponse } from '../types/curriculum'
import type { RoadmapResponse } from '../types/roadmap'
import type { TranscriptCourse } from '../types/transcript'

const ROADMAP_API_URL = 'http://127.0.0.1:8000/roadmap'
const PERSONALIZED_ROADMAP_API_URL = 'http://127.0.0.1:8000/roadmap/personalized'

export async function fetchRoadmap(): Promise<RoadmapResponse> {
  const response = await fetch(ROADMAP_API_URL)

  if (!response.ok) {
    throw new Error('Failed to load roadmap data')
  }

  return response.json() as Promise<RoadmapResponse>
}

export async function fetchPersonalizedRoadmap(
  curriculumGuide: CurriculumGuideResponse,
  transcriptCompletedCourses: TranscriptCourse[],
  transcriptUnmatchedCourseCodes: string[],
): Promise<RoadmapResponse> {
  const response = await fetch(PERSONALIZED_ROADMAP_API_URL, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
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
