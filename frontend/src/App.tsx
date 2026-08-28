import { useEffect, useMemo, useState } from 'react'
import './App.css'
import CourseList from './components/CourseList'
import LoginPage from './components/LoginPage'
import ModulesPage from './components/ModulesPage'
import SemesterRoadmap from './components/SemesterRoadmap'
import ProfilePage from './components/ProfilePage'
import { fetchModuleByCode } from './api/modulesApi'
import { fetchRecommendations } from './api/recommendationsApi'
import { useProfileStore } from './store/useProfileStore'
import type { CurriculumGuideResponse } from './types/curriculum'
import type { ModuleSummary } from './types/module'
import type { CourseRecommendation } from './types/recommendation'
import type { CourseNode, RoadmapEdge, RoadmapResponse } from './types/roadmap'

type ViewState = 'roadmap' | 'modules' | 'profile'

const VIEW_STORAGE_KEY = 'ntu-course-recommender-current-view'
const DEFAULT_VIEW: ViewState = 'roadmap'
const VALID_VIEWS: ViewState[] = ['roadmap', 'modules', 'profile']

function getCurriculumCourseTitle(course: CurriculumGuideResponse['nodes'][number]) {
  if (course.courseCode === 'BDE' || course.type === 'BDE') {
    return 'Broadening and Deepening Electives'
  }

  if (course.isChoiceSlot && course.courseCode.includes('xxx') && course.type.includes('MPE')) {
    return 'Major Prescribed Elective'
  }

  return course.title
}

// Reads the last selected tab from localStorage so reloads stay on the same page.
function getInitialView(): ViewState {
  const storedView = window.localStorage.getItem(VIEW_STORAGE_KEY)

  if (VALID_VIEWS.includes(storedView as ViewState)) {
    return storedView as ViewState
  }

  return DEFAULT_VIEW
}

function createEdgeKey(edge: RoadmapEdge) {
  return `${edge.source}->${edge.target}`
}

function getNodeIdsByCourseCode(nodes: CourseNode[]) {
  return nodes.reduce<Record<string, string[]>>((map, node) => {
    const courseCode = node.courseCode.toUpperCase()

    return {
      ...map,
      [courseCode]: [...(map[courseCode] ?? []), node.id],
    }
  }, {})
}

function createFallbackTranscriptModule(courseCode: string): ModuleSummary {
  return {
    code: courseCode,
    title: 'Completed transcript module',
    au: null,
    faculty: null,
    description: null,
    level: null,
    categories: [],
    latest_year: null,
    latest_semester: null,
    is_current_semester: false,
    not_available_to_programme: null,
    prerequisites: [],
    unlocks: [],
    prerequisite_count: 0,
    unlock_count: 0,
  }
}

function getPrerequisitesByTarget(edges: RoadmapEdge[]) {
  return edges.reduce<Record<string, string[]>>((map, edge) => {
    return {
      ...map,
      [edge.target]: [...(map[edge.target] ?? []), edge.source],
    }
  }, {})
}

// Convert the uploaded curriculum guide shape into the existing roadmap component shape.
function mapCurriculumGuideToRoadmap(
  curriculumGuide: CurriculumGuideResponse,
  transcriptOnlyModules: ModuleSummary[],
): RoadmapResponse {
  const curriculumNodes: CourseNode[] = curriculumGuide.nodes.map((course) => ({
    id: course.id,
    courseCode: course.courseCode,
    title: getCurriculumCourseTitle(course),
    type: course.type,
    year: course.year,
    semester: course.semester,
    academicUnits: course.academicUnits,
    prerequisites: curriculumGuide.edges
      .filter((edge) => edge.target === course.id)
      .map((edge) => edge.source),
    prerequisiteText: course.prerequisiteText,
    isCompleted: false,
    isChoiceSlot: course.isChoiceSlot,
    isTranscriptOnly: false,
    jobSkills: [],
  }))
  // Transcript-only modules are shown separately so they do not replace official curriculum slots.
  const transcriptNodes: CourseNode[] = transcriptOnlyModules.map((module) => ({
    id: `transcript-${module.code.toLowerCase()}`,
    courseCode: module.code,
    title: module.title,
    type: 'Transcript',
    year: 0,
    semester: 0,
    academicUnits: module.au ?? 0,
    prerequisites: [],
    prerequisiteText: module.prerequisites.join(', '),
    isCompleted: true,
    isChoiceSlot: false,
    isTranscriptOnly: true,
    jobSkills: [],
  }))
  const nodes = [...transcriptNodes, ...curriculumNodes]
  const nodeIdsByCourseCode = getNodeIdsByCourseCode(nodes)
  const transcriptEdges = transcriptOnlyModules.flatMap((module) => {
    const transcriptNodeId = `transcript-${module.code.toLowerCase()}`
    const prerequisiteEdges = module.prerequisites.flatMap((prerequisiteCode) =>
      (nodeIdsByCourseCode[prerequisiteCode.toUpperCase()] ?? []).map((prerequisiteNodeId) => ({
        source: prerequisiteNodeId,
        target: transcriptNodeId,
      })),
    )
    const unlockEdges = module.unlocks.flatMap((unlockCode) =>
      (nodeIdsByCourseCode[unlockCode.toUpperCase()] ?? []).map((unlockNodeId) => ({
        source: transcriptNodeId,
        target: unlockNodeId,
      })),
    )

    return [...prerequisiteEdges, ...unlockEdges]
  })
  const edges = [...curriculumGuide.edges, ...transcriptEdges].filter(
    (edge, index, allEdges) =>
      allEdges.findIndex((candidate) => createEdgeKey(candidate) === createEdgeKey(edge)) === index,
  )
  const prerequisitesByTarget = getPrerequisitesByTarget(edges)
  const nodesWithUpdatedPrerequisites = nodes.map((node) => ({
    ...node,
    prerequisites: prerequisitesByTarget[node.id] ?? [],
  }))

  return { nodes: nodesWithUpdatedPrerequisites, edges }
}

