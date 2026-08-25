import type { ModuleFilterOptions, ModuleListResponse, ModuleQuery, ModuleSummary } from '../types/module'

const MODULES_API_URL = 'http://127.0.0.1:8000/modules'

function buildModuleQueryString(query: ModuleQuery): string {
  const params = new URLSearchParams()

  if (query.search) {
    params.set('search', query.search)
  }
  if (query.faculty) {
    params.set('faculty', query.faculty)
  }
  if (query.level !== undefined) {
    params.set('level', String(query.level))
  }
  if (query.category) {
    params.set('category', query.category)
  }
  if (query.currentOnly) {
    params.set('current_only', 'true')
  }
  if (query.limit !== undefined) {
    params.set('limit', String(query.limit))
  }
  if (query.offset !== undefined) {
    params.set('offset', String(query.offset))
  }

  return params.toString()
}

export async function fetchModules(query: ModuleQuery = {}): Promise<ModuleListResponse> {
  const queryString = buildModuleQueryString(query)
  const response = await fetch(queryString ? `${MODULES_API_URL}?${queryString}` : MODULES_API_URL)

  if (!response.ok) {
    throw new Error('Failed to load modules')
  }

  return response.json() as Promise<ModuleListResponse>
}

export async function fetchModuleFilters(): Promise<ModuleFilterOptions> {
  const response = await fetch(`${MODULES_API_URL}/filters`)

  if (!response.ok) {
    throw new Error('Failed to load module filters')
  }

  return response.json() as Promise<ModuleFilterOptions>
}

export async function fetchModuleByCode(code: string): Promise<ModuleSummary> {
  const response = await fetch(`${MODULES_API_URL}/${encodeURIComponent(code)}`)

  if (!response.ok) {
    throw new Error('Failed to load module details')
  }

  return response.json() as Promise<ModuleSummary>
}
