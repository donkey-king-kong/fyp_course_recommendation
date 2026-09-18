import type {
  AdminBenchmarkCaseDetailResponse,
  AdminBenchmarkSummaryResponse,
  AdminLoginRequest,
  AdminLoginResponse,
} from '../types/admin'

const ADMIN_API_BASE_URL = 'http://127.0.0.1:8000/admin'

async function parseAdminResponse<T>(response: Response, fallbackMessage: string): Promise<T> {
  if (!response.ok) {
    throw new Error(fallbackMessage)
  }

  return response.json() as Promise<T>
}

export async function loginAdmin(request: AdminLoginRequest): Promise<AdminLoginResponse> {
  const response = await fetch(`${ADMIN_API_BASE_URL}/login`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(request),
  })

  return parseAdminResponse<AdminLoginResponse>(response, 'Admin login failed.')
}

export async function fetchAdminBenchmarkSummary(
  adminToken: string,
): Promise<AdminBenchmarkSummaryResponse> {
  const response = await fetch(`${ADMIN_API_BASE_URL}/benchmark`, {
    headers: {
      'X-Admin-Token': adminToken,
    },
  })

  return parseAdminResponse<AdminBenchmarkSummaryResponse>(
    response,
    'Could not load benchmark summary.',
  )
}

export async function fetchAdminBenchmarkCase(
  adminToken: string,
  caseId: string,
): Promise<AdminBenchmarkCaseDetailResponse> {
  const response = await fetch(`${ADMIN_API_BASE_URL}/benchmark/${caseId}`, {
    headers: {
      'X-Admin-Token': adminToken,
    },
  })

  return parseAdminResponse<AdminBenchmarkCaseDetailResponse>(
    response,
    'Could not load benchmark case.',
  )
}
