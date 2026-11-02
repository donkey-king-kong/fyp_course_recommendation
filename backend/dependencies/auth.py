"""FastAPI dependency that enforces an active session.

Raises 401 (JSON) rather than a redirect so the SPA can handle it cleanly.
"""

from typing import Any

from fastapi import HTTPException, Request


def require_user(request: Request) -> dict[str, Any]:
    user = request.session.get("user")
    if not user:
        raise HTTPException(status_code=401, detail="Not authenticated")
    return user
