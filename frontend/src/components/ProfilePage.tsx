import { useProfileStore } from '../store/useProfileStore'
import './ProfilePage.css'

function ProfilePage() {
  // Read the saved student profile from the shared Zustand store
  const profile = useProfileStore((state) => state.profile)

  // Update profile fields
  const updateProfile = useProfileStore((state) => state.updateProfile)

  // Read completed courses so the profile page can show a simple progress summary
  const completedCourseIds = useProfileStore((state) => state.completedCourseIds)

  return (
    <section className="profile-section">
      <div className="profile-header">
        <h2>Student Profile</h2>
        <p>Manage your details to personalize your course recommendations.</p>
      </div>

      <form className="profile-form" onSubmit={(e) => e.preventDefault()}>
        {/* Student ID acts as the temporary unique user identifier for this frontend-only version */}
        <label className="profile-field">
          <span>Student ID</span>
          <input
            type="text"
            value={profile.studentId}
            onChange={(e) => updateProfile({ studentId: e.target.value })}
            placeholder="Enter your student ID"
          />
        </label>

        <div className="profile-row">
          {/* Major is included now so future roadmap/recommendation logic can branch by programme */}
          <label className="profile-field">
            <span>Major</span>
            <select
              value={profile.major}
              onChange={(e) => updateProfile({ major: e.target.value as 'CSC' })}
            >
              {/* Only CSC is available for now */}
              <option value="CSC">CSC</option>
            </select>
          </label>

          {/* Year and semester that student is currently in */}
          <label className="profile-field">
            <span>Year of Study</span>
            <select
              value={profile.yearOfStudy}
              onChange={(e) => updateProfile({ yearOfStudy: parseInt(e.target.value, 10) })}
            >
              {[1, 2, 3, 4].map((year) => (
                <option key={year} value={year}>
                  Year {year}
                </option>
              ))}
            </select>
          </label>

          {/* This value will later help recommendations target the student's next planning */}
          <label className="profile-field">
            <span>Current Semester</span>
            <select
              value={profile.currentSemester}
              onChange={(e) => updateProfile({ currentSemester: parseInt(e.target.value, 10) })}
            >
              {[1, 2].map((sem) => (
                <option key={sem} value={sem}>
                  Semester {sem}
                </option>
              ))}
            </select>
          </label>
        </div>
      </form>

      {/* Count is shared with the Roadmap checkboxes through the same global store */}
      <div className="profile-stats">
        <div className="stat-card">
          <strong>{completedCourseIds.length}</strong>
          <span>Completed Courses</span>
        </div>
        <p className="stat-hint">
          Check off courses in the Roadmap to mark them as completed.
        </p>
      </div>
    </section>
  )
}

export default ProfilePage
