import { useEffect, useState } from 'react'
import './App.css'
import { fetchRoadmap } from './api/roadmapApi'
import CourseList from './components/CourseList'
import RoadmapGraph from './components/RoadmapGraph'
import type { RoadmapResponse } from './types/roadmap'

// Main page component
function App() {
  // Values the page can update later; when updated, React refreshes the screen.
  // const [valueToRead, functionToUpdateValue] = useState(startingValue)
  const [roadmap, setRoadmap] = useState<RoadmapResponse | null>(null)
  const [error, setError] = useState<string | null>(null)
  const [searchTerm, setSearchTerm] = useState('')

  useEffect(() => {
    // Load roadmap data once when the app first renders.
    async function loadRoadmap() {
      try {
        const roadmapData = await fetchRoadmap()
        setRoadmap(roadmapData)
      } catch {
        setError('Could not load roadmap. Make sure the backend is running.')
      }
    }

    void loadRoadmap()
  }, [])

  // Normalize the user input so search is case-insensitive and ignores extra spaces.
  const normalizedSearchTerm = searchTerm.trim().toLowerCase()

  // Display courses matching the search term.
  const filteredCourses =
    roadmap?.nodes.filter((course) => {
      const courseCode = course.courseCode.toLowerCase()
      const title = course.title.toLowerCase()

      // Keep this course if either its code or title contains the search text.
      return (
        courseCode.includes(normalizedSearchTerm) ||
        title.includes(normalizedSearchTerm)
      )
    }) ?? []

  return (
    <main className="app-shell">
      <header className="app-header">
        <p className="app-eyebrow">Course roadmap planner</p>
        <h1>FYP Course Recommendation</h1>
        <p className="app-subtitle">
          Explore course progression, prerequisites, and semester placement.
        </p>
      </header>

      {/* Show this while the request is still pending. */}
      {!roadmap && !error && <p>Loading roadmap...</p>}

      {/* Show this if the request fails. */}
      {error && <p>{error}</p>}

      {/* Show roadmap content only after data has loaded successfully. */}
      {roadmap && (
        <>
          {/* Passes prereq r/s into RoadmapGraph */}
          <RoadmapGraph courses={roadmap.nodes} prerequisiteLinks={roadmap.edges} />

          {/* Search input updates searchTerm */}
          <label className="course-search">
            Search courses
            <input
              type="search"
              value={searchTerm}
              onChange={(event) => setSearchTerm(event.target.value)}
              placeholder="Search by code or title"
            />
          </label>

          {/* Display only the courses that match the current search term. */}
          <CourseList courses={filteredCourses} />
        </>
      )}
    </main>
  )
}

export default App
