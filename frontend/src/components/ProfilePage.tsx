import { useState } from 'react'
import { uploadCurriculumGuide } from '../api/curriculumApi'
import { uploadTranscript } from '../api/transcriptApi'
import { useProfileStore } from '../store/useProfileStore'
import './ProfilePage.css'

function formatAcademicUnits(academicUnits: number) {
  return Number.isInteger(academicUnits) ? academicUnits.toString() : academicUnits.toFixed(1)
}

function ProfilePage() {
  // Read the saved student profile from the shared Zustand store
  const profile = useProfileStore((state) => state.profile)

  // Update profile fields
  const updateProfile = useProfileStore((state) => state.updateProfile)

  // Read completed courses so the profile page can show a simple progress summary
  const completedCourseIds = useProfileStore((state) => state.completedCourseIds)
  const transcriptCompletedCourseCount = useProfileStore((state) => state.transcriptCompletedCourseCount)
  const transcriptUnmatchedCourseCount = useProfileStore((state) => state.transcriptUnmatchedCourseCount)
  const transcriptMatchedCourses = useProfileStore((state) => state.transcriptMatchedCourses)
  const transcriptUnmatchedCourseCodes = useProfileStore((state) => state.transcriptUnmatchedCourseCodes)
  const transcriptTotalAcademicUnitsEarned = useProfileStore(
    (state) => state.transcriptTotalAcademicUnitsEarned,
  )
  const curriculumGuide = useProfileStore((state) => state.curriculumGuide)
  const curriculumGuideFileName = useProfileStore((state) => state.curriculumGuideFileName)
  const transcriptCompletedCourseCodes = useProfileStore(
    (state) => state.transcriptCompletedCourseCodes,
  )
  const setCurriculumGuide = useProfileStore((state) => state.setCurriculumGuide)
  const clearCurriculumGuide = useProfileStore((state) => state.clearCurriculumGuide)
  const setTranscriptResults = useProfileStore((state) => state.setTranscriptResults)
  const clearTranscriptResults = useProfileStore((state) => state.clearTranscriptResults)
  const [selectedCurriculumGuide, setSelectedCurriculumGuide] = useState<File | null>(null)
  const [selectedTranscript, setSelectedTranscript] = useState<File | null>(null)
  const [curriculumGuideInputKey, setCurriculumGuideInputKey] = useState(0)
  const [transcriptInputKey, setTranscriptInputKey] = useState(0)
  const [isUploadingCurriculumGuide, setIsUploadingCurriculumGuide] = useState(false)
  const [isUploading, setIsUploading] = useState(false)
  const [curriculumUploadMessage, setCurriculumUploadMessage] = useState('')
  const [curriculumUploadError, setCurriculumUploadError] = useState('')
  const [uploadMessage, setUploadMessage] = useState('')
  const [uploadError, setUploadError] = useState('')
  const hasCurriculumGuide = Boolean(curriculumGuide)
  const hasTranscriptResults =
    transcriptMatchedCourses.length > 0 ||
    transcriptUnmatchedCourseCodes.length > 0 ||
    transcriptCompletedCourseCount > 0
  const standingRequirements = curriculumGuide?.standingRequirements ?? []
  const transcriptSummaryMessage = `Current transcript: ${transcriptCompletedCourseCount} completed module(s), ${formatAcademicUnits(transcriptTotalAcademicUnitsEarned)} AU earned.`

  async function handleCurriculumGuideUpload() {
    if (!selectedCurriculumGuide) {
      setCurriculumUploadError('Upload a PDF curriculum guide before uploading.')
      return
    }

    try {
      setIsUploadingCurriculumGuide(true)
      setCurriculumUploadError('')
      setCurriculumUploadMessage('')

      const result = await uploadCurriculumGuide(selectedCurriculumGuide)

      setCurriculumGuide(result, selectedCurriculumGuide.name)
      setCurriculumUploadMessage(
        `Parsed ${result.nodes.length} curriculum row(s) across ${result.semesters.length} semester(s).`,
      )
    } catch {
      setCurriculumUploadError('Could not process curriculum guide. Make sure the backend is running.')
    } finally {
      setIsUploadingCurriculumGuide(false)
    }
  }

  function handleClearCurriculumGuide() {
    const shouldClear = window.confirm(
      'Clear the stored curriculum guide for this profile? Your uploaded transcript results will stay saved.',
    )

    if (!shouldClear) {
      return
    }

    clearCurriculumGuide()
    setSelectedCurriculumGuide(null)
    setCurriculumGuideInputKey((currentKey) => currentKey + 1)
    setCurriculumUploadError('')
    setCurriculumUploadMessage('Cleared stored curriculum guide for this profile.')
  }

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

      const completedCourseCodesFromTranscript = [
        ...new Set([
          ...result.completed_courses.map((course) => course.course_code),
          ...result.unmatched_course_codes,
        ]),
      ]

      // Store transcript codes first; roadmap matching happens only when a curriculum guide exists.
      setTranscriptResults(
        completedCourseCodesFromTranscript,
        result.completed_transcript_course_count,
        result.total_academic_units_earned,
      )

      if (curriculumGuide) {
        setUploadMessage(
          `Parsed ${result.completed_transcript_course_count} completed module(s) and ${formatAcademicUnits(result.total_academic_units_earned)} AU. Matching is updated against your uploaded curriculum guide.`,
        )
      } else {
        setUploadMessage(
          `Parsed ${result.completed_transcript_course_count} completed module(s) and ${formatAcademicUnits(result.total_academic_units_earned)} AU. Upload your curriculum guide to match them to your roadmap.`,
        )
      }
    } catch {
      // Keeping error message simple because failures can come from network or parsing
      setUploadError('Could not process transcript. Make sure the backend is running.')
    } finally {
      // Always stop the loading state after success, validation, or failure
      setIsUploading(false)
    }
  }

  function handleClearTranscriptResults() {
    const shouldClear = window.confirm(
      'Clear the stored transcript results for this profile? Your uploaded curriculum guide will stay saved.',
    )

    if (!shouldClear) {
      return
    }

    clearTranscriptResults()
    setSelectedTranscript(null)
    setTranscriptInputKey((currentKey) => currentKey + 1)
    setUploadError('')
    setUploadMessage('Cleared stored transcript results for this profile.')
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

        <label className="profile-field">
          <span>Career Goal</span>
          <select
            value={profile.careerGoal}
            onChange={(e) => updateProfile({ careerGoal: e.target.value })}
          >
            <option value="">Select a career goal</option>
            <option value="software-engineer">Software Engineer</option>
            <option value="ai-ml-engineer">AI / Machine Learning Engineer</option>
            <option value="cybersecurity-analyst">Cybersecurity Analyst</option>
            <option value="data-analyst">Data Analyst</option>
            <option value="backend-engineer">Backend Engineer</option>
            <option value="cloud-devops-engineer">Cloud / DevOps Engineer</option>
          </select>
        </label>
      </form>

      <section className="transcript-upload-card">
        <div>
          <h3>Curriculum Guide Upload</h3>
          <p>
            Upload your curriculum guide PDF first so the roadmap can be generated for your profile.
          </p>
        </div>

        <label className="transcript-file-field">
          <span>PDF Curriculum Guide</span>
          <input
            key={curriculumGuideInputKey}
            type="file"
            accept="application/pdf"
            onChange={(event) => {
              setSelectedCurriculumGuide(event.target.files?.[0] ?? null)
              setCurriculumUploadError('')
              setCurriculumUploadMessage('')
            }}
          />
        </label>

        <div className="transcript-action-row">
          <button
            className="transcript-upload-button"
            type="button"
            onClick={handleCurriculumGuideUpload}
            disabled={isUploadingCurriculumGuide}
          >
            {isUploadingCurriculumGuide ? 'Uploading...' : 'Upload Curriculum Guide'}
          </button>

          <button
            className="clear-transcript-button"
            type="button"
            onClick={handleClearCurriculumGuide}
            disabled={!hasCurriculumGuide}
          >
            Clear Curriculum Guide
          </button>
        </div>

        {curriculumUploadMessage && <p className="upload-success">{curriculumUploadMessage}</p>}
        {curriculumUploadError && <p className="upload-error">{curriculumUploadError}</p>}
        {hasCurriculumGuide && (
          <>
            <p>
              Current guide: {curriculumGuideFileName || `${curriculumGuide?.major} ${curriculumGuide?.cohort}`}
            </p>

            {standingRequirements.length > 0 && (
              <div className="standing-requirements-card">
                <h4>Minimum AU For Year Standing</h4>
                <ul>
                  {standingRequirements.map((requirement) => (
                    <li key={requirement.standingYear}>
                      <span>Year {requirement.standingYear} standing</span>
                      <strong>{requirement.minimumAcademicUnits} AU</strong>
                      <small>
                        From Year {requirement.includedYears.join(' + Year ')} Total AU
                      </small>
                    </li>
                  ))}
                </ul>
              </div>
            )}
          </>
        )}
      </section>

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
            key={transcriptInputKey}
            type="file"
            accept="application/pdf"
            onChange={(event) => {
              setSelectedTranscript(event.target.files?.[0] ?? null)
              setUploadError('')
              setUploadMessage('')
            }}
          />
        </label>

        <div className="transcript-action-row">
          <button
            className="transcript-upload-button"
            type="button"
            onClick={handleTranscriptUpload}
            disabled={isUploading}
          >
            {isUploading ? 'Uploading...' : 'Upload Transcript'}
          </button>

          <button
            className="clear-transcript-button"
            type="button"
            onClick={handleClearTranscriptResults}
            disabled={!hasTranscriptResults}
          >
            Clear Transcript
          </button>
        </div>

        {uploadMessage && <p className="upload-success">{uploadMessage}</p>}
        {!uploadMessage && hasTranscriptResults && (
          <p className="upload-success">{transcriptSummaryMessage}</p>
        )}
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
        <div className="stat-card transcript-au-stat-card">
          <strong>{formatAcademicUnits(transcriptTotalAcademicUnitsEarned)}</strong>
          <span>Total AU Earned</span>
        </div>
        <div className="stat-card unmatched-stat-card">
          <strong>{transcriptUnmatchedCourseCount}</strong>
          <span>Transcript Modules Outside Roadmap</span>
        </div>
      </div>

      {hasTranscriptResults && (
        <section className="transcript-results-card">
          <div className="transcript-results-header">
            <h3>Transcript Results</h3>
            <span>Latest upload</span>
          </div>

          <div className="transcript-results-grid">
            <div className="transcript-result-list">
              <h4>Transcript Modules Found In Roadmap</h4>
              {!hasCurriculumGuide ? (
                <p>Upload a curriculum guide to match transcript modules to your roadmap.</p>
              ) : transcriptMatchedCourses.length > 0 ? (
                <ul>
                  {transcriptMatchedCourses.map((course) => (
                    <li key={course.courseCode}>
                      <strong>{course.courseCode}</strong>
                      <span>{course.title}</span>
                    </li>
                  ))}
                </ul>
              ) : (
                <p>No completed transcript modules were found in the uploaded curriculum guide.</p>
              )}
            </div>

            <div className="transcript-result-list">
              <h4>Transcript Modules Outside Roadmap</h4>
              {!hasCurriculumGuide ? (
                <>
                  <p>
                    These are completed transcript modules waiting for a curriculum guide match.
                  </p>
                <div className="unmatched-code-list">
                  {transcriptCompletedCourseCodes.map((courseCode) => (
                    <span key={courseCode}>{courseCode}</span>
                  ))}
                </div>
                </>
              ) : transcriptUnmatchedCourseCodes.length > 0 ? (
                <>
                  <p>
                    These completed modules were not found in the uploaded curriculum guide.
                  </p>
                <div className="unmatched-code-list">
                  {transcriptUnmatchedCourseCodes.map((courseCode) => (
                    <span key={courseCode}>{courseCode}</span>
                  ))}
                </div>
                </>
              ) : (
                <p>All completed transcript modules were found in the uploaded curriculum guide.</p>
              )}
            </div>
          </div>
        </section>
      )}
    </section>
  )
}

export default ProfilePage
