export interface ModuleSummary {
  code: string
  title: string
  au: number | null
  faculty: string | null
  description: string | null
  level: number | null
  categories: string[]
  recommendation_tags: string[]
  latest_year: string | null
  latest_semester: string | null
  is_current_semester: boolean
  not_available_to_programme: string | null
  prerequisites: string[]
  unlocks: string[]
  prerequisite_count: number
  unlock_count: number
}

export interface ModuleListResponse {
  items: ModuleSummary[]
  total: number
  limit: number
  offset: number
}

export interface ModuleFilterOptions {
  faculties: string[]
  levels: number[]
  categories: string[]
}

export interface ModuleQuery {
  search?: string
  faculty?: string
  level?: number
  category?: string
  currentOnly?: boolean
  limit?: number
  offset?: number
}
