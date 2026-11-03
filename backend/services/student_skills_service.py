import json
from pathlib import Path

from backend.schemas.student_skills import (
    CourseSkillEvidence,
    StudentSkillArea,
    StudentSkillsRequest,
    StudentSkillsResponse,
)

EVIDENCE_PATH = Path(__file__).resolve().parents[2] / "data" / "student_skill_evidence.json"
PILOT_EVIDENCE = json.loads(EVIDENCE_PATH.read_text(encoding="utf-8"))

def normalize_codes(codes: list[str]) -> list[str]:
    return list(dict.fromkeys(code.strip().upper() for code in codes if code.strip()))

def build_student_skills_picture(request: StudentSkillsRequest) -> StudentSkillsResponse:
    completed = normalize_codes(request.completedCourseCodes)
    completed_set = set(completed)
    candidates = [code for code in normalize_codes(request.candidateCourseCodes) if code not in completed_set]
    candidate_set = set(candidates)
    role_skills = [
        skill for skill in PILOT_EVIDENCE["skills"] if request.careerGoal in skill["roleSkillAreas"]
    ]
    role_skill_ids = {skill["id"] for skill in role_skills}
    mapped_codes = {
        entry["courseCode"]
        for entry in PILOT_EVIDENCE["courseEvidence"]
        if entry["skillId"] in role_skill_ids
    }
    skills = []

    for skill in role_skills:
        prior_learning = [
            CourseSkillEvidence(
                courseCode=entry["courseCode"],
                depth=entry["depth"],
                excerpt=entry["excerpt"],
                source=PILOT_EVIDENCE["source"],
            )
            for entry in PILOT_EVIDENCE["courseEvidence"]
            if entry["skillId"] == skill["id"] and entry["courseCode"] in completed_set
        ]
        candidate_learning = [
            CourseSkillEvidence(
                courseCode=entry["courseCode"],
                depth=entry["depth"],
                excerpt=entry["excerpt"],
                source=PILOT_EVIDENCE["source"],
            )
            for entry in PILOT_EVIDENCE["courseEvidence"]
            if entry["skillId"] == skill["id"] and entry["courseCode"] in candidate_set
        ]
        prior_level = "unknown"
        if any(item.depth == "advanced" for item in prior_learning):
            prior_level = "advanced-exposure"
        elif prior_learning:
            prior_level = "introductory-exposure"

        skills.append(StudentSkillArea(
            skillId=skill["id"],
            label=skill["label"],
            roleSkillArea=skill["roleSkillAreas"][request.careerGoal],
            priorLearningLevel=prior_level,
            priorLearning=prior_learning,
            candidateLearning=candidate_learning,
        ))

    return StudentSkillsResponse(
        careerGoal=request.careerGoal,
        skills=skills,
        unmappedCompletedCourseCodes=[code for code in completed if code not in mapped_codes],
        unmappedCandidateCourseCodes=[code for code in candidates if code not in mapped_codes],
    )
