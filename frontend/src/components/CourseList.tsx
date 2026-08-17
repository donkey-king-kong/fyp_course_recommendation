import './CourseList.css'
import type { CourseNode } from '../types/roadmap'

interface CourseListProps {
  courses: CourseNode[]
}

function CourseList({ courses }: CourseListProps) {
  return (
    <section className="course-list">
      <h2>Course List</h2>
      <ul>
        {courses.map((course) => (
          <li key={course.id} className="course-list-item">
            <strong>
              {course.courseCode} - {course.title}
            </strong>
            <span>
              Year {course.year}, Semester {course.semester} - {course.academicUnits} AU -{' '}
              {course.type}
            </span>
          </li>
        ))}
      </ul>
    </section>
  )
}

export default CourseList
