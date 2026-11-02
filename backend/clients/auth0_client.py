"""Auth0 OIDC client using Authlib.

Registers the Auth0 provider and exposes helpers for the login/callback/logout
flow. The oauth object is used directly in the auth router.
"""

from authlib.integrations.starlette_client import OAuth

from backend.auth.settings import AUTH0_CLIENT_ID, AUTH0_CLIENT_SECRET, AUTH0_DOMAIN, APP_BASE_URL

oauth = OAuth()

oauth.register(
    name="auth0",
    client_id=AUTH0_CLIENT_ID,
    client_secret=AUTH0_CLIENT_SECRET,
    server_metadata_url=f"https://{AUTH0_DOMAIN}/.well-known/openid-configuration",
    client_kwargs={"scope": "openid profile email"},
)


def build_auth0_logout_url() -> str:
    """Returns the Auth0 logout URL that clears the Auth0 session and returns to APP_BASE_URL."""
    return (
        f"https://{AUTH0_DOMAIN}/v2/logout"
        f"?client_id={AUTH0_CLIENT_ID}"
        f"&returnTo={APP_BASE_URL}/"
    )
