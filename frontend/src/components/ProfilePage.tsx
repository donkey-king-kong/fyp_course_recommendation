import { useProfileStore } from '../store/useProfileStore'
import './ProfilePage.css'

function ProfilePage() {
  const profile = useProfileStore((state) => state.profile)
  const updateProfile = useProfileStore((state) => state.updateProfile)
  const completedCourseIds = useProfileStore((state) => state.completedCourseIds)

  return (
    <section className="profile-section">
      <div className="profile-header">
        <h2>Student Profile</h2>
        <p>Manage your details to personalize your course recommendations.</p>
      </div>

      <form className="profile-form" onSubmit={(e) => e.preventDefault()}>
        <label className="profile-field">
          <span>Name</span>
          <input
            type="text"
            value={profile.name}
            onChange={(e) => updateProfile({ name: e.target.value })}
            placeholder="Enter your name"
          />
        </label>

        <div className="profile-row">
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
