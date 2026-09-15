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

AI_ML_ENGINEER_SKILL_MAPPINGS = (
    CareerSkillMapping(
        skill="machine learning systems",
        tag_relationships=(
            SkillTagRelationship(
                tag="ai-ml",
                relationship_weight=1.0,
                tag_confidence=1.0,
                rationale="Directly represents applied machine learning and model-building work.",
            ),
            SkillTagRelationship(
                tag="natural-language-processing",
                relationship_weight=0.9,
                tag_confidence=1.0,
                rationale="NLP is a major applied AI engineering area for text and language products.",
            ),
            SkillTagRelationship(
                tag="computer-vision",
                relationship_weight=0.9,
                tag_confidence=1.0,
                rationale="Computer vision is a major applied AI engineering area for image and video systems.",
            ),
        ),
        weight=10,
        rationale=(
            "AI and machine learning engineers build model-driven systems, including "
            "NLP, vision, generative AI, and applied ML products."
        ),
        weight_rationale="Highest weight because model-building is central to this career goal.",
    ),
    CareerSkillMapping(
        skill="model implementation foundations",
        tag_relationships=(
            SkillTagRelationship(
                tag="algorithms",
                relationship_weight=0.85,
                tag_confidence=1.0,
                rationale="Algorithms support efficient model implementation and optimisation reasoning.",
            ),
            SkillTagRelationship(
                tag="data-structures",
                relationship_weight=0.75,
                tag_confidence=1.0,
                rationale="Data structures support efficient data and model-processing pipelines.",
            ),
            SkillTagRelationship(
                tag="math-foundation",
                relationship_weight=0.8,
                tag_confidence=0.9,
                rationale="Mathematical foundations support understanding model behaviour and trade-offs.",
            ),
            SkillTagRelationship(
                tag="programming",
                relationship_weight=0.7,
                tag_confidence=0.9,
                rationale="Programming skill is needed to implement and deploy AI systems.",
            ),
        ),
        weight=7,
        rationale=(
            "AI engineering still depends on strong programming, algorithmic, and "
            "mathematical foundations."
        ),
        weight_rationale="High weight because foundations make specialised AI modules more practical.",
    ),
    CareerSkillMapping(
        skill="scalable AI infrastructure",
        tag_relationships=(
            SkillTagRelationship(
                tag="parallel-computing",
                relationship_weight=0.85,
                tag_confidence=0.9,
                rationale="Parallel computing supports training and serving compute-heavy AI workloads.",
            ),
            SkillTagRelationship(
                tag="cloud-computing",
                relationship_weight=0.75,
                tag_confidence=0.9,
                rationale="Cloud platforms are common deployment environments for AI services.",
            ),
            SkillTagRelationship(
                tag="distributed-systems",
                relationship_weight=0.7,
                tag_confidence=0.9,
                rationale="Distributed systems support scalable data processing and model-serving systems.",
            ),
        ),
        weight=5,
        rationale=(
            "Production AI work often needs scalable compute, data, and deployment infrastructure."
        ),
        weight_rationale="Medium weight because infrastructure matters, but it is not the primary role focus.",
    ),
)

DATA_ENGINEER_SKILL_MAPPINGS = (
    CareerSkillMapping(
        skill="data storage and modelling",
        tag_relationships=(
            SkillTagRelationship(
                tag="database",
                relationship_weight=1.0,
                tag_confidence=1.0,
                rationale="Databases are the core storage and modelling foundation for data engineering.",
            ),
            SkillTagRelationship(
                tag="data-science",
                relationship_weight=0.75,
                tag_confidence=0.9,
                rationale="Data-science modules help connect pipelines to downstream analytics needs.",
            ),
            SkillTagRelationship(
                tag="information-retrieval",
                relationship_weight=0.65,
                tag_confidence=0.85,
                rationale="Retrieval knowledge is useful for search and text-heavy data systems.",
            ),
        ),
        weight=10,
        rationale=(
            "Data engineers design storage models, pipelines, and systems that make data usable."
        ),
        weight_rationale="Highest weight because storage and data modelling are central to the role.",
    ),
    CareerSkillMapping(
        skill="distributed data platforms",
        tag_relationships=(
            SkillTagRelationship(
                tag="distributed-systems",
                relationship_weight=1.0,
                tag_confidence=1.0,
                rationale="Distributed systems directly support scalable data pipelines and platforms.",
            ),
            SkillTagRelationship(
                tag="cloud-computing",
                relationship_weight=0.95,
                tag_confidence=1.0,
                rationale="Cloud platforms commonly host storage, processing, and orchestration workflows.",
            ),
            SkillTagRelationship(
                tag="parallel-computing",
                relationship_weight=0.8,
                tag_confidence=0.9,
                rationale="Parallel computing supports batch and performance-heavy data processing.",
            ),
            SkillTagRelationship(
                tag="computer-network",
                relationship_weight=0.55,
                tag_confidence=0.85,
                rationale="Networking foundations help with distributed services and data movement.",
            ),
        ),
        weight=9,
        rationale=(
            "Modern data platforms usually run across distributed, cloud, and parallel systems."
        ),
        weight_rationale="Very high weight because scalable infrastructure separates data engineering from data science.",
    ),
    CareerSkillMapping(
        skill="software implementation for pipelines",
        tag_relationships=(
            SkillTagRelationship(
                tag="backend-engineering",
                relationship_weight=0.8,
                tag_confidence=1.0,
                rationale="Data platforms often expose APIs and backend services.",
            ),
            SkillTagRelationship(
                tag="software-engineering",
                relationship_weight=0.7,
                tag_confidence=1.0,
                rationale="Reliable data pipelines require software design, testing, and maintainability.",
            ),
            SkillTagRelationship(
                tag="programming",
                relationship_weight=0.65,
                tag_confidence=0.9,
                rationale="Programming is necessary for implementation, but is broader than data engineering.",
            ),
        ),
        weight=6,
        rationale="Data engineers need enough software practice to build reliable production pipelines.",
        weight_rationale="Medium weight because implementation matters, but data systems should dominate.",
    ),
)

