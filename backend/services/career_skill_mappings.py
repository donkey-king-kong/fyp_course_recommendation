from dataclasses import dataclass

@dataclass(frozen=True)
class CareerSkillMapping:
    skill: str
    recommendation_tags: tuple[str, ...]
    weight: int
    rationale: str
    weight_rationale: str

# Static career mappings translate a career goal into skill areas, then into existing
# curated module tags. This keeps the signal inspectable before adding job-market data.
SOFTWARE_ENGINEER_SKILL_MAPPINGS = (
    CareerSkillMapping(
        skill="software design and delivery",
        recommendation_tags=(
            "software-engineering",
            "backend-engineering",
            "frontend-engineering",
            "programming",
            "web-development",
        ),
        weight=10,
        rationale=(
            "Software engineers need to design, implement, test, and maintain "
            "software systems across backend, frontend, and general programming work."
        ),
        weight_rationale=(
            "Highest weight because this is the most central skill area for the "
            "current Software Engineer career goal."
        ),
    ),
    CareerSkillMapping(
        skill="backend and data services",
        recommendation_tags=(
            "backend-engineering",
            "database",
            "distributed-systems",
            "cloud-computing",
        ),
        weight=8,
        rationale=(
            "Many software engineering roles involve APIs, data-backed services, "
            "service reliability, and scalable backend infrastructure."
        ),
        weight_rationale=(
            "High weight because backend and data-service knowledge strongly "
            "supports common full-stack and backend software roles."
        ),
    ),
    CareerSkillMapping(
        skill="systems and infrastructure",
        recommendation_tags=(
            "operating-systems",
            "computer-network",
            "distributed-systems",
            "cloud-computing",
            "parallel-computing",
        ),
        weight=7,
        rationale=(
            "Systems knowledge helps software engineers understand runtime behavior, "
            "networked applications, concurrency, and infrastructure constraints."
        ),
        weight_rationale=(
            "Medium-high weight because systems knowledge is important, but slightly "
            "less universal than core software design and backend service skills."
        ),
    ),
    CareerSkillMapping(
        skill="secure software practice",
        recommendation_tags=(
            "computer-security",
            "cryptography",
            "privacy",
        ),
        weight=6,
        rationale=(
            "Secure development matters when software handles user data, networked "
            "systems, authentication, privacy, or adversarial environments."
        ),
        weight_rationale=(
            "Medium weight because security is valuable for software roles, while "
            "specialist security depth may depend on the student's target role."
        ),
    ),
    CareerSkillMapping(
        skill="algorithmic problem solving",
        recommendation_tags=(
            "algorithms",
            "data-structures",
            "theory-of-computing",
        ),
        weight=5,
        rationale=(
            "Algorithmic thinking supports problem decomposition, performance "
            "reasoning, technical interviews, and implementation trade-offs."
        ),
        weight_rationale=(
            "Moderate weight because it supports software engineering broadly, but "
            "should not dominate more applied software-building signals."
        ),
    ),
)

CAREER_SKILL_MAPPINGS = {
    "software-engineer": SOFTWARE_ENGINEER_SKILL_MAPPINGS,
}
