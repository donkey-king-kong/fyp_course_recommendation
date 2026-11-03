from typing import Literal

from pydantic import BaseModel, Field

PilotCareerGoal = Literal["software-engineer", "data-engineer"]
LearningDepth = Literal["introductory", "advanced"]
PriorLearningLevel = Literal["unknown", "introductory-exposure", "advanced-exposure"]

class StudentSkillsRequest(BaseModel):
    careerGoal: PilotCareerGoal = Field(
        description="Pilot role whose existing static skill areas are shown.",
        examples=["data-engineer"],
    )
    completedCourseCodes: list[str] = Field(
        default_factory=list,
        description="User-supplied completed course codes; not a verified transcript or mastery record.",
        examples=[["SC3020"]],
    )
    candidateCourseCodes: list[str] = Field(
        default_factory=list,
        description="Courses to inspect for possible next learning, not an eligibility or ranking request.",
        examples=[["SC4023"]],
    )

class CourseSkillEvidence(BaseModel):
    courseCode: str
    depth: LearningDepth = Field(description="Course-content depth, not student proficiency.")
    excerpt: str = Field(description="Exact excerpt from the checked-in catalog description.")
    source: str = Field(description="Path to the source catalog in this repository.")

class StudentSkillArea(BaseModel):
    skillId: str = Field(description="Stable skill identifier across courses and applicable pilot roles.")
    label: str
    roleSkillArea: str = Field(
        description="Broader area in the static career mapping, not proof of every role-specific skill.",
    )
    priorLearningLevel: PriorLearningLevel = Field(
        description="Highest mapped course-content depth among submitted completions; never mastery.",
    )
    priorLearning: list[CourseSkillEvidence]
    candidateLearning: list[CourseSkillEvidence]

class StudentSkillsResponse(BaseModel):
    careerGoal: PilotCareerGoal
    skills: list[StudentSkillArea]
    unmappedCompletedCourseCodes: list[str] = Field(
        description="Submitted completions with no mapping for this role in the pilot ledger.",
    )
    unmappedCandidateCourseCodes: list[str] = Field(
        description="Submitted candidates with no mapping for this role in the pilot ledger.",
    )
