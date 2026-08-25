import { useEffect, useMemo, useState } from 'react'
import { fetchModuleByCode, fetchModuleFilters, fetchModules } from '../api/modulesApi'
import type { ModuleFilterOptions, ModuleSummary } from '../types/module'
import './ModulesPage.css'

const MODULE_PAGE_SIZE = 24

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
  const [modules, setModules] = useState<ModuleSummary[]>([])
  const [filterOptions, setFilterOptions] = useState<ModuleFilterOptions>({
    faculties: [],
    levels: [],
    categories: [],
  })
  const [selectedModule, setSelectedModule] = useState<ModuleSummary | null>(null)
  const [searchTerm, setSearchTerm] = useState('')
  const [selectedFaculty, setSelectedFaculty] = useState('')
  const [selectedLevel, setSelectedLevel] = useState('')
  const [selectedCategory, setSelectedCategory] = useState('')
  const [currentOnly, setCurrentOnly] = useState(true)
  const [offset, setOffset] = useState(0)
  const [total, setTotal] = useState(0)
  const [isLoading, setIsLoading] = useState(false)
  const [isDetailLoading, setIsDetailLoading] = useState(false)
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

  function resetFilters() {
    setSearchTerm('')
    setSelectedFaculty('')
    setSelectedLevel('')
    setSelectedCategory('')
    setCurrentOnly(true)
    setOffset(0)
  }

  async function openModuleDetail(code: string) {
    try {
      setIsDetailLoading(true)
      const module = await fetchModuleByCode(code)
      setSelectedModule(module)
    } catch {
      setError(`Could not load details for ${code}.`)
    } finally {
      setIsDetailLoading(false)
    }
  }

  function handleFilterChange(updateFilter: () => void) {
    updateFilter()
    setOffset(0)
  }

  return (
    <section className="modules-page">
      <div className="modules-hero">
        <div>
          <p className="modules-eyebrow"></p>
          <h2>NTU Modules</h2>
          <p>
            Browse NTU modules. Each card shows the module, its pre-requisites and what modules can be taken next.
          </p>
        </div>
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
        <label className="modules-current-toggle">
          <input
            type="checkbox"
            checked={currentOnly}
            onChange={(event) => handleFilterChange(() => setCurrentOnly(event.target.checked))}
          />
          <span>Current semester only</span>
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

      <aside className="module-detail-panel">
        {isDetailLoading && <p>Loading selected module...</p>}
        {!isDetailLoading && selectedModule && (
          <>
            <div className="module-detail-header">
              <span>{selectedModule.code}</span>
              <button type="button" onClick={() => setSelectedModule(null)}>
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
        {!isDetailLoading && !selectedModule && (
          <div className="module-detail-empty">
            <span>Signal detail</span>
            <p>Select a module card to inspect prerequisites, unlocks, and restrictions.</p>
          </div>
        )}
      </aside>
    </section>
  )
}

export default ModulesPage
