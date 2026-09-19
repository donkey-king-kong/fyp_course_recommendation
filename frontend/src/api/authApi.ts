import type { AuthenticatedUser } from '../types/auth'

const AUTH_API_BASE_URL = 'http://127.0.0.1:8000/auth'

export function redirectToNtuLogin() {
  window.location.href = `${AUTH_API_BASE_URL}/login`
}

export async function fetchCurrentUser(): Promise<AuthenticatedUser | null> {
  const response = await fetch(`${AUTH_API_BASE_URL}/me`, {
    credentials: 'include',
  })

  if (response.status === 401) {
    return null
  }

  if (!response.ok) {
    throw new Error('Failed to fetch current user')
  }

  return response.json() as Promise<AuthenticatedUser>
}

export async function logoutCurrentUser(): Promise<void> {
  const response = await fetch(`${AUTH_API_BASE_URL}/logout`, {
    method: 'POST',
    credentials: 'include',
  })

  if (!response.ok) {
    throw new Error('Failed to log out')
  }
}
