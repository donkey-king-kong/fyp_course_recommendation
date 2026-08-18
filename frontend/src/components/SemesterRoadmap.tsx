import { useLayoutEffect, useRef, useState, type CSSProperties } from 'react'
import './SemesterRoadmap.css'
import type { CourseNode, RoadmapEdge } from '../types/roadmap'

// Pass courses and prerequisite links into this component
interface SemesterRoadmapProps {
  courses: CourseNode[]
  prerequisiteLinks: RoadmapEdge[]
}

// Shape used after grouping courses into curriculum rows
interface SemesterGroup {
  year: number
  semester: number
  courses: CourseNode[]
}

// SVG path data for one prerequisite arrow
interface ArrowPath {
  id: string
  d: string
  isHighlighted: boolean
  isDimmed: boolean
}

const YEAR_ACCENTS = ['#f59e0b', '#ec4899', '#8b5cf6', '#22d3ee']

// Turn course type text into a CSS class name like "Common-Core" to "common-core"
function getCourseTypeClass(type: string) {
  return type.toLowerCase().replaceAll(' ', '-')
}

// Convert a flat course list into rows such as Year 1 Sem 1, Year 1 Sem 2, etc
function groupCoursesBySemester(courses: CourseNode[]) {
  return courses.reduce<SemesterGroup[]>((groups, course) => {
    const existingGroup = groups.find(
      (group) => group.year === course.year && group.semester === course.semester,
    )

    if (existingGroup) {
      existingGroup.courses.push(course)
      return groups
    }

    return [
      ...groups,
      {
        year: course.year,
        semester: course.semester,
        courses: [course],
      },
    ]
  }, [])
}

