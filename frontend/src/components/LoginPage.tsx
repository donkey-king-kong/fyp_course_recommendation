import { API_BASE_URL } from '../api/apiConfig'
import './LoginPage.css'

interface LoginPageProps {
  // Set to true when Auth0 returned a 403 (non-NTU account).
  accessDenied?: boolean
}

function LoginPage({ accessDenied = false }: LoginPageProps) {
  function handleSignIn() {
    window.location.href = `${API_BASE_URL}/login`
  }

  return (
    <main className="login-shell">
      <section className="login-card">
        <p className="login-eyebrow">NTU Course Recommender</p>
        <h1>Sign in with your NTU account</h1>
        <p className="login-copy">
          Use your NTU Microsoft account (@e.ntu.edu.sg) to continue. Your profile
          and roadmap progress will be saved to your account.
        </p>

        {accessDenied && (
          <p className="login-error" role="alert">
            Access is restricted to NTU student accounts. Please sign in with your @e.ntu.edu.sg email.
          </p>
        )}

        <button type="button" className="login-microsoft-button" onClick={handleSignIn}>
          Sign in with Microsoft
        </button>
      </section>
    </main>
  )
}

export default LoginPage
