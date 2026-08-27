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
  const transcriptCompletedCourseCount = useProfileStore((state) => state.transcriptCompletedCourseCount)
  const transcriptUnmatchedCourseCount = useProfileStore((state) => state.transcriptUnmatchedCourseCount)
  const setTranscriptResults = useProfileStore((state) => state.setTranscriptResults)
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

      // Save both roadmap matches and the wider transcript count for the active Student ID.
      setTranscriptResults(
        completedCourseIdsFromTranscript,
        result.completed_transcript_course_count,
        result.unmatched_course_codes.length,
      )
      setUploadMessage(
        `Parsed ${result.completed_transcript_course_count} completed module(s). ${completedCourseIdsFromTranscript.length} matched the roadmap. ${result.unmatched_course_codes.length} unmatched.`,
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
        {/* Roadmap count and transcript count are separate because not every cleared module is in the roadmap. */}
        <div className="stat-card">
          <strong>{completedCourseIds.length}</strong>
          <span>Completed Roadmap Courses</span>
        </div>
        <div className="stat-card transcript-stat-card">
          <strong>{transcriptCompletedCourseCount}</strong>
          <span>Completed Transcript Modules</span>
        </div>
        <div className="stat-card unmatched-stat-card">
          <strong>{transcriptUnmatchedCourseCount}</strong>
          <span>Unmatched Transcript Modules</span>
        </div>
      </div>
    </section>
  )
}

export default ProfilePage
