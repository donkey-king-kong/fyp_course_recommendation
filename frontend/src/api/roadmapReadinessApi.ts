import type {
  RoadmapReadinessRequest,
  RoadmapReadinessResponse,
} from '../types/roadmapReadiness'

const ROADMAP_READINESS_API_URL = 'http://127.0.0.1:8000/roadmap/readiness'
const ROADMAP_READINESS_TIMEOUT_MS = 10000

export async function fetchRoadmapReadiness(
  request: RoadmapReadinessRequest,
): Promise<RoadmapReadinessResponse> {
  const controller = new AbortController()
  const timeoutId = window.setTimeout(() => controller.abort(), ROADMAP_READINESS_TIMEOUT_MS)

  try {
    const response = await fetch(ROADMAP_READINESS_API_URL, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(request),
      signal: controller.signal,
    })

    if (!response.ok) {
      throw new Error('Failed to evaluate roadmap readiness')
    }

    return response.json() as Promise<RoadmapReadinessResponse>
  } finally {
    window.clearTimeout(timeoutId)
  }
}
