export const API_BASE_URL = 'http://localhost:8000'

// All API calls must include credentials so the session cookie is sent cross-origin.
export async function apiFetch(input: string, init?: RequestInit): Promise<Response> {
  return fetch(`${API_BASE_URL}${input}`, {
    ...init,
    credentials: 'include',
    headers: {
      'Content-Type': 'application/json',
      ...init?.headers,
    },
  })
}
