"""Auth0 OAuth routes: login initiation, callback, logout, session check."""

from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import JSONResponse, RedirectResponse

from backend.auth.settings import APP_BASE_URL, FRONTEND_URL
from backend.clients.auth0_client import build_auth0_logout_url, oauth
from backend.schemas.auth import AuthUser
from backend.services.auth_service import build_session_user, is_allowed_ntu_email

router = APIRouter(tags=["auth"])


@router.get(
    "/login",
    summary="Initiate Auth0 Microsoft SSO login",
    description="Redirects the browser to Auth0, which forwards to the Microsoft login screen.",
    response_description="Redirect to Auth0 authorization endpoint",
    status_code=302,
)
async def login(request: Request) -> RedirectResponse:
    redirect_uri = f"{APP_BASE_URL}/callback"
    # Remove connection= to use Auth0's universal login page (lets user pick any enabled connection).
    # Add connection="windowslive" once the Microsoft social connection is enabled in Auth0 dashboard.
    return await oauth.auth0.authorize_redirect(
        request,
        redirect_uri,
    )


@router.get(
    "/callback",
    summary="Handle Auth0 OAuth callback",
    description=(
        "Receives the authorization code from Auth0, exchanges it for an ID token, "
        "validates that the email belongs to @e.ntu.edu.sg, and stores the user in the session."
    ),
    response_description="Redirect to the frontend after successful login",
    status_code=302,
    responses={403: {"description": "Email is not from an allowed NTU student domain"}},
)
async def callback(request: Request) -> RedirectResponse:
    token = await oauth.auth0.authorize_access_token(request)
    claims = token.get("userinfo") or token.get("id_token_claims", {})
    email: str = claims.get("email", "")

    if not is_allowed_ntu_email(email):
        request.session.clear()
        raise HTTPException(
            status_code=403,
            detail="Access is restricted to NTU student accounts (@e.ntu.edu.sg).",
        )

    request.session["user"] = build_session_user(claims)
    return RedirectResponse(url=f"{FRONTEND_URL}?login=success")


@router.get(
    "/logout",
    summary="Log out and clear the session",
    description="Clears the server-side session and redirects to Auth0 logout to end the SSO session.",
    response_description="Redirect to Auth0 logout endpoint",
    status_code=302,
)
async def logout(request: Request) -> RedirectResponse:
    request.session.clear()
    return RedirectResponse(url=build_auth0_logout_url())


@router.get(
    "/",
    summary="Post-logout landing redirect",
    description="Auth0 returns here after logout (matches the configured Logout URL). Redirects to the frontend.",
    response_description="Redirect to frontend",
    status_code=302,
    include_in_schema=False,
)
async def root_redirect() -> RedirectResponse:
    return RedirectResponse(url=FRONTEND_URL)


@router.get(
    "/me",
    summary="Get the currently authenticated user",
    description="Returns the signed-in user's sub, email, and name from the session.",
    response_model=AuthUser,
    responses={401: {"description": "Not authenticated"}},
)
async def me(request: Request) -> JSONResponse:
    user = request.session.get("user")
    if not user:
        raise HTTPException(status_code=401, detail="Not authenticated")
    return JSONResponse(content=user)
