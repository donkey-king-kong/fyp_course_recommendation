import './CourseList.css'
import type { CourseNode } from '../types/roadmap'

interface CourseListProps {
  courses: CourseNode[]
}

interface CourseGroup {
  year: number
  semester: number
  courses: CourseNode[]
}

function CourseList({ courses }: CourseListProps) {
  const courseGroups = courses.reduce<CourseGroup[]>((groups, course) => {
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

  return (
    <section className="course-list">
      <h2>Course List</h2>

      {courses.length === 0 && <p className="course-list-empty">No courses found.</p>}

      <div className="course-groups">
        {courseGroups.map((group) => (
          <section
            key={`${group.year}-${group.semester}`}
            className="course-group"
          >
            <h3>
              Year {group.year}, Semester {group.semester}
            </h3>

            <ul>
              {group.courses.map((course) => (
                <li key={course.id} className="course-list-item">
                  <strong>
                    {course.courseCode} - {course.title}
                  </strong>
                  <span>
                    {course.academicUnits} AU - {course.type}
                  </span>
                </li>
              ))}
            </ul>
          </section>
        ))}
      </div>
    </section>
  )
}

export default CourseList
