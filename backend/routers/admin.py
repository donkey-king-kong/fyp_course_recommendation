import os
import secrets
from typing import Optional

from fastapi import APIRouter, Header, HTTPException, Query, status

from backend.schemas.admin import (
    AdminBenchmarkCaseDetailResponse,
    AdminBenchmarkSummaryResponse,
    AdminLoginRequest,
    AdminLoginResponse,
)
from backend.services.admin_benchmark_service import (
    get_admin_benchmark_case_detail,
    get_admin_benchmark_summary,
)

router = APIRouter(prefix="/admin", tags=["Admin"])
DEFAULT_ADMIN_USERNAME = "admin"
DEFAULT_ADMIN_PASSWORD = "admin"
DEFAULT_ADMIN_TOKEN = "local-admin-token"

def get_admin_username() -> str:
    return os.getenv("ADMIN_USERNAME", DEFAULT_ADMIN_USERNAME)

def get_admin_password() -> str:
    return os.getenv("ADMIN_PASSWORD", DEFAULT_ADMIN_PASSWORD)

def get_admin_token() -> str:
    return os.getenv("ADMIN_TOKEN", DEFAULT_ADMIN_TOKEN)

def require_admin_token(x_admin_token: Optional[str] = Header(default=None)) -> None:
    if not x_admin_token or not secrets.compare_digest(x_admin_token, get_admin_token()):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Admin login required.",
        )

@router.post(
    "/login",
    response_model=AdminLoginResponse,
    summary="Log in to the local admin evaluation dashboard",
    response_description="Prototype admin session token for read-only benchmark endpoints.",
)
def login_admin(request: AdminLoginRequest) -> AdminLoginResponse:
    is_valid_username = secrets.compare_digest(request.username, get_admin_username())
    is_valid_password = secrets.compare_digest(request.password, get_admin_password())
    if not is_valid_username or not is_valid_password:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid admin credentials.",
        )

    return AdminLoginResponse(isAdmin=True, token=get_admin_token())

@router.get(
    "/benchmark",
    response_model=AdminBenchmarkSummaryResponse,
    summary="Read recommendation benchmark summary",
    response_description="Benchmark metrics and case summaries sorted with weak cases first.",
)
def read_admin_benchmark_summary(
    x_admin_token: Optional[str] = Header(default=None, alias="X-Admin-Token"),
    k: int = Query(default=5, ge=1, le=20, description="Ranking cutoff used for summary metrics."),
) -> AdminBenchmarkSummaryResponse:
    require_admin_token(x_admin_token)
    return get_admin_benchmark_summary(k=k)

@router.get(
    "/benchmark/{case_id}",
    response_model=AdminBenchmarkCaseDetailResponse,
    summary="Read one recommendation benchmark case",
    response_description="Benchmark inputs, labels, saved predictions, metrics, and score breakdowns.",
)
def read_admin_benchmark_case(
    case_id: str,
    x_admin_token: Optional[str] = Header(default=None, alias="X-Admin-Token"),
    k: int = Query(default=5, ge=1, le=20, description="Ranking cutoff used for case metrics."),
) -> AdminBenchmarkCaseDetailResponse:
    require_admin_token(x_admin_token)
    result = get_admin_benchmark_case_detail(case_id, k=k)
    if result is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Benchmark case not found.",
        )

    return result
