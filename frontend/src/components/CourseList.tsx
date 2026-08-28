import './CourseList.css'
import type { CurriculumCourse } from '../types/curriculum'

// Describe the data this component receives from App.tsx
interface CourseListProps {
  courses: CurriculumCourse[]
}

// One group represents all courses in the same year and semester
interface CourseGroup {
  year: number
  semester: number
  courses: CurriculumCourse[]
}

// Displays uploaded curriculum guide courses as semester groups.
function CourseList({ courses }: CourseListProps) {
  // Convert the flat course array into grouped sections such as Year 1, Semester 1.
  const courseGroups = courses
    .reduce<CourseGroup[]>((groups, course) => {
      const existingGroup = groups.find(
        (group) => group.year === course.year && group.semester === course.semester,
      )

      // If this semester group already exists, add the course into it
      if (existingGroup) {
        existingGroup.courses.push(course)
        return groups
      }

      // Else, create a new semester group and add this course
      return [
        ...groups,
        {
          year: course.year,
          semester: course.semester,
          courses: [course],
        },
      ]
    }, [])
    .sort((firstGroup, secondGroup) => (
      firstGroup.year - secondGroup.year || firstGroup.semester - secondGroup.semester
    ))

  return (
    <section className="course-list">
      <h2>Curriculum Guide Courses</h2>

      {/* Show this message when there are no courses to display */}
      {courses.length === 0 && <p className="course-list-empty">No courses found.</p>}

      <div className="course-groups">
        {/* Render one section for each year and semester group */}
        {courseGroups.map((group) => (
          <section
            key={`${group.year}-${group.semester}`}
            className="course-group"
          >
            <h3>
              Year {group.year}, Semester {group.semester}
            </h3>

            <ul className="course-card-grid">
              {/* Render every course inside the current semester group */}
              {group.courses.map((course) => (
                <li key={course.id} className="course-list-item">
                  <strong>
                    {course.courseCode} - {course.title}
                  </strong>
                  <span className="course-list-meta">
                    <span>{course.academicUnits} AU</span>
                    <span className="course-type-badge">{course.type}</span>
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
