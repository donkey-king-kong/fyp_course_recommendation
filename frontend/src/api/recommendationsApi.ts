import type {
  RecommendationRequest,
  RecommendationResponse,
} from '../types/recommendation'

const RECOMMENDATIONS_API_URL = 'http://127.0.0.1:8000/recommendations'
const RECOMMENDATIONS_TIMEOUT_MS = 15000

export async function fetchRecommendations(
  request: RecommendationRequest,
): Promise<RecommendationResponse> {
  const controller = new AbortController()
  const timeoutId = window.setTimeout(() => controller.abort(), RECOMMENDATIONS_TIMEOUT_MS)

  try {
    const response = await fetch(RECOMMENDATIONS_API_URL, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(request),
      signal: controller.signal,
    })

    if (!response.ok) {
      throw new Error('Failed to load recommendations')
    }

    return response.json() as Promise<RecommendationResponse>
  } finally {
    window.clearTimeout(timeoutId)
  }
}
