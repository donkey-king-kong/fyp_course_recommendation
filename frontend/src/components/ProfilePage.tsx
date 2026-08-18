import { useState } from 'react'
import { uploadTranscript } from '../api/transcriptApi'
import { useProfileStore } from '../store/useProfileStore'
import './ProfilePage.css'

function ProfilePage() {
  // Read the saved student profile from the shared Zustand store
  const profile = useProfileStore((state) => state.profile)

  // Update profile fields
  const updateProfile = useProfileStore((state) => state.updateProfile)

  // Read completed courses so the profile page can show a simple progress summary
  const completedCourseIds = useProfileStore((state) => state.completedCourseIds)
  const setCompletedCourses = useProfileStore((state) => state.setCompletedCourses)
  const [selectedTranscript, setSelectedTranscript] = useState<File | null>(null)
  const [isUploading, setIsUploading] = useState(false)
  const [uploadMessage, setUploadMessage] = useState('')
  const [uploadError, setUploadError] = useState('')

  async function handleTranscriptUpload() {
    // Error message when upload button clicked without uploading anything
    if (!selectedTranscript) {
      setUploadError('Upload a PDF transcript before uploading.')
      return
    }

    try {
      // Reset previous upload feedback before starting a new upload
      setIsUploading(true)
      setUploadError('')
      setUploadMessage('')

      // Send the selected PDF to the backend transcript parser
      const result = await uploadTranscript(selectedTranscript)

      // For extracted courses, use courseID only to check boxes
      const completedCourseIdsFromTranscript = result.completed_courses.map(
        (course) => course.course_id,
      )

      // Roadmap data is not wiped if extracted info is nothing useful
      if (completedCourseIdsFromTranscript.length === 0) {
        setUploadMessage('No completed roadmap courses were found in this transcript yet.')
        return
      }

      // Save these IDs so the roadmap checkboxes become checked for the particular Student ID
      setCompletedCourses(completedCourseIdsFromTranscript)
      setUploadMessage(
        `Found ${completedCourseIdsFromTranscript.length} completed roadmap course(s).`,
      )
    } catch {
      // Keeping error message simple because failures can come from network or parsing
      setUploadError('Could not process transcript. Make sure the backend is running.')
    } finally {
      // Always stop the loading state after success, validation, or failure
      setIsUploading(false)
    }
  }

  return (
    <section className="profile-section">
      <div className="profile-header">
        <h2>Student Profile</h2>
        <p>Manage your details to personalize your course recommendations.</p>
      </div>

      <form className="profile-form" onSubmit={(e) => e.preventDefault()}>
        {/* Student ID is the browser-side profile identity. */}
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

      <section className="transcript-upload-card">
        <div>
          <h3>Transcript Upload</h3>
          <p>
            Upload a PDF transcript to auto-mark completed roadmap courses.
          </p>
        </div>

        <label className="transcript-file-field">
          <span>PDF Transcript</span>
          <input
            type="file"
            accept="application/pdf"
            onChange={(event) => {
              setSelectedTranscript(event.target.files?.[0] ?? null)
              setUploadError('')
              setUploadMessage('')
            }}
          />
        </label>

        <button
          className="transcript-upload-button"
          type="button"
          onClick={handleTranscriptUpload}
          disabled={isUploading}
        >
          {isUploading ? 'Uploading...' : 'Upload Transcript'}
        </button>

        {uploadMessage && <p className="upload-success">{uploadMessage}</p>}
        {uploadError && <p className="upload-error">{uploadError}</p>}
      </section>

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