// Show curriculum rows, course cards, prerequisite arrows, and hover emphasis
function SemesterRoadmap({ courses, prerequisiteLinks }: SemesterRoadmapProps) {
  // Track hover state so connected courses/arrows can be emphasized
  const [hoveredCourseId, setHoveredCourseId] = useState<string | null>(null)
  const [showAllArrows, setShowAllArrows] = useState(true)
  const [arrowPaths, setArrowPaths] = useState<ArrowPath[]>([])

  // Let us measure where each course card is on screen so SVG arrows can connect them
  const roadmapRef = useRef<HTMLDivElement | null>(null)
  const courseRefs = useRef<Record<string, HTMLElement | null>>({})

  // Sort rows so the roadmap follows curriculum order
  const semesterGroups = groupCoursesBySemester(courses).sort(
    (a, b) => a.year - b.year || a.semester - b.semester,
  )

  const connectedCourseIds = new Set<string>()

  // When hovering a course, keep that course and its direct prerequisite links visually active
  if (hoveredCourseId) {
    connectedCourseIds.add(hoveredCourseId)

    prerequisiteLinks.forEach((link) => {
      if (link.source === hoveredCourseId || link.target === hoveredCourseId) {
        connectedCourseIds.add(link.source)
        connectedCourseIds.add(link.target)
      }
    })
  }

  // Recalculate arrow paths after layout changes because arrows depend on actual card positions
  useLayoutEffect(() => {
    function updateArrowPaths() {
      const roadmapElement = roadmapRef.current

      if (!roadmapElement) {
        return
      }

      const roadmapRect = roadmapElement.getBoundingClientRect()

      const nextArrowPaths = prerequisiteLinks.flatMap((link) => {
        const sourceElement = courseRefs.current[link.source]
        const targetElement = courseRefs.current[link.target]

        // If no source or target course found, don't draw arrow
        if (!sourceElement || !targetElement) {
          return []
        }

        const sourceRect = sourceElement.getBoundingClientRect()
        const targetRect = targetElement.getBoundingClientRect()
        const startX = sourceRect.right - roadmapRect.left
        const startY = sourceRect.top + sourceRect.height / 2 - roadmapRect.top
        const endX = targetRect.left - roadmapRect.left
        const endY = targetRect.top + targetRect.height / 2 - roadmapRect.top
        const controlOffset = Math.max(80, Math.abs(endX - startX) * 0.45)
        const isHighlighted =
          hoveredCourseId === link.source || hoveredCourseId === link.target
        const shouldShow = showAllArrows || isHighlighted

        if (!shouldShow) {
          return []
        }

        return [
          {
            id: `${link.source}-${link.target}`,
            // Cubic curve from source card to target card.
            d: `M ${startX} ${startY} C ${startX + controlOffset} ${startY}, ${
              endX - controlOffset
            } ${endY}, ${endX} ${endY}`,
            isHighlighted,
            isDimmed: Boolean(hoveredCourseId) && !isHighlighted,
          },
        ]
      })

      setArrowPaths(nextArrowPaths)
    }

    // Calculate arrows after cards appear, then recalculate them if the window size changes
    const animationFrameId = window.requestAnimationFrame(updateArrowPaths)

    window.addEventListener('resize', updateArrowPaths)

    return () => {
      window.cancelAnimationFrame(animationFrameId)
      window.removeEventListener('resize', updateArrowPaths)
    }
  }, [hoveredCourseId, prerequisiteLinks, showAllArrows])

  return (
    <section className="semester-roadmap-section">
      <div className="semester-roadmap-header">
        <h2>Roadmap</h2>

        {/* Toggle between all prerequisite arrows and only the hovered course's arrows. */}
        <label className="arrow-toggle">
          All arrows
          <input
            type="checkbox"
            checked={showAllArrows}
            onChange={(event) => setShowAllArrows(event.target.checked)}
          />
        </label>
      </div>

      <div className="semester-roadmap" ref={roadmapRef}>
        {/* SVG overlay draws curved prerequisite arrows behind the course cards. */}
        <svg className="roadmap-arrows" aria-hidden="true">
          <defs>
            <marker
              id="roadmap-arrow"
              markerHeight="8"
              markerWidth="8"
              orient="auto"
              refX="7"
              refY="4"
            >
              <path d="M 0 0 L 8 4 L 0 8 z" />
            </marker>
          </defs>

          {arrowPaths.map((arrowPath) => (
            <path
              key={arrowPath.id}
              className={[
                'roadmap-arrow',
                arrowPath.isHighlighted ? 'roadmap-arrow-highlighted' : '',
                arrowPath.isDimmed ? 'roadmap-arrow-dimmed' : '',
              ]
                .filter(Boolean)
                .join(' ')}
              d={arrowPath.d}
            />
          ))}
        </svg>

        {/* Render each curriculum row: one year/semester label and its course cards. */}
        {semesterGroups.map((group) => {
          const yearAccent = YEAR_ACCENTS[(group.year - 1) % YEAR_ACCENTS.length]

          return (
            <section
              key={`${group.year}-${group.semester}`}
              className="semester-band"
              style={{ '--year-accent': yearAccent } as CSSProperties}
            >
              <div className="semester-label">
                <strong>Year {group.year}</strong>
                <span>Sem {group.semester}</span>
              </div>

              <div className="semester-courses">
                {group.courses.map((course) => {
                  const isConnected = connectedCourseIds.has(course.id)
                  const isDimmed = Boolean(hoveredCourseId) && !isConnected

                  return (
                    // Each card stores its DOM ref so arrow endpoints can be measured.
                    <article
                      key={course.id}
                      ref={(element) => {
                        courseRefs.current[course.id] = element
                      }}
                      className={[
                        'semester-course-card',
                        isConnected ? 'semester-course-card-connected' : '',
                        isDimmed ? 'semester-course-card-dimmed' : '',
                      ]
                        .filter(Boolean)
                        .join(' ')}
                      onMouseEnter={() => setHoveredCourseId(course.id)}
                      onMouseLeave={() => setHoveredCourseId(null)}
                    >
                      <div className="semester-course-card-top">
                        <strong>{course.courseCode}</strong>
                        <span>{course.academicUnits}AU</span>
                      </div>
                      <p>{course.title}</p>
                      <div className="semester-course-card-bottom">
                        <span
                          className={`semester-course-type ${getCourseTypeClass(
                            course.type,
                          )}`}
                        >
                          {course.type}
                        </span>
                        <span
                          className={[
                            'completion-indicator',
                            course.isCompleted ? 'completion-indicator-checked' : '',
                          ]
                            .filter(Boolean)
                            .join(' ')}
                          aria-label={
                            course.isCompleted ? 'Completed course' : 'Incomplete course'
                          }
                        />
                      </div>
                    </article>
                  )
                })}
              </div>
            </section>
          )
        })}
      </div>
    </section>
  )
}

export default SemesterRoadmap