CLOUD_PLATFORM_ENGINEER_SKILL_MAPPINGS = (
    CareerSkillMapping(
        skill="cloud and distributed infrastructure",
        tag_relationships=(
            SkillTagRelationship(
                tag="cloud-computing",
                relationship_weight=1.0,
                tag_confidence=1.0,
                rationale="Directly represents cloud infrastructure and platform concepts.",
            ),
            SkillTagRelationship(
                tag="distributed-systems",
                relationship_weight=0.95,
                tag_confidence=1.0,
                rationale="Distributed systems are foundational for scalable cloud platforms.",
            ),
            SkillTagRelationship(
                tag="computer-network",
                relationship_weight=0.75,
                tag_confidence=1.0,
                rationale="Networking supports deployment, routing, communication, and reliability.",
            ),
        ),
        weight=10,
        rationale=(
            "Cloud and platform engineers build infrastructure for scalable, networked services."
        ),
        weight_rationale="Highest weight because infrastructure and distributed platforms define this role.",
    ),
    CareerSkillMapping(
        skill="systems performance and reliability",
        tag_relationships=(
            SkillTagRelationship(
                tag="operating-systems",
                relationship_weight=0.9,
                tag_confidence=1.0,
                rationale="Operating systems support runtime, resource, and performance understanding.",
            ),
            SkillTagRelationship(
                tag="parallel-computing",
                relationship_weight=0.8,
                tag_confidence=0.9,
                rationale="Parallel computing supports performance-aware infrastructure work.",
            ),
            SkillTagRelationship(
                tag="computer-architecture",
                relationship_weight=0.7,
                tag_confidence=0.85,
                rationale="Architecture knowledge helps reason about performance and hardware constraints.",
            ),
        ),
        weight=7,
        rationale="Platform work benefits from understanding lower-level systems and performance trade-offs.",
        weight_rationale="High weight because systems knowledge supports reliable infrastructure decisions.",
    ),
    CareerSkillMapping(
        skill="secure platform operation",
        tag_relationships=(
            SkillTagRelationship(
                tag="computer-security",
                relationship_weight=0.7,
                tag_confidence=0.9,
                rationale="Platform engineers need to understand security risks in deployed systems.",
            ),
            SkillTagRelationship(
                tag="privacy",
                relationship_weight=0.5,
                tag_confidence=0.8,
                rationale="Privacy is useful when platforms handle user or operational data.",
            ),
        ),
        weight=5,
        rationale="Cloud platforms need secure operation, but security is secondary to platform fundamentals.",
        weight_rationale="Medium weight because security supports the role without replacing infrastructure depth.",
    ),
)

CYBERSECURITY_ENGINEER_SKILL_MAPPINGS = (
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
            "Cybersecurity engineers need to identify risks, investigate incidents, "
            "build defensive controls, and reason about secure systems."
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
            "Cybersecurity engineers often investigate networked systems, endpoints, "
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
            "Cybersecurity engineers benefit from understanding cryptography and "
            "secure implementation, especially when reviewing software or protocols."
        ),
        weight_rationale="Medium weight because it is valuable, but more specialised than general security analysis.",
    ),
)

CAREER_SKILL_MAPPINGS = {
    "software-engineer": SOFTWARE_ENGINEER_SKILL_MAPPINGS,
    "data-scientist": DATA_SCIENTIST_SKILL_MAPPINGS,
    "cybersecurity-engineer": CYBERSECURITY_ENGINEER_SKILL_MAPPINGS,
    "ai-ml-engineer": AI_ML_ENGINEER_SKILL_MAPPINGS,
    "data-engineer": DATA_ENGINEER_SKILL_MAPPINGS,
    "cloud-platform-engineer": CLOUD_PLATFORM_ENGINEER_SKILL_MAPPINGS,
}
