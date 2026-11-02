import type { AuthUser } from '../types/auth'
import { API_BASE_URL } from './apiConfig'

// Returns the signed-in user or null if there is no active session.
export async function fetchCurrentUser(): Promise<AuthUser | null> {
  const response = await fetch(`${API_BASE_URL}/me`, {
    credentials: 'include',
  })

  if (response.status === 401) {
    return null
  }

  if (!response.ok) {
    throw new Error('Failed to fetch current user')
  }

  return response.json() as Promise<AuthUser>
}