function getChoiceSlotCode(course: CurriculumGuideResponse['nodes'][number]) {
  return course.isChoiceSlot ? course.courseCode : null
}

// Size the recommendation pool from actual slot demand, not just unique slot labels.
// BDE needs more candidates because duplicates, wrong-year levels, and prerequisites can be skipped.
function getRecommendationLimit(openChoiceSlots: CurriculumGuideResponse['nodes']) {
  const bdeSlotCount = openChoiceSlots.filter(
    (course) => course.courseCode === 'BDE' || course.type === 'BDE',
  ).length
  const mpeSlotCount = openChoiceSlots.filter(
    (course) => course.courseCode !== 'BDE' && course.type !== 'BDE',
  ).length

  return Math.min(120, Math.max(24, bdeSlotCount * 18 + mpeSlotCount * 10))
}

// Main page component
function App() {
  const [searchTerm, setSearchTerm] = useState('')
  const [theme, setTheme] = useState<'light' | 'dark'>('light') // Toggle Button
  const [currentView, setCurrentView] = useState<ViewState>(getInitialView)
  const [isLoadingRecommendations, setIsLoadingRecommendations] = useState(false)
  const [recommendationError, setRecommendationError] = useState('')
  const [recommendations, setRecommendations] = useState<CourseRecommendation[]>([])
  const [transcriptOnlyModules, setTranscriptOnlyModules] = useState<ModuleSummary[]>([])
  const activeStudentId = useProfileStore((state) => state.activeStudentId)
  const curriculumGuide = useProfileStore((state) => state.curriculumGuide)
  const completedCourseIds = useProfileStore((state) => state.completedCourseIds)
  const profile = useProfileStore((state) => state.profile)
  const transcriptCompletedCourseCodes = useProfileStore(
    (state) => state.transcriptCompletedCourseCodes,
  )
  const transcriptUnmatchedCourseCodes = useProfileStore(
    (state) => state.transcriptUnmatchedCourseCodes,
  )
  const logout = useProfileStore((state) => state.logout)

  useEffect(() => {
    window.localStorage.setItem(VIEW_STORAGE_KEY, currentView)
  }, [currentView])

  const roadmap = useMemo(
    () => (
      curriculumGuide ? mapCurriculumGuideToRoadmap(curriculumGuide, transcriptOnlyModules) : null
    ),
    [curriculumGuide, transcriptOnlyModules],
  )

  useEffect(() => {
    let shouldIgnoreResult = false

    async function loadTranscriptOnlyModules() {
      if (!curriculumGuide || transcriptUnmatchedCourseCodes.length === 0) {
        setTranscriptOnlyModules([])
        return
      }

      const loadedModules = await Promise.all(
        transcriptUnmatchedCourseCodes.map(async (courseCode) => {
          try {
            return await fetchModuleByCode(courseCode)
          } catch {
            return createFallbackTranscriptModule(courseCode)
          }
        }),
      )

      if (!shouldIgnoreResult) {
        setTranscriptOnlyModules(loadedModules)
      }
    }

    void loadTranscriptOnlyModules()

    return () => {
      shouldIgnoreResult = true
    }
  }, [curriculumGuide, transcriptUnmatchedCourseCodes])

  // Normalize the user input so search is case-insensitive and ignores extra spaces.
  const normalizedSearchTerm = searchTerm.trim().toLowerCase()

  // Display uploaded curriculum courses matching the search term.
  const filteredCourses =
    roadmap?.nodes.filter((course) => {
      if (course.isTranscriptOnly) {
        return false
      }

      const courseCode = course.courseCode.toLowerCase()
      const title = course.title.toLowerCase()

      // Keep this course if either its code or title contains the search text.
      return (
        courseCode.includes(normalizedSearchTerm) ||
        title.includes(normalizedSearchTerm)
      )
    }) ?? []

  // Show the login page until a studentID is entered
  if (!activeStudentId) {
    return <LoginPage />
  }

  function handleLogout() {
    setCurrentView(DEFAULT_VIEW)
    logout()
  }

  async function handleLoadRoadmapRecommendations() {
    if (!curriculumGuide) {
      setRecommendationError('Upload a curriculum guide before loading the roadmap.')
      return
    }

    if (profile.careerGoal !== 'software-engineer') {
      setRecommendationError('Select Software Engineer before loading the roadmap.')
      return
    }

    const completedRoadmapCourseCodes = curriculumGuide.nodes
      .filter((course) => completedCourseIds.includes(course.id))
      .map((course) => course.courseCode)
    const completedCourseCodes = [
      ...new Set([...transcriptCompletedCourseCodes, ...completedRoadmapCourseCodes]),
    ]
    // Send only uncompleted choice slots; the roadmap decides which slots can display results.
    const openChoiceSlots = curriculumGuide.nodes.filter(
      (course) => course.isChoiceSlot && !completedCourseIds.includes(course.id),
    )
    const choiceSlotCodes = [
      ...new Set(
        openChoiceSlots
          .map((course) => getChoiceSlotCode(course))
          .filter((courseCode): courseCode is string => Boolean(courseCode)),
      ),
    ]
    const fixedCurriculumCourses = curriculumGuide.nodes.filter((course) => !course.isChoiceSlot)
    const excludedCourseCodes = fixedCurriculumCourses.map((course) => course.courseCode)
    const excludedCourseTitles = fixedCurriculumCourses.map((course) => course.title)

    if (choiceSlotCodes.length === 0) {
      setRecommendationError('No open choice slots were found in the uploaded curriculum guide.')
      return
    }

    try {
      setIsLoadingRecommendations(true)
      setRecommendationError('')
      setRecommendations([])

      const result = await fetchRecommendations({
        careerGoal: profile.careerGoal,
        completedCourseCodes,
        choiceSlotCodes,
        excludedCourseCodes,
        excludedCourseTitles,
        limit: getRecommendationLimit(openChoiceSlots),
      })

      setRecommendations(result.recommendations)
    } catch {
      setRecommendationError('Could not load recommendations. Make sure the backend is running.')
    } finally {
      setIsLoadingRecommendations(false)
    }
  }

  return (
    <main className="app-shell" data-theme={theme}>
      <header className="app-header">
        <div className="app-header-top">
          <nav className="app-nav">
            <button
              className={`nav-button ${currentView === 'roadmap' ? 'active' : ''}`}
              onClick={() => setCurrentView('roadmap')}
            >
              Roadmap
            </button>
            <button
              className={`nav-button ${currentView === 'modules' ? 'active' : ''}`}
              onClick={() => setCurrentView('modules')}
            >
              Modules
            </button>
            <button
              className={`nav-button ${currentView === 'profile' ? 'active' : ''}`}
              onClick={() => setCurrentView('profile')}
            >
              Profile
            </button>
            <button className="nav-button logout-button" onClick={handleLogout}>
              Log out
            </button>
          </nav>
          <label className="theme-switch"> 
            {/* Moon icon for the theme toggle. */}
            <span className="theme-switch-icon" aria-hidden="true">
              ☾
            </span>
            <input
              type="checkbox"
              aria-label="Toggle dark mode"
              checked={theme === 'dark'}
              onChange={(event) => setTheme(event.target.checked ? 'dark' : 'light')}
            />
            <span className="theme-switch-control" />
          </label>
        </div>
        <div className="app-header-copy">
          <h1>NTU Course Recommender</h1>
          <p className="app-subtitle">
            Get your course roadmap to plan your NTU journey.
          </p>
        </div>
      </header>

      {currentView === 'roadmap' && !roadmap && (
        <section className="roadmap-empty-state">
          <h2>Upload Your Curriculum Guide</h2>
          <p>
            Your roadmap will be generated from your uploaded curriculum guide. Go to Profile and
            upload the PDF before planning courses.
          </p>
          <button type="button" onClick={() => setCurrentView('profile')}>
            Go to Profile
          </button>
        </section>
      )}

      {/* Show roadmap content only after a curriculum guide exists for this profile. */}
      {roadmap && currentView === 'roadmap' && (
        <>
          {/* Shows the curriculum-style roadmap with semester bands and prerequisite arrows. */}
          <SemesterRoadmap
            courses={roadmap.nodes}
            prerequisiteLinks={roadmap.edges}
            recommendations={recommendations}
            isLoadingRecommendations={isLoadingRecommendations}
            recommendationError={recommendationError}
          />

          {/* Search input updates searchTerm */}
          <label className="course-search">
            Search curriculum guide
            <input
              type="search"
              value={searchTerm}
              onChange={(event) => setSearchTerm(event.target.value)}
              placeholder="Search curriculum courses by code or title"
            />
          </label>

          {/* Display only the courses that match the current search term. */}
          <CourseList courses={filteredCourses} />
        </>
      )}

      {currentView === 'modules' && <ModulesPage />}

      {/* Show profile page when selected */}
      {currentView === 'profile' && (
        <ProfilePage
          isLoadingRoadmap={isLoadingRecommendations}
          recommendationError={recommendationError}
          onGoToRoadmap={() => setCurrentView('roadmap')}
          onLoadRoadmap={handleLoadRoadmapRecommendations}
        />
      )}
    </main>
  )
}

export default App
