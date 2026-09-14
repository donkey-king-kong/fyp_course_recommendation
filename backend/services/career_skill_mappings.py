from dataclasses import dataclass

@dataclass(frozen=True)
class SkillTagRelationship:
    tag: str
    relationship_weight: float
    tag_confidence: float
    rationale: str

@dataclass(frozen=True)
class CareerSkillMapping:
    skill: str
    tag_relationships: tuple[SkillTagRelationship, ...]
    weight: int
    rationale: str
    weight_rationale: str

# Static career mappings translate a career goal into skill areas, then into existing
# curated module tags. This keeps the signal inspectable before adding job-market data.
SOFTWARE_ENGINEER_SKILL_MAPPINGS = (
    CareerSkillMapping(
        skill="software design and delivery",
        tag_relationships=(
            SkillTagRelationship(
                tag="software-engineering",
                relationship_weight=1.0,
                tag_confidence=1.0,
                rationale="Directly represents structured software design and delivery practice.",
            ),
            SkillTagRelationship(
                tag="backend-engineering",
                relationship_weight=0.85,
                tag_confidence=1.0,
                rationale="Backend implementation is a major applied software delivery path.",
            ),
            SkillTagRelationship(
                tag="frontend-engineering",
                relationship_weight=0.8,
                tag_confidence=1.0,
                rationale="Frontend implementation is a major applied software delivery path.",
            ),
            SkillTagRelationship(
                tag="programming",
                relationship_weight=0.75,
                tag_confidence=0.9,
                rationale="Programming is foundational but can be broad or introductory.",
            ),
            SkillTagRelationship(
                tag="web-development",
                relationship_weight=0.65,
                tag_confidence=0.9,
                rationale="Web development is useful for software delivery but not universal to all roles.",
            ),
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
        tag_relationships=(
            SkillTagRelationship(
                tag="distributed-systems",
                relationship_weight=0.8,
                tag_confidence=1.0,
                rationale="Strongest signal for scalable backend services and service reliability.",
            ),
            SkillTagRelationship(
                tag="backend-engineering",
                relationship_weight=0.9,
                tag_confidence=1.0,
                rationale="Directly supports API and server-side service implementation.",
            ),
            SkillTagRelationship(
                tag="database",
                relationship_weight=0.8,
                tag_confidence=1.0,
                rationale="Data modelling and querying are common backend service responsibilities.",
            ),
            SkillTagRelationship(
                tag="cloud-computing",
                relationship_weight=0.7,
                tag_confidence=0.9,
                rationale="Cloud concepts support deployment and operations, but may be broader than backend work.",
            ),
            SkillTagRelationship(
                tag="web-development",
                relationship_weight=0.5,
                tag_confidence=0.85,
                rationale="Web modules can support service integration, but are weaker backend evidence.",
            ),
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
        tag_relationships=(
            SkillTagRelationship(
                tag="operating-systems",
                relationship_weight=1.0,
                tag_confidence=1.0,
                rationale="Direct systems foundation for runtime, memory, process, and concurrency behavior.",
            ),
            SkillTagRelationship(
                tag="distributed-systems",
                relationship_weight=0.95,
                tag_confidence=1.0,
                rationale="Strong signal for infrastructure and networked software behavior.",
            ),
            SkillTagRelationship(
                tag="computer-network",
                relationship_weight=0.75,
                tag_confidence=1.0,
                rationale="Networking knowledge directly supports distributed and internet-facing software.",
            ),
            SkillTagRelationship(
                tag="cloud-computing",
                relationship_weight=0.75,
                tag_confidence=0.9,
                rationale="Cloud modules often cover deployment platforms and infrastructure concepts.",
            ),
            SkillTagRelationship(
                tag="parallel-computing",
                relationship_weight=0.6,
                tag_confidence=0.85,
                rationale="Parallel computing is useful for performance but more specialised.",
            ),
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
        tag_relationships=(
            SkillTagRelationship(
                tag="computer-security",
                relationship_weight=1.0,
                tag_confidence=1.0,
                rationale="Directly represents secure software and systems practice.",
            ),
            SkillTagRelationship(
                tag="privacy",
                relationship_weight=0.75,
                tag_confidence=0.9,
                rationale="Privacy is important for responsible data-handling software.",
            ),
            SkillTagRelationship(
                tag="cryptography",
                relationship_weight=0.65,
                tag_confidence=0.9,
                rationale="Cryptography is important but more specialist than general secure development.",
            ),
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
        tag_relationships=(
            SkillTagRelationship(
                tag="algorithms",
                relationship_weight=1.0,
                tag_confidence=1.0,
                rationale="Directly supports algorithmic reasoning and implementation trade-offs.",
            ),
            SkillTagRelationship(
                tag="data-structures",
                relationship_weight=0.9,
                tag_confidence=1.0,
                rationale="Data structures are a practical foundation for efficient software implementation.",
            ),
            SkillTagRelationship(
                tag="theory-of-computing",
                relationship_weight=0.55,
                tag_confidence=0.85,
                rationale="Theory supports reasoning, but is less direct for most applied software roles.",
            ),
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

DATA_SCIENTIST_SKILL_MAPPINGS = (
    CareerSkillMapping(
        skill="data modelling and analytics",
        tag_relationships=(
            SkillTagRelationship(
                tag="data-science",
                relationship_weight=1.0,
                tag_confidence=1.0,
                rationale="Directly represents extracting insight from data using analytical methods.",
            ),
            SkillTagRelationship(
                tag="database",
                relationship_weight=0.85,
                tag_confidence=1.0,
                rationale="Data storage, querying, and modelling are core foundations for analytics work.",
            ),
            SkillTagRelationship(
                tag="data-visualisation",
                relationship_weight=0.8,
                tag_confidence=1.0,
                rationale="Visualisation helps communicate data insights to stakeholders.",
            ),
            SkillTagRelationship(
                tag="information-retrieval",
                relationship_weight=0.65,
                tag_confidence=0.9,
                rationale="Retrieval methods are useful for text-heavy and search-oriented data products.",
            ),
            SkillTagRelationship(
                tag="privacy",
                relationship_weight=0.45,
                tag_confidence=0.8,
                rationale="Privacy supports responsible handling of user data and analytics governance.",
            ),
        ),
        weight=10,
        rationale=(
            "Data scientists need to collect, model, query, analyse, and communicate "
            "data so that technical results become useful decisions."
        ),
        weight_rationale="Highest weight because this is the central skill area for Data Scientist roles.",
    ),
    CareerSkillMapping(
        skill="machine learning and statistical reasoning",
        tag_relationships=(
            SkillTagRelationship(
                tag="ai-ml",
                relationship_weight=1.0,
                tag_confidence=1.0,
                rationale="Directly supports model training, evaluation, and applied machine learning work.",
            ),
            SkillTagRelationship(
                tag="math-foundation",
                relationship_weight=0.8,
                tag_confidence=0.9,
                rationale="Mathematical foundations support statistical reasoning and model understanding.",
            ),
            SkillTagRelationship(
                tag="algorithms",
                relationship_weight=0.7,
                tag_confidence=0.9,
                rationale="Algorithmic reasoning helps with model implementation and efficiency trade-offs.",
            ),
            SkillTagRelationship(
                tag="data-structures",
                relationship_weight=0.55,
                tag_confidence=0.85,
                rationale="Data structures support efficient data processing and model implementation.",
            ),
            SkillTagRelationship(
                tag="natural-language-processing",
                relationship_weight=0.65,
                tag_confidence=0.9,
                rationale="NLP is a specialised applied machine learning area for text data.",
            ),
            SkillTagRelationship(
                tag="computer-vision",
                relationship_weight=0.65,
                tag_confidence=0.9,
                rationale="Computer vision is a specialised applied machine learning area for image data.",
            ),
        ),
        weight=9,
        rationale=(
            "Machine learning and statistical reasoning help data scientists build, "
            "evaluate, and explain predictive models."
        ),
        weight_rationale="Very high weight because modelling is a major Data Scientist responsibility.",
    ),
    CareerSkillMapping(
        skill="data systems and scalable processing",
        tag_relationships=(
            SkillTagRelationship(
                tag="distributed-systems",
                relationship_weight=0.85,
                tag_confidence=0.9,
                rationale="Distributed systems support large-scale data processing and reliable pipelines.",
            ),
            SkillTagRelationship(
                tag="cloud-computing",
                relationship_weight=0.75,
                tag_confidence=0.9,
                rationale="Cloud platforms often host data workflows, storage, and model services.",
            ),
            SkillTagRelationship(
                tag="parallel-computing",
                relationship_weight=0.7,
                tag_confidence=0.85,
                rationale="Parallel computing is useful for performance-heavy analytics workloads.",
            ),
            SkillTagRelationship(
                tag="programming",
                relationship_weight=0.65,
                tag_confidence=0.85,
                rationale="Programming is needed to implement data workflows, but it is broader than data science.",
            ),
        ),
        weight=6,
        rationale=(
            "Data scientists benefit from understanding the systems that store, "
            "process, and serve data at practical scale."
        ),
        weight_rationale="Medium weight because systems depth is useful but not always the primary role focus.",
    ),
)

CYBERSECURITY_ANALYST_SKILL_MAPPINGS = (
    CareerSkillMapping(
        skill="security analysis and defence",
        tag_relationships=(
            SkillTagRelationship(
                tag="computer-security",
                relationship_weight=1.0,
                tag_confidence=1.0,
                rationale="Directly represents security concepts, threats, and defensive practice.",
            ),
            SkillTagRelationship(
                tag="digital-forensics",
                relationship_weight=0.85,
                tag_confidence=1.0,
                rationale="Forensics supports investigation, incident response, and evidence analysis.",
            ),
            SkillTagRelationship(
                tag="malware-analysis",
                relationship_weight=0.85,
                tag_confidence=1.0,
                rationale="Malware analysis is a specialised but direct security-analysis skill.",
            ),
            SkillTagRelationship(
                tag="privacy",
                relationship_weight=0.7,
                tag_confidence=0.9,
                rationale="Privacy knowledge supports responsible handling of sensitive systems and data.",
            ),
        ),
        weight=10,
        rationale=(
            "Cybersecurity analysts need to identify risks, investigate incidents, "
            "and reason about defensive controls."
        ),
        weight_rationale="Highest weight because direct security analysis is central to the role.",
    ),
    CareerSkillMapping(
        skill="networks and systems security",
        tag_relationships=(
            SkillTagRelationship(
                tag="computer-network",
                relationship_weight=1.0,
                tag_confidence=1.0,
                rationale="Network knowledge is essential for analysing attacks, traffic, and defences.",
            ),
            SkillTagRelationship(
                tag="operating-systems",
                relationship_weight=0.9,
                tag_confidence=1.0,
                rationale="Operating-system knowledge supports endpoint security and incident analysis.",
            ),
            SkillTagRelationship(
                tag="distributed-systems",
                relationship_weight=0.7,
                tag_confidence=0.85,
                rationale="Distributed systems knowledge helps analyse complex service architectures.",
            ),
            SkillTagRelationship(
                tag="cloud-computing",
                relationship_weight=0.65,
                tag_confidence=0.85,
                rationale="Cloud concepts are useful as security work increasingly covers cloud-hosted systems.",
            ),
        ),
        weight=8,
        rationale=(
            "Security analysts often investigate networked systems, endpoints, "
            "cloud services, and distributed applications."
        ),
        weight_rationale="High weight because systems and network foundations make security analysis practical.",
    ),
    CareerSkillMapping(
        skill="cryptography and secure implementation",
        tag_relationships=(
            SkillTagRelationship(
                tag="cryptography",
                relationship_weight=1.0,
                tag_confidence=1.0,
                rationale="Cryptography directly supports secure protocols and data protection.",
            ),
            SkillTagRelationship(
                tag="software-engineering",
                relationship_weight=0.55,
                tag_confidence=0.85,
                rationale="Secure implementation depends on understanding how software is designed and maintained.",
            ),
            SkillTagRelationship(
                tag="programming",
                relationship_weight=0.45,
                tag_confidence=0.85,
                rationale="Programming supports practical security tooling and code-level analysis.",
            ),
        ),
        weight=6,
        rationale=(
            "Cybersecurity analysts benefit from understanding cryptography and "
            "secure implementation, especially when reviewing software or protocols."
        ),
        weight_rationale="Medium weight because it is valuable, but more specialised than general security analysis.",
    ),
)

CAREER_SKILL_MAPPINGS = {
    "software-engineer": SOFTWARE_ENGINEER_SKILL_MAPPINGS,
    "data-scientist": DATA_SCIENTIST_SKILL_MAPPINGS,
    "cybersecurity-analyst": CYBERSECURITY_ANALYST_SKILL_MAPPINGS,
}
