from fastapi import APIRouter, HTTPException, Query, Request, status
from fastapi.responses import RedirectResponse

from backend.schemas.auth import AuthenticatedUser
from backend.services.auth_service import (
    build_authorization_url,
    build_frontend_error_url,
    clear_session_user,
    complete_authorization,
    get_session_user,
)

router = APIRouter(prefix="/auth", tags=["Authentication"])

AUTH_NOT_SIGNED_IN_RESPONSE = {
    "description": "No active app session exists.",
    "content": {"application/json": {"example": {"detail": "Not signed in."}}},
}


@router.get(
    "/login",
    summary="Start NTU Microsoft sign-in",
    description=(
        "Redirects the browser to Microsoft Azure AD using the OAuth 2.0 Authorization "
        "Code flow. The backend stores a temporary state value in the signed session "
        "cookie and validates it when Microsoft redirects back."
    ),
    response_description="Redirect to Microsoft login.",
)
def login(request: Request) -> RedirectResponse:
    authorization_url = build_authorization_url(request)
    return RedirectResponse(authorization_url)


@router.get(
    "/callback",
    summary="Handle Microsoft sign-in callback",
    description=(
        "Receives the Microsoft authorization code, exchanges it with MSAL, validates "
        "the NTU identity claims, stores a safe app session, and redirects back to the "
        "frontend. Azure access tokens are not returned to the browser."
    ),
    response_description="Redirect to the frontend after login.",
)
def callback(
    request: Request,
    code: str | None = Query(default=None, description="Authorization code returned by Microsoft."),
    state: str | None = Query(default=None, description="State value returned by Microsoft."),
    error: str | None = Query(default=None, description="OAuth error returned by Microsoft."),
    error_description: str | None = Query(default=None, description="OAuth error details returned by Microsoft."),
) -> RedirectResponse:
    if error:
        message = error_description or error
        return RedirectResponse(build_frontend_error_url(message))

    if not code:
        return RedirectResponse(build_frontend_error_url("Microsoft login did not return an authorization code."))

    try:
        frontend_url = complete_authorization(request, code, state)
    except HTTPException as auth_error:
        return RedirectResponse(build_frontend_error_url(str(auth_error.detail)))

    return RedirectResponse(frontend_url)


@router.get(
    "/me",
    response_model=AuthenticatedUser,
    summary="Get current signed-in user",
    description="Returns the current app session user if the browser has a valid signed session cookie.",
    response_description="Current authenticated NTU user.",
    responses={401: AUTH_NOT_SIGNED_IN_RESPONSE},
)
def read_current_user(request: Request) -> AuthenticatedUser:
    user = get_session_user(request)

    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not signed in.")

    return user


@router.post(
    "/logout",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Log out current user",
    description="Clears the app-owned session cookie for the current browser.",
    response_description="Session cleared.",
)
def logout(request: Request) -> None:
    clear_session_user(request)
