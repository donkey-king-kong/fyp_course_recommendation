import { useEffect, useState } from 'react'
import './App.css'
import CourseList from './components/CourseList'
import LoginPage from './components/LoginPage'
import ModulesPage from './components/ModulesPage'
import SemesterRoadmap from './components/SemesterRoadmap'
import ProfilePage from './components/ProfilePage'
import { fetchRecommendations } from './api/recommendationsApi'
import { fetchPersonalizedRoadmap } from './api/roadmapApi'
import { useProfileStore } from './store/useProfileStore'
import type { CurriculumGuideResponse } from './types/curriculum'
import type { RoadmapResponse } from './types/roadmap'
import type { RoadmapRecommendationStaleReason } from './store/useProfileStore'

type ViewState = 'roadmap' | 'modules' | 'profile'

const VIEW_STORAGE_KEY = 'ntu-course-recommender-current-view'
const DEFAULT_VIEW: ViewState = 'roadmap'
const VALID_VIEWS: ViewState[] = ['roadmap', 'modules', 'profile']
const EMPTY_RECOMMENDATION_TAGS: string[] = []

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

function getChoiceSlotCode(course: CurriculumGuideResponse['nodes'][number]) {
  return course.isChoiceSlot ? course.courseCode : null
}

// Backend owns final slot assignment, so request one recommendation per open slot.
function getRecommendationLimit(openChoiceSlots: CurriculumGuideResponse['nodes']) {
  return Math.max(1, openChoiceSlots.length)
}

function getRecommendationNotice(
  staleReasons: RoadmapRecommendationStaleReason[],
  hasRecommendations: boolean,
) {
  if (!hasRecommendations || staleReasons.length === 0) {
    return ''
  }

  const changedInputs = staleReasons
    .map((reason) => {
      if (reason === 'curriculum-guide') {
        return 'Curriculum guide'
      }

      if (reason === 'transcript') {
        return 'Transcript'
      }

      return 'Completed courses'
    })
    .join(' and ')

  return `${changedInputs} changed. Reload or clear recommendations.`
}

// Main page component
function App() {
  const [searchTerm, setSearchTerm] = useState('')
  const [theme, setTheme] = useState<'light' | 'dark'>('light') // Toggle Button
  const [currentView, setCurrentView] = useState<ViewState>(getInitialView)
  const [isLoadingRecommendations, setIsLoadingRecommendations] = useState(false)
  const [recommendationError, setRecommendationError] = useState('')
  const [roadmap, setRoadmap] = useState<RoadmapResponse | null>(null)
  const [roadmapProjectionError, setRoadmapProjectionError] = useState('')
  const activeStudentId = useProfileStore((state) => state.activeStudentId)
  const curriculumGuide = useProfileStore((state) => state.curriculumGuide)
  const completedCourseIds = useProfileStore((state) => state.completedCourseIds)
  const profile = useProfileStore((state) => state.profile)
  const preferredRecommendationTags = profile.preferredRecommendationTags ?? EMPTY_RECOMMENDATION_TAGS
  const transcriptCompletedCourseCodes = useProfileStore(
    (state) => state.transcriptCompletedCourseCodes,
  )
  const transcriptCompletedCourses = useProfileStore((state) => state.transcriptCompletedCourses)
  const transcriptUnmatchedCourseCodes = useProfileStore(
    (state) => state.transcriptUnmatchedCourseCodes,
  )
  const recommendations = useProfileStore((state) => state.roadmapRecommendations)
  const roadmapRecommendationStaleReasons = useProfileStore(
    (state) => state.roadmapRecommendationStaleReasons,
  )
  const setRoadmapRecommendations = useProfileStore((state) => state.setRoadmapRecommendations)
  const clearRoadmapRecommendations = useProfileStore((state) => state.clearRoadmapRecommendations)
  const logout = useProfileStore((state) => state.logout)
  const hasLoadedRoadmapRecommendations = recommendations.length > 0
  const recommendationNotice = getRecommendationNotice(
    roadmapRecommendationStaleReasons,
    hasLoadedRoadmapRecommendations,
  )

  useEffect(() => {
    window.localStorage.setItem(VIEW_STORAGE_KEY, currentView)
  }, [currentView])

  useEffect(() => {
    setRecommendationError('')
  }, [
    curriculumGuide,
    profile.careerGoal,
    preferredRecommendationTags,
    transcriptCompletedCourseCodes,
  ])

  useEffect(() => {
    let shouldIgnoreResult = false

    async function loadPersonalizedRoadmap() {
      if (!curriculumGuide) {
        setRoadmap(null)
        setRoadmapProjectionError('')
        return
      }

      try {
        const result = await fetchPersonalizedRoadmap(
          curriculumGuide,
          transcriptCompletedCourses,
          transcriptUnmatchedCourseCodes,
        )

        if (!shouldIgnoreResult) {
          setRoadmap(result)
          setRoadmapProjectionError('')
        }
      } catch {
        if (!shouldIgnoreResult) {
          setRoadmap(null)
          setRoadmapProjectionError('Could not build your personalized roadmap. Make sure the backend is running.')
        }
      }
    }

    void loadPersonalizedRoadmap()

    return () => {
      shouldIgnoreResult = true
    }
  }, [curriculumGuide, transcriptCompletedCourses, transcriptUnmatchedCourseCodes])

  // Normalize the user input so search is case-insensitive and ignores extra spaces.
  const normalizedSearchTerm = searchTerm.trim().toLowerCase()

  // Display only the uploaded curriculum guide courses, without transcript placement overrides.
  const filteredCourses =
    curriculumGuide?.nodes.map((course) => ({
      ...course,
      title: getCurriculumCourseTitle(course),
    })).filter((course) => {
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

    if (!roadmap) {
      setRecommendationError('The uploaded curriculum guide could not be converted into a roadmap.')
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
    const choiceSlots = openChoiceSlots.flatMap((course) => {
      const courseCode = getChoiceSlotCode(course)

      if (!courseCode) {
        return []
      }

      return [
        {
          slotId: course.id,
          courseCode,
          year: course.year,
          semester: course.semester,
        },
      ]
    })
    const curriculumCourses = roadmap.nodes.map((course) => ({
      nodeId: course.id,
      courseCode: course.courseCode,
      title: course.title,
      year: course.year,
      semester: course.semester,
      isChoiceSlot: Boolean(course.isChoiceSlot),
    }))
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
      clearRoadmapRecommendations()

      const result = await fetchRecommendations({
        careerGoal: profile.careerGoal,
        preferredRecommendationTags,
        studentFaculty: profile.major,
        completedCourseCodes,
        choiceSlotCodes,
        choiceSlots,
        curriculumCourses,
        excludedCourseCodes,
        excludedCourseTitles,
        limit: getRecommendationLimit(openChoiceSlots),
      })

      setRoadmapRecommendations(result.recommendations)
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
          {roadmapProjectionError && (
            <p className="roadmap-recommendation-error">{roadmapProjectionError}</p>
          )}
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
            recommendationNotice={recommendationNotice}
            onClearRecommendations={clearRoadmapRecommendations}
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
          hasLoadedRoadmap={hasLoadedRoadmapRecommendations}
          recommendationError={recommendationError}
          recommendationNotice={recommendationNotice}
          onGoToRoadmap={() => setCurrentView('roadmap')}
          onLoadRoadmap={handleLoadRoadmapRecommendations}
          onClearRecommendations={clearRoadmapRecommendations}
        />
      )}
    </main>
  )
}

export default App
