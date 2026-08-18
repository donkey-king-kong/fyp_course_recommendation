import { useEffect, useState } from 'react'
import './App.css'
import { fetchRoadmap } from './api/roadmapApi'
import CourseList from './components/CourseList'
import type { RoadmapResponse } from './types/roadmap'

function App() {
  const [roadmap, setRoadmap] = useState<RoadmapResponse | null>(null)
  const [error, setError] = useState<string | null>(null)
  const [searchTerm, setSearchTerm] = useState('')

  useEffect(() => {
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

  const firstCourseCode = roadmap?.nodes[0]?.courseCode ?? 'None'
  const normalizedSearchTerm = searchTerm.trim().toLowerCase()
  const filteredCourses =
    roadmap?.nodes.filter((course) => {
      const courseCode = course.courseCode.toLowerCase()
      const title = course.title.toLowerCase()

      return (
        courseCode.includes(normalizedSearchTerm) ||
        title.includes(normalizedSearchTerm)
      )
    }) ?? []

  return (
    <main className="app-shell">
      <h1>FYP Course Recommendation</h1>

      {!roadmap && !error && <p>Loading roadmap...</p>}

      {error && <p>{error}</p>}

      {roadmap && (
        <>
          <section className="roadmap-summary">
            <h2>Roadmap loaded</h2>
            <p>Courses: {roadmap.nodes.length}</p>
            <p>Prerequisite links: {roadmap.edges.length}</p>
            <p>First course: {firstCourseCode}</p>
          </section>

          <label className="course-search">
            Search courses
            <input
              type="search"
              value={searchTerm}
              onChange={(event) => setSearchTerm(event.target.value)}
              placeholder="Search by code or title"
            />
          </label>

          <CourseList courses={filteredCourses} />
        </>
      )}
    </main>
  )
}

export default App
