"""Capture live backend recommendation outputs for benchmark cases.

By default this script now runs the FastAPI app in-process using TestClient so
no running server is required. Pass --live to call a running backend instead.
The output JSON can then be passed into `scripts/evaluate_recommendation_benchmark.py`.
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Optional
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

DEFAULT_BENCHMARK_PATH = "data/recommendation_benchmark_cases.json"
DEFAULT_OUTPUT_PATH = "data/recommendation_benchmark_predictions.json"
DEFAULT_API_URL = "http://127.0.0.1:8000/recommendations"


def get_post_fn(live: bool) -> Any:
    """Return either the live HTTP post_json or the in-process TestClient version."""
    return post_json if live else _get_testclient_post_json()


def _get_testclient_post_json() -> Any:
    """Return a post_json function backed by TestClient with auth bypassed."""
    # Add the repo root to sys.path so backend imports resolve when the script
    # is run from anywhere inside the project.
    repo_root = Path(__file__).resolve().parent.parent
    if str(repo_root) not in sys.path:
        sys.path.insert(0, str(repo_root))

    from fastapi.testclient import TestClient
    from backend.main import app
    from backend.dependencies.auth import require_user

    _EVAL_USER = {"sub": "eval-script", "email": "eval@script", "name": "Eval Script"}
    app.dependency_overrides[require_user] = lambda: _EVAL_USER
    client = TestClient(app, raise_server_exceptions=True)

    def _post_json(api_url: str, payload: dict[str, Any], timeout: float) -> dict[str, Any]:
        response = client.post("/recommendations", json=payload)
        response.raise_for_status()
        return response.json()

    return _post_json

def load_json(path: Path) -> dict[str, Any]:
    with path.open() as file:
        return json.load(file)

def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w") as file:
        json.dump(payload, file, indent=2)
        file.write("\n")

def course_code_from_curriculum_item(item: Any) -> Optional[str]:
    if isinstance(item, str):
        return item
    if isinstance(item, dict):
        code = item.get("courseCode")
        return str(code) if code else None
    return None

def normalise_curriculum_courses(case: dict[str, Any]) -> list[dict[str, Any]]:
    curriculum_courses = []
    for item in case.get("curriculumCourses", []):
        if isinstance(item, dict):
            curriculum_courses.append(item)
            continue

        course_code = course_code_from_curriculum_item(item)
        if course_code:
            curriculum_courses.append({"courseCode": course_code})
    return curriculum_courses

def unique_course_codes(items: list[Any]) -> list[str]:
    seen = set()
    course_codes = []
    for item in items:
        course_code = course_code_from_curriculum_item(item)
        if not course_code:
            continue

        normalized_code = course_code.strip().upper()
        if normalized_code and normalized_code not in seen:
            seen.add(normalized_code)
            course_codes.append(normalized_code)
    return course_codes

def build_recommendation_request(case: dict[str, Any], limit_override: Optional[int]) -> dict[str, Any]:
    choice_slots = case.get("choiceSlots", [])
    choice_slot_codes = []
    for slot in choice_slots:
        slot_code = str(slot.get("courseCode", "")).strip()
        if slot_code and slot_code not in choice_slot_codes:
            choice_slot_codes.append(slot_code)

    curriculum_courses = normalise_curriculum_courses(case)
    limit = limit_override if limit_override is not None else max(1, len(choice_slots))
    return {
        "careerGoal": case["careerGoal"],
        "preferredRecommendationTags": case.get("preferredRecommendationTags", []),
        "studentFaculty": case.get("studentFaculty"),
        "completedCourseCodes": case.get("completedCourseCodes", []),
        "choiceSlotCodes": choice_slot_codes,
        "choiceSlots": choice_slots,
        "curriculumCourses": curriculum_courses,
        "excludedCourseCodes": unique_course_codes(case.get("curriculumCourses", [])),
        "excludedCourseTitles": [],
        "limit": limit,
    }

def post_json(api_url: str, payload: dict[str, Any], timeout: float) -> dict[str, Any]:
    """Call the recommendations endpoint over HTTP. Used when --live is passed."""
    encoded_payload = json.dumps(payload).encode("utf-8")
    request = Request(
        api_url,
        data=encoded_payload,
        headers={
            "Content-Type": "application/json",
            "Accept": "application/json",
        },
        method="POST",
    )
    with urlopen(request, timeout=timeout) as response:
        return json.loads(response.read().decode("utf-8"))

def capture_predictions(
    benchmark: dict[str, Any],
    api_url: str,
    timeout: float,
    limit_override: Optional[int],
    post_fn: Any = None,
) -> dict[str, Any]:
    if post_fn is None:
        post_fn = post_json
    cases = []
    for case in benchmark.get("cases", []):
        request_payload = build_recommendation_request(case, limit_override)
        try:
            response_payload = post_fn(api_url, request_payload, timeout)
            cases.append(
                {
                    "caseId": case["caseId"],
                    "request": request_payload,
                    "recommendations": response_payload.get("recommendations", []),
                }
            )
        except HTTPError as error:
            error_body = error.read().decode("utf-8", errors="replace")
            raise SystemExit(
                f"{case['caseId']} failed with HTTP {error.code}: {error_body}"
            ) from error
        except URLError as error:
            raise SystemExit(
                f"Could not reach {api_url}. Start the FastAPI backend first. Details: {error.reason}"
            ) from error

    return {
        "source": "in-process" if post_fn is not post_json else "live-backend",
        "generatedAt": datetime.now(timezone.utc).isoformat(),
        "apiUrl": api_url,
        "benchmarkStatus": benchmark.get("status"),
        "cases": cases,
    }

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Call the backend recommender for each benchmark case and save predictions."
    )
    parser.add_argument(
        "--benchmark",
        default=DEFAULT_BENCHMARK_PATH,
        help="Path to the benchmark cases JSON file.",
    )
    parser.add_argument(
        "--output",
        default=DEFAULT_OUTPUT_PATH,
        help="Path where saved recommendation predictions JSON should be written.",
    )
    parser.add_argument(
        "--api-url",
        default=DEFAULT_API_URL,
        help="Live backend POST /recommendations URL (only used with --live).",
    )
    parser.add_argument(
        "--timeout",
        type=float,
        default=30.0,
        help="Per-request timeout in seconds (only used with --live).",
    )
    parser.add_argument(
        "--limit",
        type=int,
        help="Optional recommendation limit override for every case. Defaults to each case's slot count.",
    )
    parser.add_argument(
        "--live",
        action="store_true",
        help="Call a running backend server instead of running in-process. Requires the backend to be started separately.",
    )
    return parser.parse_args()

def main() -> None:
    args = parse_args()
    benchmark = load_json(Path(args.benchmark))
    post_fn = post_json if args.live else _get_testclient_post_json()
    predictions = capture_predictions(
        benchmark=benchmark,
        api_url=args.api_url,
        timeout=args.timeout,
        limit_override=args.limit,
        post_fn=post_fn,
    )
    write_json(Path(args.output), predictions)
    print(f"Saved predictions for {len(predictions['cases'])} cases to {args.output}")

if __name__ == "__main__":
    main()
