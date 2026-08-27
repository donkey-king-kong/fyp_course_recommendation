import { useEffect, useMemo, useState } from 'react'
import { fetchModuleByCode, fetchModuleFilters, fetchModules } from '../api/modulesApi'
import type { ModuleFilterOptions, ModuleSummary } from '../types/module'
import './ModulesPage.css'

const MODULE_PAGE_SIZE = 24
const MODULE_FILTER_STORAGE_KEY = 'ntu-course-recommender-module-filters'

type SavedModuleFilters = {
  searchTerm: string
  selectedFaculty: string
  selectedLevel: string
  selectedCategory: string
  currentOnly: boolean
  offset: number
}

const DEFAULT_MODULE_FILTERS: SavedModuleFilters = {
  searchTerm: '',
  selectedFaculty: '',
  selectedLevel: '',
  selectedCategory: '',
  currentOnly: true,
  offset: 0,
}

// Reads saved module filters so refreshes keep the current catalogue view.
function getSavedModuleFilters(): SavedModuleFilters {
  const storedFilters = window.localStorage.getItem(MODULE_FILTER_STORAGE_KEY)

  if (!storedFilters) {
    return DEFAULT_MODULE_FILTERS
  }

  try {
    const parsedFilters = JSON.parse(storedFilters) as Partial<SavedModuleFilters>
    const savedOffset = parsedFilters.offset

    return {
      searchTerm: typeof parsedFilters.searchTerm === 'string' ? parsedFilters.searchTerm : DEFAULT_MODULE_FILTERS.searchTerm,
      selectedFaculty: typeof parsedFilters.selectedFaculty === 'string' ? parsedFilters.selectedFaculty : DEFAULT_MODULE_FILTERS.selectedFaculty,
      selectedLevel: typeof parsedFilters.selectedLevel === 'string' ? parsedFilters.selectedLevel : DEFAULT_MODULE_FILTERS.selectedLevel,
      selectedCategory: typeof parsedFilters.selectedCategory === 'string' ? parsedFilters.selectedCategory : DEFAULT_MODULE_FILTERS.selectedCategory,
      currentOnly: typeof parsedFilters.currentOnly === 'boolean' ? parsedFilters.currentOnly : DEFAULT_MODULE_FILTERS.currentOnly,
      offset: typeof savedOffset === 'number' && Number.isInteger(savedOffset) && savedOffset >= 0 ? savedOffset : DEFAULT_MODULE_FILTERS.offset,
    }
  } catch {
    return DEFAULT_MODULE_FILTERS
  }
}

function formatSemester(module: ModuleSummary) {
  if (!module.latest_year || !module.latest_semester) {
    return 'No latest term'
  }

  return `AY${module.latest_year}/${Number(module.latest_year) + 1} S${module.latest_semester}`
}

function formatAu(au: number | null) {
  if (au === null) {
    return 'AU unknown'
  }

  return `${au.toFixed(1)} AU`
}

