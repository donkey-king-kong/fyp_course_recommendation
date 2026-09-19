import { useMemo } from 'react'
import { redirectToNtuLogin } from '../api/authApi'
import './LoginPage.css'

interface LoginPageProps {
  authError?: string
  isCheckingSession?: boolean
}

function LoginPage({ authError = '', isCheckingSession = false }: LoginPageProps) {
  const loginError = useMemo(() => {
    const queryError = new URLSearchParams(window.location.search).get('authError')
    return authError || queryError || ''
  }, [authError])

  return (
    <main className="login-shell">
      <section className="login-card">
        <p className="login-eyebrow">NTU Course Recommender</p>
        <h1>Sign in with NTU</h1>
        <p className="login-copy">
          Use your NTU Microsoft account to continue. The app uses your Azure Object ID
          as the stable profile key, not your email or matriculation number.
        </p>

        {loginError && (
          <p className="login-error" role="alert">
            {loginError}
          </p>
        )}

        <button
          className="login-button"
          type="button"
          onClick={redirectToNtuLogin}
          disabled={isCheckingSession}
        >
          {isCheckingSession ? 'Checking sign-in...' : 'Sign in with NTU'}
        </button>
      </section>
    </main>
  )
}

export default LoginPage
