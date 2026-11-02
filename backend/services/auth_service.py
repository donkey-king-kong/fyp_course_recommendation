"""Pure authentication logic: email validation and session user construction."""

from typing import Any

_NTU_STUDENT_DOMAIN = "@e.ntu.edu.sg"


def is_allowed_ntu_email(email: str) -> bool:
    return email.lower().endswith(_NTU_STUDENT_DOMAIN)


def build_session_user(claims: dict[str, Any]) -> dict[str, str]:
    """Extract the fields we keep in the session from Auth0 ID-token claims."""
    return {
        "sub": claims["sub"],
        "email": claims.get("email", ""),
        "name": claims.get("name", ""),
    }
