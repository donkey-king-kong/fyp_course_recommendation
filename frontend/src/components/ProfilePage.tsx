import { useMemo, useState } from 'react'
import { uploadCurriculumGuide } from '../api/curriculumApi'
import { matchTranscriptToCurriculum, uploadTranscript } from '../api/transcriptApi'
import { useProfileStore } from '../store/useProfileStore'
import './ProfilePage.css'

function formatAcademicUnits(academicUnits: number) {
  return Number.isInteger(academicUnits) ? academicUnits.toString() : academicUnits.toFixed(1)
}

interface ProfilePageProps {
  isLoadingRoadmap: boolean
  hasLoadedRoadmap: boolean
  recommendationError: string
  recommendationNotice: string
  onGoToRoadmap: () => void
  onLoadRoadmap: () => void
  onClearRecommendations: () => void
}

const RECOMMENDATION_TAG_OPTIONS = [
  { value: 'software-engineering', label: 'Software Engineering' },
  { value: 'programming', label: 'Programming' },
  { value: 'web-development', label: 'Web Development' },
  { value: 'backend-engineering', label: 'Backend Engineering' },
  { value: 'frontend-engineering', label: 'Frontend Engineering' },
  { value: 'database', label: 'Database' },
  { value: 'computer-network', label: 'Computer Network' },
  { value: 'computer-security', label: 'Computer Security' },
  { value: 'cryptography', label: 'Cryptography' },
  { value: 'malware-analysis', label: 'Malware Analysis' },
  { value: 'digital-forensics', label: 'Digital Forensics' },
  { value: 'privacy', label: 'Privacy' },
  { value: 'algorithms', label: 'Algorithms' },
  { value: 'data-structures', label: 'Data Structures' },
  { value: 'operating-systems', label: 'Operating Systems' },
  { value: 'distributed-systems', label: 'Distributed Systems' },
  { value: 'cloud-computing', label: 'Cloud Computing' },
  { value: 'parallel-computing', label: 'Parallel Computing' },
  { value: 'compiler', label: 'Compiler' },
  { value: 'ai-ml', label: 'AI / ML' },
  { value: 'natural-language-processing', label: 'Natural Language Processing' },
  { value: 'computer-vision', label: 'Computer Vision' },
  { value: 'data-science', label: 'Data Science' },
  { value: 'data-visualisation', label: 'Data Visualisation' },
  { value: 'information-retrieval', label: 'Information Retrieval' },
  { value: 'computer-graphics', label: 'Computer Graphics' },
  { value: 'human-computer-interaction', label: 'Human-Computer Interaction' },
  { value: 'computer-architecture', label: 'Computer Architecture' },
  { value: 'hardware-embedded', label: 'Hardware / Embedded' },
  { value: 'internet-of-things', label: 'Internet of Things' },
  { value: 'cyber-physical-systems', label: 'Cyber-Physical Systems' },
  { value: 'signal-processing', label: 'Signal Processing' },
  { value: 'digital-logic', label: 'Digital Logic' },
  { value: 'simulation-modelling', label: 'Simulation / Modelling' },
  { value: 'quantum-computing', label: 'Quantum Computing' },
  { value: 'theory-of-computing', label: 'Theory of Computing' },
  { value: 'math-foundation', label: 'Math Foundation' },
  { value: 'project-management', label: 'Project Management' },
  { value: 'product-management', label: 'Product Management' },
  { value: 'professional-skills', label: 'Professional Skills' },
  { value: 'ethics', label: 'Ethics' },
  { value: 'sustainability-computing', label: 'Sustainability Computing' },
]
const EMPTY_RECOMMENDATION_TAGS: string[] = []

