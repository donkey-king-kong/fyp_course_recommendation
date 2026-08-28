import { useLayoutEffect, useRef, useState, useEffect, type CSSProperties } from 'react'
import './SemesterRoadmap.css'
import type { CourseNode, RoadmapEdge } from '../types/roadmap'
import { useProfileStore } from '../store/useProfileStore'
import type { StandingRequirement } from '../types/curriculum'
import type { CourseRecommendation, RecommendationPrerequisite } from '../types/recommendation'
import ClassicLoader from './ClassicLoader'

// Pass courses and prerequisite links into this component
interface SemesterRoadmapProps {
  courses: CourseNode[]
  prerequisiteLinks: RoadmapEdge[]
  recommendations: CourseRecommendation[]
  isLoadingRecommendations: boolean
  recommendationError: string
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

type CourseEligibilityStatus = 'completed' | 'available' | 'locked'

interface CourseEligibility {
  status: CourseEligibilityStatus
  missingPrerequisites: string[]
}

interface ChoiceSlotCandidate {
  course: CourseNode
  slotKey: string
}

interface AssignedRecommendation {
  courseCode: string
  title: string
  label: string
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

function shouldIgnorePrerequisiteText(course: CourseNode) {
  const prerequisiteText = course.prerequisiteText?.trim().toLowerCase() ?? ''

  return (
    !prerequisiteText ||
    prerequisiteText === 'nil' ||
    course.courseCode === 'BDE' ||
    course.type === 'BDE' ||
    prerequisiteText.includes('refer to class schedule')
  )
}

function getStandingYear(prerequisiteText?: string) {
  const standingMatch = prerequisiteText?.match(/\byear\s+([2-4])\s+standing\b/i)

  return standingMatch ? parseInt(standingMatch[1], 10) : null
}

function getChoiceSlotKey(course: CourseNode) {
  const courseCode = course.courseCode.toUpperCase()

  if (!course.isChoiceSlot) {
    return null
  }

  if (courseCode === 'BDE') {
    return 'BDE'
  }

  const mpeMatch = courseCode.match(/^SC([3-4])XXX$/)

  return mpeMatch ? `SC${mpeMatch[1]}xxx` : course.courseCode
}

function getPreferredBdeLevel(year: number) {
  return Math.min(Math.max(year, 1), 4)
}

function getSemesterOrder(course: CourseNode) {
  return (course.year - 1) * 2 + course.semester
}

function canFitRecommendationInSlot(
  choiceSlot: ChoiceSlotCandidate,
  recommendation: CourseRecommendation | RecommendationPrerequisite,
) {
  if (choiceSlot.slotKey.toUpperCase() === 'BDE') {
    return true
  }

  return recommendation.faculty === 'CSC' && choiceSlot.slotKey === `SC${recommendation.level}xxx`
}

function sortRecommendationsForSlot(
  choiceSlot: ChoiceSlotCandidate,
  recommendations: CourseRecommendation[],
) {
  if (choiceSlot.slotKey.toUpperCase() !== 'BDE') {
    return [...recommendations].sort(
      (first, second) => second.score - first.score || first.courseCode.localeCompare(second.courseCode),
    )
  }

  const preferredLevel = getPreferredBdeLevel(choiceSlot.course.year)

  return [...recommendations].sort((first, second) => {
    const firstLevelGap = Math.abs((first.level ?? preferredLevel) - preferredLevel)
    const secondLevelGap = Math.abs((second.level ?? preferredLevel) - preferredLevel)

    return (
      firstLevelGap - secondLevelGap ||
      second.score - first.score ||
      first.courseCode.localeCompare(second.courseCode)
    )
  })
}

function assignRecommendationsToChoiceSlots(
  choiceSlots: ChoiceSlotCandidate[],
  recommendations: CourseRecommendation[],
) {
  const usedCourseCodes = new Set<string>()
  const sortedChoiceSlots = [...choiceSlots].sort(
    (first, second) =>
      getSemesterOrder(first.course) - getSemesterOrder(second.course) ||
      first.course.id.localeCompare(second.course.id),
  )

  return sortedChoiceSlots.reduce<Record<string, AssignedRecommendation>>((assignments, choiceSlot) => {
    if (assignments[choiceSlot.course.id]) {
      return assignments
    }

    const matchingRecommendations = recommendations.filter(
      (recommendation) =>
        recommendation.matchedChoiceSlot.toUpperCase() === choiceSlot.slotKey.toUpperCase() &&
        !usedCourseCodes.has(recommendation.courseCode),
    )

    for (const recommendation of sortRecommendationsForSlot(choiceSlot, matchingRecommendations)) {
      if (recommendation.missingPrerequisites.length === 0) {
        usedCourseCodes.add(recommendation.courseCode)

        return {
          ...assignments,
          [choiceSlot.course.id]: {
            courseCode: recommendation.courseCode,
            title: recommendation.title,
            label: 'Recommended option',
          },
        }
      }

      const prerequisite = recommendation.prerequisiteRecommendations[0]
      const previousSlot = sortedChoiceSlots.find(
        (slot) =>
          getSemesterOrder(slot.course) === getSemesterOrder(choiceSlot.course) - 1 &&
          !assignments[slot.course.id] &&
          canFitRecommendationInSlot(slot, prerequisite),
      )

      if (recommendation.missingPrerequisites.length !== 1 || !prerequisite || !previousSlot) {
        continue
      }

      usedCourseCodes.add(prerequisite.courseCode)
      usedCourseCodes.add(recommendation.courseCode)

      return {
        ...assignments,
        [previousSlot.course.id]: {
          courseCode: prerequisite.courseCode,
          title: prerequisite.title,
          label: `Prerequisite for ${recommendation.courseCode}`,
        },
        [choiceSlot.course.id]: {
          courseCode: recommendation.courseCode,
          title: recommendation.title,
          label: 'Recommended option',
        },
      }
    }

    return assignments
  }, {})
}

function getMissingStandingRequirement(
  course: CourseNode,
  completedAcademicUnits: number,
  standingRequirements: StandingRequirement[],
) {
  if (shouldIgnorePrerequisiteText(course)) {
    return null
  }

  const standingYear = getStandingYear(course.prerequisiteText)

  if (!standingYear) {
    return course.prerequisiteText ?? 'Prerequisite required'
  }

  const standingRequirement = standingRequirements.find(
    (requirement) => requirement.standingYear === standingYear,
  )

  if (!standingRequirement) {
    return course.prerequisiteText ?? `Year ${standingYear} standing`
  }

  if (completedAcademicUnits >= standingRequirement.minimumAcademicUnits) {
    return null
  }

  return `Year ${standingYear} standing requires ${standingRequirement.minimumAcademicUnits} AU; you have ${completedAcademicUnits} AU`
}

// A course is available when every listed prerequisite is already completed.
function getCourseEligibility(
  course: CourseNode,
  completedCourseIds: string[],
  completedAcademicUnits: number,
  standingRequirements: StandingRequirement[],
): CourseEligibility {
  if (completedCourseIds.includes(course.id)) {
    return {
      status: 'completed',
      missingPrerequisites: [],
    }
  }

  const missingPrerequisites = course.prerequisites.filter(
    (prerequisiteId) => !completedCourseIds.includes(prerequisiteId),
  )
  const missingStandingRequirement = getMissingStandingRequirement(
    course,
    completedAcademicUnits,
    standingRequirements,
  )

  if (missingPrerequisites.length === 0 && !missingStandingRequirement) {
    return {
      status: 'available',
      missingPrerequisites: [],
    }
  }

  return {
    status: 'locked',
    missingPrerequisites: [
      ...missingPrerequisites,
      ...(missingStandingRequirement ? [missingStandingRequirement] : []),
    ],
  }
}

// Show curriculum rows, course cards, prerequisite arrows, and hover emphasis
function SemesterRoadmap({
  courses,
  prerequisiteLinks,
  recommendations,
  isLoadingRecommendations,
  recommendationError,
}: SemesterRoadmapProps) {
  // Track hover state so connected courses/arrows can be emphasized
  const [hoveredCourseId, setHoveredCourseId] = useState<string | null>(null)
  const [showAllArrows, setShowAllArrows] = useState(true)
  const [arrowPaths, setArrowPaths] = useState<ArrowPath[]>([])
  const completedCourseIds = useProfileStore((state) => state.completedCourseIds)
  const toggleCourseCompletion = useProfileStore((state) => state.toggleCourseCompletion)
  const setCompletedCourses = useProfileStore((state) => state.setCompletedCourses)
  const clearCurriculumGuide = useProfileStore((state) => state.clearCurriculumGuide)
  const curriculumGuide = useProfileStore((state) => state.curriculumGuide)
  const transcriptTotalAcademicUnitsEarned = useProfileStore(
    (state) => state.transcriptTotalAcademicUnitsEarned,
  )
  // Hydrate completed courses from roadmap if not already in store
  useEffect(() => {
    if (completedCourseIds.length === 0) {
      const initialCompleted = courses.filter((c) => c.isCompleted).map((c) => c.id)
      if (initialCompleted.length > 0) {
        setCompletedCourses(initialCompleted)
      }
    }
  }, [courses, completedCourseIds.length, setCompletedCourses])

  // Let us measure where each course card is on screen so SVG arrows can connect them
  const roadmapRef = useRef<HTMLDivElement | null>(null)
  const courseRefs = useRef<Record<string, HTMLElement | null>>({})

  // Sort rows so the roadmap follows curriculum order
  const semesterGroups = groupCoursesBySemester(courses).sort(
    (a, b) => a.year - b.year || a.semester - b.semester,
  )

  const connectedCourseIds = new Set<string>()
  const courseCodeById = new Map(courses.map((course) => [course.id, course.courseCode]))
  const completedRoadmapAcademicUnits = courses
    .filter((course) => completedCourseIds.includes(course.id))
    .reduce((total, course) => total + course.academicUnits, 0)
  const completedAcademicUnits =
    transcriptTotalAcademicUnitsEarned > 0
      ? transcriptTotalAcademicUnitsEarned
      : completedRoadmapAcademicUnits
  const standingRequirements = curriculumGuide?.standingRequirements ?? []
  const availableChoiceSlots = courses
    .filter((course) => {
      const eligibility = getCourseEligibility(
        course,
        completedCourseIds,
        completedAcademicUnits,
        standingRequirements,
      )

      return course.isChoiceSlot && eligibility.status === 'available'
    })
    .map((course) => {
      const slotKey = getChoiceSlotKey(course)

      return slotKey ? { course, slotKey } : null
    })
    .filter((choiceSlot): choiceSlot is ChoiceSlotCandidate => Boolean(choiceSlot))
  const recommendationByChoiceSlotId = assignRecommendationsToChoiceSlots(
    availableChoiceSlots,
    recommendations,
  )

  function handleClearRoadmap() {
    const shouldClear = window.confirm(
      'Clear the uploaded curriculum guide from this profile? Your uploaded transcript will stay saved.',
    )

    if (shouldClear) {
      clearCurriculumGuide()
    }
  }

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
        const shouldShow = hoveredCourseId ? isHighlighted : showAllArrows

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

        <div className="roadmap-actions">
          {/* Remove the uploaded curriculum guide while keeping transcript data saved for rematching. */}
          <button type="button" className="clear-roadmap-button" onClick={handleClearRoadmap}>
            Clear roadmap
          </button>

          {/* Clear the completed-course list so every roadmap checkbox becomes unchecked */}
          <button
            type="button"
            className="clear-completed-button"
            onClick={() => setCompletedCourses([])}
            // Disable if no completed courses to clear
            disabled={completedCourseIds.length === 0}
          >
            Clear completed
          </button>

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
      </div>

      {recommendationError && (
        <p className="roadmap-recommendation-error">{recommendationError}</p>
      )}
      {isLoadingRecommendations && (
        <p className="roadmap-recommendation-loading">
          <ClassicLoader className="roadmap-recommendation-loader" />
          Loading recommendations...
        </p>
      )}

      <div
        className={[
          'semester-roadmap',
          hoveredCourseId ? 'semester-roadmap-hovering' : '',
        ]
          .filter(Boolean)
          .join(' ')}
        ref={roadmapRef}
      >
        {/* SVG overlay draws curved prerequisite arrows. */}
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
            <marker
              id="roadmap-arrow-highlighted"
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
                  const isCompleted = completedCourseIds.includes(course.id)
                  const eligibility = getCourseEligibility(
                    course,
                    completedCourseIds,
                    completedAcademicUnits,
                    standingRequirements,
                  )
                  const slotRecommendation = recommendationByChoiceSlotId[course.id]

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
                        isCompleted ? 'semester-course-card-completed' : '',
                        eligibility.status === 'locked' ? 'semester-course-card-locked' : '',
                      ]
                        .filter(Boolean)
                        .join(' ')}
                      onMouseEnter={() => setHoveredCourseId(course.id)}
                      onMouseLeave={() => setHoveredCourseId(null)}
                    >
                      <div className="semester-course-card-top">
                        <strong>{course.courseCode}</strong>
                        <div className="semester-course-card-meta">
                          {eligibility.status === 'locked' && (
                            <span className="course-lock-badge">Locked</span>
                          )}
                          <span className="course-au">{course.academicUnits}AU</span>
                        </div>
                      </div>
                      <p>{course.title}</p>
                      {eligibility.status === 'locked' && (
                        <p className="missing-prerequisites">
                          Missing:{' '}
                          {eligibility.missingPrerequisites
                            .map((courseId) => courseCodeById.get(courseId) ?? courseId)
                            .join(', ')}
                        </p>
                      )}
                      {course.isChoiceSlot &&
                        eligibility.status === 'available' &&
                        slotRecommendation && (
                          <div className="choice-slot-recommendations">
                            <span>{slotRecommendation.label}</span>
                            <strong>{slotRecommendation.courseCode}</strong>
                            <small>{slotRecommendation.title}</small>
                          </div>
                        )}
                      {course.isChoiceSlot &&
                        eligibility.status === 'available' &&
                        isLoadingRecommendations &&
                        !slotRecommendation && (
                          <div className="choice-slot-loading">
                            <ClassicLoader className="choice-slot-loader" />
                            Loading recommendations...
                          </div>
                        )}
                      <div className="semester-course-card-bottom">
                        <span
                          className={`semester-course-type ${getCourseTypeClass(
                            course.type,
                          )}`}
                        >
                          {course.type}
                        </span>
                        <input
                          type="checkbox"
                          className="completion-indicator"
                          checked={isCompleted}
                          onChange={() => toggleCourseCompletion(course.id)}
                          aria-label={
                            isCompleted ? 'Mark course as incomplete' : 'Mark course as complete'
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