function ModulesPage() {
  const savedFilters = useMemo(getSavedModuleFilters, [])
  const [modules, setModules] = useState<ModuleSummary[]>([])
  const [filterOptions, setFilterOptions] = useState<ModuleFilterOptions>({
    faculties: [],
    levels: [],
    categories: [],
  })
  const [selectedModule, setSelectedModule] = useState<ModuleSummary | null>(null)
  const [searchTerm, setSearchTerm] = useState(savedFilters.searchTerm)
  const [selectedFaculty, setSelectedFaculty] = useState(savedFilters.selectedFaculty)
  const [selectedLevel, setSelectedLevel] = useState(savedFilters.selectedLevel)
  const [selectedCategory, setSelectedCategory] = useState(savedFilters.selectedCategory)
  const [currentOnly, setCurrentOnly] = useState(savedFilters.currentOnly)
  const [offset, setOffset] = useState(savedFilters.offset)
  const [total, setTotal] = useState(0)
  const [isLoading, setIsLoading] = useState(false)
  const [isDetailLoading, setIsDetailLoading] = useState(false)
  const [isDetailOpen, setIsDetailOpen] = useState(false)
  const [error, setError] = useState('')

  const currentPage = Math.floor(offset / MODULE_PAGE_SIZE) + 1
  const totalPages = Math.max(1, Math.ceil(total / MODULE_PAGE_SIZE))

  const activeFilterCount = useMemo(() => {
    return [searchTerm, selectedFaculty, selectedLevel, selectedCategory, currentOnly ? 'current' : ''].filter(Boolean).length
  }, [currentOnly, searchTerm, selectedCategory, selectedFaculty, selectedLevel])

  useEffect(() => {
    async function loadFilterOptions() {
      try {
        const options = await fetchModuleFilters()
        setFilterOptions(options)
      } catch {
        setError('Could not load module filters. Make sure the backend is running.')
      }
    }

    void loadFilterOptions()
  }, [])

  useEffect(() => {
    async function loadModules() {
      try {
        setIsLoading(true)
        setError('')

        const response = await fetchModules({
          search: searchTerm.trim() || undefined,
          faculty: selectedFaculty || undefined,
          level: selectedLevel ? Number(selectedLevel) : undefined,
          category: selectedCategory || undefined,
          currentOnly,
          limit: MODULE_PAGE_SIZE,
          offset,
        })

        setModules(response.items)
        setTotal(response.total)
      } catch {
        setError('Could not load modules. Make sure the backend is running.')
      } finally {
        setIsLoading(false)
      }
    }

    void loadModules()
  }, [currentOnly, offset, searchTerm, selectedCategory, selectedFaculty, selectedLevel])

  useEffect(() => {
    window.localStorage.setItem(
      MODULE_FILTER_STORAGE_KEY,
      JSON.stringify({
        searchTerm,
        selectedFaculty,
        selectedLevel,
        selectedCategory,
        currentOnly,
        offset,
      }),
    )
  }, [currentOnly, offset, searchTerm, selectedCategory, selectedFaculty, selectedLevel])

  useEffect(() => {
    function closeOnEscape(event: KeyboardEvent) {
      if (event.key === 'Escape') {
        closeModuleDetail()
      }
    }

    if (isDetailOpen) {
      window.addEventListener('keydown', closeOnEscape)
    }

    return () => window.removeEventListener('keydown', closeOnEscape)
  }, [isDetailOpen])

  function resetFilters() {
    setSearchTerm(DEFAULT_MODULE_FILTERS.searchTerm)
    setSelectedFaculty(DEFAULT_MODULE_FILTERS.selectedFaculty)
    setSelectedLevel(DEFAULT_MODULE_FILTERS.selectedLevel)
    setSelectedCategory(DEFAULT_MODULE_FILTERS.selectedCategory)
    setCurrentOnly(DEFAULT_MODULE_FILTERS.currentOnly)
    setOffset(DEFAULT_MODULE_FILTERS.offset)
  }

  async function openModuleDetail(code: string) {
    try {
      setSelectedModule(null)
      setIsDetailOpen(true)
      setIsDetailLoading(true)
      const module = await fetchModuleByCode(code)
      setSelectedModule(module)
    } catch {
      setError(`Could not load details for ${code}.`)
    } finally {
      setIsDetailLoading(false)
    }
  }

  function closeModuleDetail() {
    setIsDetailOpen(false)
    setSelectedModule(null)
  }

  function handleFilterChange(updateFilter: () => void) {
    updateFilter()
    setOffset(0)
  }

  return (
    <section className="modules-page">
      <div className="modules-heading">
        <h2>NTU Modules</h2>
        <p>Search course details, pre-requisites, and modules can be taken next.</p>
      </div>

      <form className="modules-toolbar" onSubmit={(event) => event.preventDefault()}>
        <label className="modules-search">
          <span>Search modules</span>
          <input
            type="search"
            value={searchTerm}
            onChange={(event) => handleFilterChange(() => setSearchTerm(event.target.value))}
            placeholder="Type a course code or description"
          />
        </label>
        <label>
          <span>Faculty</span>
          <select value={selectedFaculty} onChange={(event) => handleFilterChange(() => setSelectedFaculty(event.target.value))}>
            <option value="">All faculties</option>
            {filterOptions.faculties.map((faculty) => (
              <option key={faculty} value={faculty}>
                {faculty}
              </option>
            ))}
          </select>
        </label>
        <label>
          <span>Level</span>
          <select value={selectedLevel} onChange={(event) => handleFilterChange(() => setSelectedLevel(event.target.value))}>
            <option value="">All levels</option>
            {filterOptions.levels.map((level) => (
              <option key={level} value={level}>
                Level {level}
              </option>
            ))}
          </select>
        </label>
        <label>
          <span>Category</span>
          <select value={selectedCategory} onChange={(event) => handleFilterChange(() => setSelectedCategory(event.target.value))}>
            <option value="">All categories</option>
            {filterOptions.categories.map((category) => (
              <option key={category} value={category}>
                {category}
              </option>
            ))}
          </select>
        </label>
        <label>
          <span>Availability</span>
          <select value={currentOnly ? 'current' : ''} onChange={(event) => handleFilterChange(() => setCurrentOnly(event.target.value === 'current'))}>
            <option value="">All semesters</option>
            <option value="current">Current semester only</option>
          </select>
        </label>
        <button type="button" className="modules-reset-button" onClick={resetFilters}>
          Reset filters
        </button>
      </form>

      <div className="modules-status-row">
        <span>{activeFilterCount} active filter{activeFilterCount === 1 ? '' : 's'}</span>
        <span className="modules-count-note">{total} matching modules</span>
        <span>Page {currentPage} of {totalPages}</span>
      </div>

      {error && <p className="modules-error">{error}</p>}
      {isLoading && <p className="modules-loading">Loading modules from PostgreSQL...</p>}

      {!isLoading && modules.length === 0 && (
        <div className="modules-empty">
          <h3>No modules found</h3>
          <p>Try clearing one filter or searching by a broader keyword.</p>
        </div>
      )}

      {isDetailOpen && (
        <div className="module-detail-overlay" onMouseDown={(event) => event.currentTarget === event.target && closeModuleDetail()}>
          <aside className="module-detail-panel" role="dialog" aria-modal="true" aria-label="Module details">
            {isDetailLoading && <p>Loading selected module...</p>}
            {!isDetailLoading && selectedModule && (
              <>
                <div className="module-detail-header">
                  <span>{selectedModule.code}</span>
                  <button type="button" onClick={closeModuleDetail}>
                    Close
                  </button>
                </div>
                <h3>{selectedModule.title}</h3>
                <p>{selectedModule.description ?? 'No description available yet.'}</p>
                <dl>
                  <div>
                    <dt>Prerequisites</dt>
                    <dd>{selectedModule.prerequisites.length > 0 ? selectedModule.prerequisites.join(', ') : 'None listed'}</dd>
                  </div>
                  <div>
                    <dt>Unlocks</dt>
                    <dd>{selectedModule.unlocks.length > 0 ? selectedModule.unlocks.join(', ') : 'None listed'}</dd>
                  </div>
                  <div>
                    <dt>Restrictions</dt>
                    <dd>{selectedModule.not_available_to_programme ?? 'None listed'}</dd>
                  </div>
                </dl>
              </>
            )}
          </aside>
        </div>
      )}

      <div className="modules-board">
        {modules.map((module) => (
          <button key={module.code} className="module-card" type="button" onClick={() => void openModuleDetail(module.code)}>
            <span className="module-card-code">{module.code}</span>
            <span className="module-card-title">{module.title}</span>
            <span className="module-card-meta">
              {formatAu(module.au)} · {module.faculty ?? 'Faculty unknown'} · {formatSemester(module)}
            </span>
            <span className="module-card-categories">
              {module.categories.slice(0, 3).map((category) => (
                <span key={category}>{category}</span>
              ))}
            </span>
            <span className="module-card-signals">
              <span>requires {module.prerequisite_count}</span>
              <span>unlocks {module.unlock_count}</span>
            </span>
          </button>
        ))}
      </div>

      <div className="modules-pagination">
        <button type="button" disabled={offset === 0} onClick={() => setOffset(Math.max(0, offset - MODULE_PAGE_SIZE))}>
          Previous
        </button>
        <button type="button" disabled={offset + MODULE_PAGE_SIZE >= total} onClick={() => setOffset(offset + MODULE_PAGE_SIZE)}>
          Next
        </button>
      </div>
    </section>
  )
}

export default ModulesPage
