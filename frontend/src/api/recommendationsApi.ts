import type {
  RecommendationRequest,
  RecommendationResponse,
} from '../types/recommendation'
import { apiFetch } from './apiConfig'

const RECOMMENDATIONS_TIMEOUT_MS = 15000

export async function fetchRecommendations(
  request: RecommendationRequest,
): Promise<RecommendationResponse> {
  const controller = new AbortController()
  // Prevents the Profile page from staying in Loading state if the backend reloads or stalls.
  const timeoutId = window.setTimeout(() => controller.abort(), RECOMMENDATIONS_TIMEOUT_MS)

  try {
    const response = await apiFetch('/recommendations', {
      method: 'POST',
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
