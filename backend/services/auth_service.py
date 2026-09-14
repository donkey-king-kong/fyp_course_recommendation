from __future__ import annotations

import os
import secrets
from dataclasses import dataclass
from urllib.parse import urlencode

import msal
from dotenv import load_dotenv
from fastapi import HTTPException, Request, status

from backend.schemas.auth import AuthenticatedUser

load_dotenv()

AUTH_SCOPES = ["User.Read"]
AUTH_SESSION_STATE_KEY = "auth_state"
AUTH_SESSION_USER_KEY = "auth_user"
NTU_EMAIL_DOMAIN = "@ntu.edu.sg"
AUTHORITY_HOST = "https://login.microsoftonline.com/"
UNPINNED_AUTHORITY_SEGMENTS = {"common", "organizations", "consumers"}


@dataclass(frozen=True)
class AuthSettings:
    client_id: str
    client_secret: str
    authority: str
    redirect_uri: str
    frontend_url: str


def get_auth_settings() -> AuthSettings:
    client_id = os.getenv("APP_REG_CLIENT_ID", "").strip()
    client_secret = os.getenv("APP_REG_CLIENT_SECRET", "").strip()
    authority = os.getenv("AUTHORITY", "").strip().rstrip("/")
    redirect_uri = os.getenv("AUTH_REDIRECT_URI", "").strip()
    frontend_url = os.getenv("FRONTEND_URL", "http://127.0.0.1:5173").strip().rstrip("/")
    missing_names = [
        name
        for name, value in {
            "APP_REG_CLIENT_ID": client_id,
            "APP_REG_CLIENT_SECRET": client_secret,
            "AUTHORITY": authority,
            "AUTH_REDIRECT_URI": redirect_uri,
        }.items()
        if not value
    ]

    if missing_names:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"Auth is not configured. Missing: {', '.join(missing_names)}.",
        )

    if not is_pinned_tenant_authority(authority):
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="AUTHORITY must be pinned to the NTU Azure tenant, not common/organizations/consumers.",
        )

    return AuthSettings(
        client_id=client_id,
        client_secret=client_secret,
        authority=authority,
        redirect_uri=redirect_uri,
        frontend_url=frontend_url,
    )


def is_pinned_tenant_authority(authority: str) -> bool:
    if not authority.startswith(AUTHORITY_HOST) or "<" in authority or ">" in authority:
        return False

    tenant_segment = authority.removeprefix(AUTHORITY_HOST).strip("/")
    return bool(tenant_segment) and tenant_segment.lower() not in UNPINNED_AUTHORITY_SEGMENTS


def create_msal_app(settings: AuthSettings) -> msal.ConfidentialClientApplication:
    return msal.ConfidentialClientApplication(
        client_id=settings.client_id,
        authority=settings.authority,
        client_credential=settings.client_secret,
    )


def build_authorization_url(request: Request) -> str:
    settings = get_auth_settings()
    state = secrets.token_urlsafe(32)
    request.session[AUTH_SESSION_STATE_KEY] = state
    app = create_msal_app(settings)

    return app.get_authorization_request_url(
        scopes=AUTH_SCOPES,
        redirect_uri=settings.redirect_uri,
        state=state,
        prompt="select_account",
    )


def complete_authorization(request: Request, code: str, state: str | None) -> str:
    settings = get_auth_settings()
    expected_state = request.session.pop(AUTH_SESSION_STATE_KEY, None)

    if not expected_state or not state or state != expected_state:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid login state.")

    app = create_msal_app(settings)
    token_result = app.acquire_token_by_authorization_code(
        code=code,
        scopes=AUTH_SCOPES,
        redirect_uri=settings.redirect_uri,
    )

    if "error" in token_result:
        error_description = token_result.get("error_description", "Microsoft login failed.")
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=error_description)

    claims = token_result.get("id_token_claims") or {}
    user = build_authenticated_user(claims)
    request.session[AUTH_SESSION_USER_KEY] = user.model_dump()
    return settings.frontend_url


def build_authenticated_user(claims: dict) -> AuthenticatedUser:
    oid = str(claims.get("oid") or "").strip()
    email = str(claims.get("preferred_username") or "").strip()
    name = str(claims.get("name") or email or "NTU Student").strip()

    if not oid:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Microsoft login did not return an oid.")

    if not email.lower().endswith(NTU_EMAIL_DOMAIN):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Please sign in with an NTU email account.")

    return AuthenticatedUser(oid=oid, email=email, name=name)


def get_session_user(request: Request) -> AuthenticatedUser | None:
    user_data = request.session.get(AUTH_SESSION_USER_KEY)

    if not isinstance(user_data, dict):
        return None

    try:
        return AuthenticatedUser.model_validate(user_data)
    except ValueError:
        request.session.pop(AUTH_SESSION_USER_KEY, None)
        return None


def clear_session_user(request: Request) -> None:
    request.session.pop(AUTH_SESSION_USER_KEY, None)
    request.session.pop(AUTH_SESSION_STATE_KEY, None)


def build_frontend_error_url(message: str) -> str:
    settings = get_auth_settings()
    query = urlencode({"authError": message})
    return f"{settings.frontend_url}/?{query}"
