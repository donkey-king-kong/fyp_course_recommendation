"""Auth0 configuration loaded from environment variables.

Fails fast at import time if any required variable is missing, so a misconfigured
server surfaces the error immediately rather than at the first login attempt.
"""

import os

from dotenv import load_dotenv

load_dotenv()

def _require(name: str) -> str:
    value = os.getenv(name)
    if not value:
        raise RuntimeError(f"Missing required environment variable: {name}")
    return value

AUTH0_DOMAIN: str = _require("AUTH0_DOMAIN")
AUTH0_CLIENT_ID: str = _require("AUTH0_CLIENT_ID")
AUTH0_CLIENT_SECRET: str = _require("AUTH0_CLIENT_SECRET")
AUTH0_SECRET: str = _require("AUTH0_SECRET")
APP_BASE_URL: str = _require("APP_BASE_URL")
FRONTEND_URL: str = os.getenv("FRONTEND_URL", "http://localhost:5173")
