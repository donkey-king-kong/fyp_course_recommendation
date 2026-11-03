"""Capture live backend recommendation outputs for benchmark cases.

Run the FastAPI backend separately before using this script. The output JSON can
then be passed into `scripts/evaluate_recommendation_benchmark.py`.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Optional
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

DEFAULT_BENCHMARK_PATH = "data/recommendation_benchmark_cases.json"
DEFAULT_OUTPUT_PATH = "data/recommendation_benchmark_predictions.json"
DEFAULT_API_URL = "http://127.0.0.1:8000/recommendations"
REPO_ROOT = Path(__file__).resolve().parents[1]
PROVENANCE_FILES = (
    "data/modules.json", "data/ntu_prerequisite_unlock_graph.json", "data/course_catalog.json",
    "data/course_offerings.json", "data/mpe_specialisation_paths.json",
    "backend/services/career_skill_mappings.py", "backend/services/recommendation_service.py",
    "backend/services/prerequisite_rules.py",
    "backend/database/seed.py",
)

# Local capture provenance is not proof of which code or dataset a remote process serves.
def capture_provenance(
    serving_revision: Optional[str] = None,
    database_fingerprint: Optional[str] = None,
) -> dict[str, Any]:
    try:
        revision = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=REPO_ROOT, text=True).strip()
        dirty = bool(subprocess.check_output(["git", "status", "--porcelain"], cwd=REPO_ROOT, text=True))
    except (OSError, subprocess.CalledProcessError):
        revision, dirty = None, None
    hashes = {
        name: hashlib.sha256((REPO_ROOT / name).read_bytes()).hexdigest()
        for name in PROVENANCE_FILES if (REPO_ROOT / name).is_file()
    }
    return {
        "capturedAt": datetime.now(timezone.utc).isoformat(),
        "localCaptureRevision": revision,
        "localCaptureWorktreeDirty": dirty,
        "localFileSha256": hashes,
        "servingRevision": serving_revision,
        "servingRevisionEvidence": "operator-declared" if serving_revision else "unverified",
        "databaseFingerprint": database_fingerprint,
        "databaseFingerprintEvidence": "operator-declared" if database_fingerprint else "unverified",
        "databaseState": "unverified; local seed hashes do not identify the serving database",
    }

def parse_database_fingerprint(value: str) -> str:
    if len(value) != 64 or any(character not in "0123456789abcdefABCDEF" for character in value):
        raise argparse.ArgumentTypeError("Provide only a SHA-256 hex digest, never database credentials or a connection URL.")
    return value.lower()

def add_provenance_args(parser: argparse.ArgumentParser) -> None:
    parser.add_argument(
        "--serving-revision",
        help="Operator-declared backend revision after confirming its launch; not independently verified. Never pass credentials.",
    )
    parser.add_argument(
        "--database-fingerprint", type=parse_database_fingerprint,
        help="Operator-declared SHA-256 digest of a read-only database snapshot; not independent proof of the serving database.",
    )

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

def fixed_curriculum_courses(case: dict[str, Any]) -> list[Any]:
    return [
        item for item in case.get("curriculumCourses", [])
        if not (isinstance(item, dict) and item.get("isChoiceSlot"))
        and str(course_code_from_curriculum_item(item) or "").upper() not in {"BDE", "MPE"}
        and "XXX" not in str(course_code_from_curriculum_item(item) or "").upper()
    ]

def build_recommendation_request(case: dict[str, Any], limit_override: Optional[int]) -> dict[str, Any]:
    choice_slots = case.get("choiceSlots", [])
    choice_slot_codes = []
    for slot in choice_slots:
        slot_code = str(slot.get("courseCode", "")).strip()
        if slot_code and slot_code not in choice_slot_codes:
            choice_slot_codes.append(slot_code)

    curriculum_courses = normalise_curriculum_courses(case)
    limit = limit_override if limit_override is not None else case.get("limit", max(1, len(choice_slots)))
    fixed_courses = fixed_curriculum_courses(case)
    excluded_titles = list(dict.fromkeys([
        *case.get("excludedCourseTitles", []),
        *(item["title"] for item in fixed_courses if isinstance(item, dict) and item.get("title")),
    ]))
    return {
        "careerGoal": case["careerGoal"],
        "preferredRecommendationTags": case.get("preferredRecommendationTags", []),
        "studentFaculty": case.get("studentFaculty"),
        "completedCourseCodes": case.get("completedCourseCodes", []),
        "choiceSlotCodes": choice_slot_codes,
        "choiceSlots": choice_slots,
        "curriculumCourses": curriculum_courses,
        "excludedCourseCodes": unique_course_codes([*fixed_courses, *case.get("excludedCourseCodes", [])]),
        "excludedCourseTitles": excluded_titles,
        "limit": limit,
    }

def post_json(api_url: str, payload: dict[str, Any], timeout: float) -> dict[str, Any]:
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
    serving_revision: Optional[str] = None,
    database_fingerprint: Optional[str] = None,
) -> dict[str, Any]:
    cases = []
    for case in benchmark.get("cases", []):
        request_payload = build_recommendation_request(case, limit_override)
        try:
            response_payload = post_json(api_url, request_payload, timeout)
            cases.append(
                {
                    "caseId": case["caseId"],
                    "request": request_payload,
                    "recommendations": response_payload.get("recommendations", []),
                    "response": response_payload,
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
        "source": "live-backend",
        "generatedAt": datetime.now(timezone.utc).isoformat(),
        "apiUrl": api_url,
        "benchmarkStatus": benchmark.get("status"),
        "provenance": capture_provenance(serving_revision, database_fingerprint),
        "cases": cases,
    }

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Call the live backend recommender for each benchmark case and save predictions."
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
        help="Live backend POST /recommendations URL.",
    )
    parser.add_argument(
        "--timeout",
        type=float,
        default=30.0,
        help="Per-request timeout in seconds.",
    )
    parser.add_argument(
        "--limit",
        type=int,
        help="Optional recommendation limit override for every case. Defaults to each case's slot count.",
    )
    add_provenance_args(parser)
    return parser.parse_args()

def main() -> None:
    args = parse_args()
    benchmark = load_json(Path(args.benchmark))
    predictions = capture_predictions(
        benchmark=benchmark,
        api_url=args.api_url,
        timeout=args.timeout,
        limit_override=args.limit,
        serving_revision=args.serving_revision,
        database_fingerprint=args.database_fingerprint,
    )
    write_json(Path(args.output), predictions)
    print(f"Saved predictions for {len(predictions['cases'])} cases to {args.output}")

if __name__ == "__main__":
    main()
