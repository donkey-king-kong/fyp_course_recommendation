import { useState } from 'react'
import { useProfileStore } from '../store/useProfileStore'
import './LoginPage.css'

const STUDENT_ID_PATTERN = /^[A-Z]{4}\d{4}$/

function LoginPage() {
  // Write profile updates into the shared browser-persisted profile store
  const updateProfile = useProfileStore((state) => state.updateProfile)

  // Keep what the user is typing before it is saved into the profile store
  const [studentIdInput, setStudentIdInput] = useState('')
  const [error, setError] = useState('')

  function handleSubmit(event: { preventDefault: () => void }) {
    // HTML forms reload the page by default
    // React handles this submit instead.
    event.preventDefault()

    const normalizedStudentId = studentIdInput.trim().toUpperCase()

    // Empty Student ID should not create a profile
    if (!normalizedStudentId) {
      setError('Enter your Student ID to continue.')
      return
    }

    // Student IDs currently follow a four-letter, four-digit format.
    if (!STUDENT_ID_PATTERN.test(normalizedStudentId)) {
      setError('Enter a valid Student ID using 4 letters followed by 4 numbers.')
      return
    }

    setError('')

    // Normalizes the Student ID again before saving it
    updateProfile({ studentId: normalizedStudentId })
  }

  return (
    <main className="login-shell">
      <section className="login-card">
        <p className="login-eyebrow">NTU Course Recommender</p>
        <h1>Start with your student profile</h1>
        <p className="login-copy">
          Enter your Student ID to continue. This identifies your profile and keeps
          your roadmap progress available.
        </p>

        <form className="login-form" onSubmit={handleSubmit}>
          {/* Student ID is the user identity for the profile flow. */}
          <label>
            <span>Student ID</span>
            <input
              type="text"
              value={studentIdInput}
              onChange={(event) => {
                setStudentIdInput(event.target.value)
                setError('')
              }}
              placeholder="Enter your student ID"
              aria-invalid={Boolean(error)}
              aria-describedby={error ? 'student-id-error' : undefined}
              autoFocus
            />
          </label>

          {error && (
            <p className="login-error" id="student-id-error">
              {error}
            </p>
          )}

          <button type="submit">Continue</button>
        </form>
      </section>
    </main>
  )
}

export default LoginPage