function ProfilePage({
  isLoadingRoadmap,
  hasLoadedRoadmap,
  recommendationError,
  recommendationNotice,
  onGoToRoadmap,
  onLoadRoadmap,
  onClearRecommendations,
}: ProfilePageProps) {
  // Read the saved student profile from the shared Zustand store
  const profile = useProfileStore((state) => state.profile)

  // Update profile fields
  const updateProfile = useProfileStore((state) => state.updateProfile)

  const transcriptCompletedCourseCount = useProfileStore((state) => state.transcriptCompletedCourseCount)
  const transcriptMatchedCourses = useProfileStore((state) => state.transcriptMatchedCourses)
  const transcriptUnmatchedCourseCodes = useProfileStore((state) => state.transcriptUnmatchedCourseCodes)
  const transcriptTotalAcademicUnitsEarned = useProfileStore(
    (state) => state.transcriptTotalAcademicUnitsEarned,
  )
  const curriculumGuide = useProfileStore((state) => state.curriculumGuide)
  const curriculumGuideFileName = useProfileStore((state) => state.curriculumGuideFileName)
  const transcriptFileName = useProfileStore((state) => state.transcriptFileName)
  const transcriptCompletedCourseCodes = useProfileStore(
    (state) => state.transcriptCompletedCourseCodes,
  )
  const transcriptCompletedCourses = useProfileStore((state) => state.transcriptCompletedCourses)
  const isTranscriptAppliedToRoadmap = useProfileStore((state) => state.isTranscriptAppliedToRoadmap)
  const setCurriculumGuide = useProfileStore((state) => state.setCurriculumGuide)
  const clearCurriculumGuide = useProfileStore((state) => state.clearCurriculumGuide)
  const setTranscriptResults = useProfileStore((state) => state.setTranscriptResults)
  const clearTranscriptResults = useProfileStore((state) => state.clearTranscriptResults)
  const [uploadingCurriculumGuideFileName, setUploadingCurriculumGuideFileName] = useState('')
  const [uploadingTranscriptFileName, setUploadingTranscriptFileName] = useState('')
  const [curriculumGuideInputKey, setCurriculumGuideInputKey] = useState(0)
  const [transcriptInputKey, setTranscriptInputKey] = useState(0)
  const [isUploadingCurriculumGuide, setIsUploadingCurriculumGuide] = useState(false)
  const [isUploading, setIsUploading] = useState(false)
  const [isReapplyingTranscript, setIsReapplyingTranscript] = useState(false)
  const [curriculumUploadMessage, setCurriculumUploadMessage] = useState('')
  const [curriculumUploadError, setCurriculumUploadError] = useState('')
  const [uploadMessage, setUploadMessage] = useState('')
  const [uploadError, setUploadError] = useState('')
  const [preferenceSearch, setPreferenceSearch] = useState('')
  const hasCurriculumGuide = Boolean(curriculumGuide)
  const hasTranscriptResults =
    transcriptMatchedCourses.length > 0 ||
    transcriptUnmatchedCourseCodes.length > 0 ||
    transcriptCompletedCourseCount > 0
  const canReapplyTranscript =
    Boolean(curriculumGuide) &&
    transcriptCompletedCourses.length > 0 &&
    !isTranscriptAppliedToRoadmap
  const standingRequirements = curriculumGuide?.standingRequirements ?? []
  const displayedCurriculumGuideFileName = uploadingCurriculumGuideFileName || curriculumGuideFileName
  const displayedTranscriptFileName = uploadingTranscriptFileName || transcriptFileName
  const transcriptSummaryMessage = `Current transcript: ${transcriptCompletedCourseCount} completed module(s), ${formatAcademicUnits(transcriptTotalAcademicUnitsEarned)} AU earned.`
  const hasStaleRecommendations = Boolean(recommendationNotice)
  const canLoadRoadmap =
    hasCurriculumGuide &&
    profile.careerGoal === 'software-engineer' &&
    !isLoadingRoadmap &&
    !isUploadingCurriculumGuide &&
    !isUploading
  const selectedPreferenceTags = profile.preferredRecommendationTags ?? EMPTY_RECOMMENDATION_TAGS
  const selectedPreferenceTagSet = useMemo(
    () => new Set(selectedPreferenceTags),
    [selectedPreferenceTags],
  )
  const hasPreferenceSearch = preferenceSearch.trim().length > 0
  const filteredRecommendationTagOptions = useMemo(() => {
    const normalizedSearch = preferenceSearch.trim().toLowerCase()

    if (!normalizedSearch) {
      return []
    }

    return RECOMMENDATION_TAG_OPTIONS.filter(
      (option) =>
        !selectedPreferenceTagSet.has(option.value) &&
        (option.label.toLowerCase().includes(normalizedSearch) ||
          option.value.toLowerCase().includes(normalizedSearch)),
    )
  }, [preferenceSearch, selectedPreferenceTagSet])

  function handleTogglePreferenceTag(tag: string) {
    const nextTags = selectedPreferenceTagSet.has(tag)
      ? selectedPreferenceTags.filter((selectedTag) => selectedTag !== tag)
      : [...selectedPreferenceTags, tag]

    updateProfile({ preferredRecommendationTags: nextTags })
  }

  async function handleCurriculumGuideUpload(file: File) {
    try {
      setIsUploadingCurriculumGuide(true)
      setUploadingCurriculumGuideFileName(file.name)
      setCurriculumUploadError('')
      setCurriculumUploadMessage('Uploading and parsing selected curriculum guide...')

      const result = await uploadCurriculumGuide(file)
      const transcriptMatch =
        isTranscriptAppliedToRoadmap && transcriptCompletedCourseCodes.length > 0
          ? await matchTranscriptToCurriculum(
              transcriptCompletedCourseCodes,
              transcriptCompletedCourses,
              result,
            )
          : undefined

      setCurriculumGuide(result, file.name, transcriptMatch)
      setCurriculumGuideInputKey((currentKey) => currentKey + 1)
      setCurriculumUploadMessage(
        `Parsed ${result.nodes.length} curriculum row(s) across ${result.semesters.length} semester(s).`,
      )
    } catch {
      setCurriculumUploadError('Could not process curriculum guide. Make sure the backend is running.')
    } finally {
      setIsUploadingCurriculumGuide(false)
      setUploadingCurriculumGuideFileName('')
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
    setUploadingCurriculumGuideFileName('')
    setCurriculumGuideInputKey((currentKey) => currentKey + 1)
    setCurriculumUploadError('')
    setCurriculumUploadMessage('Cleared stored curriculum guide for this profile.')
  }

  async function handleTranscriptUpload(file: File) {
    try {
      // Reset previous upload feedback before starting a new upload
      setIsUploading(true)
      setUploadingTranscriptFileName(file.name)
      setUploadError('')
      setUploadMessage('Uploading and parsing selected transcript...')

      // Send the selected PDF to the backend transcript parser
      const result = await uploadTranscript(file)

      const completedCourseCodesFromTranscript = [
        ...new Set([
          ...result.completed_transcript_courses.map((course) => course.course_code),
        ]),
      ]
      const transcriptMatch = curriculumGuide
        ? await matchTranscriptToCurriculum(
            completedCourseCodesFromTranscript,
            result.completed_transcript_courses,
            curriculumGuide,
          )
        : undefined

      // Save parsed transcript data with backend matching when a curriculum guide exists.
      setTranscriptResults(
        file.name,
        completedCourseCodesFromTranscript,
        result.completed_transcript_courses,
        result.completed_transcript_course_count,
        result.total_academic_units_earned,
        transcriptMatch,
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
      setUploadingTranscriptFileName('')
      setTranscriptInputKey((currentKey) => currentKey + 1)
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
    setUploadingTranscriptFileName('')
    setTranscriptInputKey((currentKey) => currentKey + 1)
    setUploadError('')
    setUploadMessage('Cleared stored transcript results for this profile.')
  }

  async function handleReapplyTranscriptResults() {
    if (!curriculumGuide || transcriptCompletedCourses.length === 0) {
      return
    }

    try {
      setIsReapplyingTranscript(true)
      setUploadError('')
      setUploadMessage('')

      const transcriptMatch = await matchTranscriptToCurriculum(
        transcriptCompletedCourseCodes,
        transcriptCompletedCourses,
        curriculumGuide,
      )

      setTranscriptResults(
        transcriptFileName,
        transcriptCompletedCourseCodes,
        transcriptCompletedCourses,
        transcriptCompletedCourseCount,
        transcriptTotalAcademicUnitsEarned,
        transcriptMatch,
      )
      setUploadMessage(`Re-applied ${transcriptMatch.completedCourseIds.length} transcript match(es) to your roadmap.`)
    } catch {
      setUploadError('Could not re-apply transcript results. Make sure the backend is running.')
    } finally {
      setIsReapplyingTranscript(false)
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
        {/* Keep primary profile inputs together to avoid wasting a full row on Student ID. */}
        <div className="profile-row profile-identity-row">
          <label className="profile-field">
            <span>Student ID</span>
            <input
              type="text"
              value={profile.studentId}
              onChange={(e) => updateProfile({ studentId: e.target.value })}
              placeholder="Enter your student ID"
            />
          </label>

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

          <label className="profile-field">
            <span>Career Goal</span>
            <select
              value={profile.careerGoal}
              onChange={(e) => updateProfile({ careerGoal: e.target.value })}
            >
              <option value="">Select a career goal</option>
              <option value="software-engineer">Software Engineer</option>
            </select>
          </label>
        </div>

        <section className="profile-preferences-card">
          <div className="profile-preferences-header">
            <div>
              <h3>Topic Preferences</h3>
              <p>
                Optional. These tags softly boost matching modules after the career goal,
                eligibility, and prerequisite checks pass.
              </p>
            </div>
            {selectedPreferenceTags.length > 0 && (
              <button
                type="button"
                className="profile-preferences-clear"
                onClick={() => updateProfile({ preferredRecommendationTags: [] })}
              >
                Clear
              </button>
            )}
          </div>

          <label className="profile-field">
            <span>Search Tags</span>
            <input
              type="search"
              value={preferenceSearch}
              onChange={(event) => setPreferenceSearch(event.target.value)}
              placeholder="Type backend, AI, database..."
            />
          </label>

          {selectedPreferenceTags.length > 0 && (
            <div className="selected-preference-list">
              {selectedPreferenceTags.map((tag) => {
                const option = RECOMMENDATION_TAG_OPTIONS.find((item) => item.value === tag)

                return (
                  <span key={tag} className="selected-preference-tag">
                    <span className="selected-preference-label">{option?.label ?? tag}</span>
                    <button
                      type="button"
                      aria-label={`Remove ${option?.label ?? tag}`}
                      onClick={() => handleTogglePreferenceTag(tag)}
                    >
                      ×
                    </button>
                  </span>
                )
              })}
            </div>
          )}

          {hasPreferenceSearch && (
            <div className="preference-option-list">
              {filteredRecommendationTagOptions.length > 0 ? (
                filteredRecommendationTagOptions.map((option) => (
                  <button
                    key={option.value}
                    type="button"
                    className="preference-option"
                    onClick={() => {
                      handleTogglePreferenceTag(option.value)
                      setPreferenceSearch('')
                    }}
                  >
                    {option.label}
                  </button>
                ))
              ) : (
                <p className="preference-empty-message">
                  No matching tag. Choose from the curated list only.
                </p>
              )}
            </div>
          )}
        </section>

        <div className="profile-roadmap-actions">
          <div className="profile-roadmap-load-row">
            <button
              type="button"
              className={[
                'load-roadmap-button',
                hasLoadedRoadmap && !hasStaleRecommendations ? 'loaded' : '',
                hasStaleRecommendations ? 'stale' : '',
              ]
                .filter(Boolean)
                .join(' ')}
              onClick={onLoadRoadmap}
              disabled={!canLoadRoadmap}
              title={hasLoadedRoadmap ? 'Click to reload roadmap recommendations' : 'Load roadmap recommendations'}
            >
              {isLoadingRoadmap && <span className="load-roadmap-spinner" aria-hidden="true" />}
              {hasLoadedRoadmap && !hasStaleRecommendations && !isLoadingRoadmap && (
                <span className="load-roadmap-tick" aria-hidden="true">
                  ✓
                </span>
              )}
              {hasStaleRecommendations
                ? 'Reload Roadmap'
                : hasLoadedRoadmap
                  ? 'Roadmap Loaded'
                  : 'Load Roadmap'}
            </button>

            <button
              className="profile-clear-recommendations-button"
              type="button"
              onClick={onClearRecommendations}
              disabled={!hasLoadedRoadmap || isLoadingRoadmap}
            >
              Clear Recommendations
            </button>

            {recommendationNotice && (
              <span className="recommendation-stale-notice">{recommendationNotice}</span>
            )}
          </div>

          <button className="profile-roadmap-link" type="button" onClick={onGoToRoadmap}>
            Go to roadmap...
          </button>
          {recommendationError && <p className="upload-error">{recommendationError}</p>}
        </div>
      </form>

      <div className="profile-upload-grid">
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
              className="screen-reader-file-input"
              accept="application/pdf"
              onChange={(event) => {
                const selectedFile = event.target.files?.[0] ?? null

                setCurriculumUploadError('')
                setCurriculumUploadMessage('')

                if (selectedFile) {
                  void handleCurriculumGuideUpload(selectedFile)
                }
              }}
              disabled={isUploadingCurriculumGuide}
            />
            <span className="file-picker-row">
              <span className="file-picker-button">
                {isUploadingCurriculumGuide ? 'Uploading...' : 'Choose file'}
              </span>
              <span className="file-picker-name">
                {displayedCurriculumGuideFileName || 'No file chosen'}
              </span>
            </span>
          </label>

          <div className="transcript-action-row">
            <button
              className="clear-transcript-button"
              type="button"
              onClick={handleClearCurriculumGuide}
              disabled={!hasCurriculumGuide || isUploadingCurriculumGuide}
            >
              Clear Curriculum Guide
            </button>
          </div>

          {curriculumUploadMessage && <p className="upload-success">{curriculumUploadMessage}</p>}
          {curriculumUploadError && <p className="upload-error">{curriculumUploadError}</p>}
          {hasCurriculumGuide && (
            <>
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
              className="screen-reader-file-input"
              accept="application/pdf"
              onChange={(event) => {
                const selectedFile = event.target.files?.[0] ?? null

                setUploadError('')
                setUploadMessage('')

                if (selectedFile) {
                  void handleTranscriptUpload(selectedFile)
                }
              }}
              disabled={isUploading}
            />
            <span className="file-picker-row">
              <span className="file-picker-button">
                {isUploading ? 'Uploading...' : 'Choose file'}
              </span>
              <span className="file-picker-name">
                {displayedTranscriptFileName || 'No file chosen'}
              </span>
            </span>
          </label>

          <div className="transcript-action-row">
            <button
              className="clear-transcript-button"
              type="button"
              onClick={handleClearTranscriptResults}
              disabled={!hasTranscriptResults || isUploading}
            >
              Clear Transcript
            </button>

            {canReapplyTranscript && (
              <button
                className="reapply-transcript-button"
                type="button"
                onClick={handleReapplyTranscriptResults}
                disabled={isReapplyingTranscript}
              >
                {isReapplyingTranscript ? 'Re-applying...' : 'Re-apply Transcript'}
              </button>
            )}
          </div>

          {uploadMessage && <p className="upload-success">{uploadMessage}</p>}
          {!uploadMessage && hasTranscriptResults && (
            <p className="upload-success">{transcriptSummaryMessage}</p>
          )}
          {uploadError && <p className="upload-error">{uploadError}</p>}

          {hasTranscriptResults && (
            <div className="transcript-summary-grid">
              <div className="transcript-summary-item">
                <strong>{transcriptCompletedCourseCount}</strong>
                <span>Completed Modules</span>
              </div>
              <div className="transcript-summary-item transcript-au-summary-item">
                <strong>{formatAcademicUnits(transcriptTotalAcademicUnitsEarned)}</strong>
                <span>Total AU Earned</span>
              </div>
            </div>
          )}
        </section>
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
