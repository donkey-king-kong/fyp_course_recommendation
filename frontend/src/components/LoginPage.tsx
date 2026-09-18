import { useState } from 'react'
import { loginAdmin } from '../api/adminApi'
import { useProfileStore } from '../store/useProfileStore'
import './LoginPage.css'

const STUDENT_ID_PATTERN = /^[A-Z]{4}\d{4}$/

interface LoginPageProps {
  onAdminLogin: (adminToken: string) => void
}

function LoginPage({ onAdminLogin }: LoginPageProps) {
  // Activate an existing browser-saved profile, or create one for this Student ID.
  const loginWithStudentId = useProfileStore((state) => state.loginWithStudentId)

  // Keep what the user is typing before it is saved into the profile store
  const [studentIdInput, setStudentIdInput] = useState('')
  const [adminUsernameInput, setAdminUsernameInput] = useState('')
  const [adminPasswordInput, setAdminPasswordInput] = useState('')
  const [isAdminLoginLoading, setIsAdminLoginLoading] = useState(false)
  const [error, setError] = useState('')
  const [adminError, setAdminError] = useState('')

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
      setError('Enter a valid Student ID.')
      return
    }

    setError('')

    // Load the saved browser profile for this ID, or create one if it is new
    loginWithStudentId(normalizedStudentId)
  }

  async function handleAdminSubmit(event: { preventDefault: () => void }) {
    event.preventDefault()

    if (!adminUsernameInput.trim() || !adminPasswordInput) {
      setAdminError('Enter the admin username and password.')
      return
    }

    try {
      setIsAdminLoginLoading(true)
      setAdminError('')
      const result = await loginAdmin({
        username: adminUsernameInput.trim(),
        password: adminPasswordInput,
      })
      onAdminLogin(result.token)
    } catch {
      setAdminError('Admin login failed. Check the local admin credentials.')
    } finally {
      setIsAdminLoginLoading(false)
    }
  }

  return (
    <main className="login-shell">
      <section className="login-card">
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

        <section className="admin-login-panel" aria-label="Admin benchmark access">
          <div>
            <h2>Admin benchmark access</h2>
            <p>
              Open the read-only benchmark dashboard for reviewing cases, labels,
              predictions, and score breakdowns.
            </p>
          </div>

          <form className="login-form" onSubmit={handleAdminSubmit}>
            <label>
              <span>Admin Username</span>
              <input
                type="text"
                value={adminUsernameInput}
                onChange={(event) => {
                  setAdminUsernameInput(event.target.value)
                  setAdminError('')
                }}
                placeholder="admin"
                autoComplete="username"
              />
            </label>

            <label>
              <span>Admin Password</span>
              <input
                type="password"
                value={adminPasswordInput}
                onChange={(event) => {
                  setAdminPasswordInput(event.target.value)
                  setAdminError('')
                }}
                placeholder="Local admin password"
                autoComplete="current-password"
              />
            </label>

            {adminError && (
              <p className="login-error" id="admin-login-error">
                {adminError}
              </p>
            )}

            <button type="submit" disabled={isAdminLoginLoading}>
              {isAdminLoginLoading ? 'Checking...' : 'Open Admin Dashboard'}
            </button>
          </form>
        </section>
      </section>
    </main>
  )
}

export default LoginPage
