from typing import Optional

from sqlalchemy.orm import Session

from backend.models import ModuleModel
from backend.schemas.curriculum import CurriculumCourse, CurriculumGuideResponse
from backend.schemas.roadmap import CourseNode, RoadmapEdge, RoadmapResponse
from backend.schemas.transcript import TranscriptCourse
from backend.services.module_service import get_prerequisites_by_module, get_unlocks_by_module
from backend.services.transcript_matching_service import (
    get_course_title_signature,
    normalize_course_title,
)

def build_personalized_roadmap(
    db: Session,
    curriculum_guide: CurriculumGuideResponse,
    transcript_completed_courses: list[TranscriptCourse],
    transcript_unmatched_course_codes: list[str],
) -> RoadmapResponse:
    transcript_placement_by_course_key = get_transcript_placement_by_course_key(
        transcript_completed_courses,
    )
    curriculum_nodes = [
        build_curriculum_node(course, curriculum_guide, transcript_placement_by_course_key)
        for course in curriculum_guide.nodes
    ]
    transcript_nodes, transcript_edges = build_transcript_only_roadmap_items(
        db,
        transcript_completed_courses,
        transcript_unmatched_course_codes,
        curriculum_nodes,
    )
    nodes = [*transcript_nodes, *curriculum_nodes]
    curriculum_edges = [
        RoadmapEdge(source=edge.source, target=edge.target)
        for edge in curriculum_guide.edges
    ]
    edges = deduplicate_edges([*curriculum_edges, *transcript_edges])
    prerequisites_by_target = get_prerequisites_by_target(edges)
    nodes_with_updated_prerequisites = [
        node.model_copy(update={"prerequisites": prerequisites_by_target.get(node.id, [])})
        for node in nodes
    ]

    return RoadmapResponse(nodes=nodes_with_updated_prerequisites, edges=edges)

def build_curriculum_node(
    course: CurriculumCourse,
    curriculum_guide: CurriculumGuideResponse,
    transcript_placement_by_course_key: dict[str, tuple[int, int]],
) -> CourseNode:
    transcript_placement = get_transcript_placement_for_curriculum_course(
        course,
        transcript_placement_by_course_key,
    )
    year = transcript_placement[0] if transcript_placement else course.year
    semester = transcript_placement[1] if transcript_placement else course.semester

    return CourseNode(
        id=course.id,
        courseCode=course.courseCode,
        title=get_curriculum_course_title(course),
        type=course.type,
        year=year,
        semester=semester,
        academicUnits=course.academicUnits,
        prerequisites=[
            edge.source
            for edge in curriculum_guide.edges
            if edge.target == course.id
        ],
        prerequisiteText=course.prerequisiteText,
        isCompleted=False,
        isChoiceSlot=course.isChoiceSlot,
        isTranscriptOnly=False,
        jobSkills=[],
    )

def build_transcript_only_roadmap_items(
    db: Session,
    transcript_completed_courses: list[TranscriptCourse],
    transcript_unmatched_course_codes: list[str],
    curriculum_nodes: list[CourseNode],
) -> tuple[list[CourseNode], list[RoadmapEdge]]:
    transcript_courses_by_code = {
        course.course_code: course
        for course in transcript_completed_courses
    }
    modules_by_code, prerequisites_by_module, unlocks_by_module = get_modules_by_code(
        db,
        transcript_unmatched_course_codes,
    )
    transcript_nodes = [
        build_transcript_node(
            transcript_courses_by_code.get(course_code),
            modules_by_code.get(course_code),
            prerequisites_by_module.get(course_code, []),
            course_code,
        )
        for course_code in transcript_unmatched_course_codes
    ]
    node_ids_by_course_code = get_node_ids_by_course_code([*transcript_nodes, *curriculum_nodes])
    transcript_edges = build_transcript_edges(
        transcript_nodes,
        prerequisites_by_module,
        unlocks_by_module,
        node_ids_by_course_code,
    )

    return transcript_nodes, transcript_edges

def build_transcript_node(
    transcript_course: Optional[TranscriptCourse],
    module: Optional[ModuleModel],
    prerequisites: list[str],
    course_code: str,
) -> CourseNode:
    return CourseNode(
        id=f"transcript-{course_code.lower()}",
        courseCode=course_code,
        title=get_transcript_node_title(transcript_course, module),
        type="Transcript",
        year=transcript_course.study_year if transcript_course and transcript_course.study_year else 0,
        semester=(
            transcript_course.transcript_semester
            if transcript_course and transcript_course.transcript_semester
            else 0
        ),
        academicUnits=get_transcript_node_au(transcript_course, module),
        prerequisites=[],
        prerequisiteText=", ".join(prerequisites),
        isCompleted=True,
        isChoiceSlot=False,
        isTranscriptOnly=True,
        jobSkills=[],
    )

def build_transcript_edges(
    transcript_nodes: list[CourseNode],
    prerequisites_by_module: dict[str, list[str]],
    unlocks_by_module: dict[str, list[str]],
    node_ids_by_course_code: dict[str, list[str]],
) -> list[RoadmapEdge]:
    edges = []

    for node in transcript_nodes:
        prerequisite_edges = [
            RoadmapEdge(source=prerequisite_node_id, target=node.id)
            for prerequisite_code in prerequisites_by_module.get(node.courseCode, [])
            for prerequisite_node_id in node_ids_by_course_code.get(prerequisite_code.upper(), [])
        ]
        unlock_edges = [
            RoadmapEdge(source=node.id, target=unlock_node_id)
            for unlock_code in unlocks_by_module.get(node.courseCode, [])
            for unlock_node_id in node_ids_by_course_code.get(unlock_code.upper(), [])
        ]
        edges.extend([*prerequisite_edges, *unlock_edges])

    return edges

def get_modules_by_code(
    db: Session,
    course_codes: list[str],
) -> tuple[dict[str, ModuleModel], dict[str, list[str]], dict[str, list[str]]]:
    if not course_codes:
        return {}, {}, {}

    modules = db.query(ModuleModel).filter(ModuleModel.code.in_(course_codes)).all()
    module_codes = [module.code for module in modules]
    prerequisites_by_module = get_prerequisites_by_module(db, module_codes)
    unlocks_by_module = get_unlocks_by_module(db, module_codes)

    return {module.code: module for module in modules}, prerequisites_by_module, unlocks_by_module

def get_curriculum_course_title(course: CurriculumCourse) -> str:
    if course.courseCode == "BDE" or course.type == "BDE":
        return "Broadening and Deepening Electives"

    if course.isChoiceSlot and "xxx" in course.courseCode and "MPE" in course.type:
        return "Major Prescribed Elective"

    return course.title

def get_transcript_node_title(
    transcript_course: Optional[TranscriptCourse],
    module: Optional[ModuleModel],
) -> str:
    if module:
        return module.title

    if transcript_course and transcript_course.title:
        return transcript_course.title

    return "Completed transcript module"

def get_transcript_node_au(
    transcript_course: Optional[TranscriptCourse],
    module: Optional[ModuleModel],
) -> float:
    if module and module.au is not None:
        return module.au

    if transcript_course:
        return transcript_course.academic_units

    return 0

def get_transcript_placement_by_course_key(
    transcript_courses: list[TranscriptCourse],
) -> dict[str, tuple[int, int]]:
    placements: dict[str, tuple[int, int]] = {}

    for course in transcript_courses:
        if not course.study_year or not course.transcript_semester:
            continue

        placement = (course.study_year, course.transcript_semester)

        for key in get_course_matching_keys(course.course_code, course.title):
            placements[key] = placement

    return placements

def get_transcript_placement_for_curriculum_course(
    course: CurriculumCourse,
    transcript_placement_by_course_key: dict[str, tuple[int, int]],
) -> Optional[tuple[int, int]]:
    return next(
        (
            transcript_placement_by_course_key[key]
            for key in get_course_matching_keys(course.courseCode, course.title)
            if key in transcript_placement_by_course_key
        ),
        None,
    )

def get_course_matching_keys(course_code: str, title: str) -> list[str]:
    return [
        key
        for key in [
            course_code.upper(),
            normalize_course_title(title),
            get_course_title_signature(title),
        ]
        if key
    ]

def get_node_ids_by_course_code(nodes: list[CourseNode]) -> dict[str, list[str]]:
    node_ids_by_course_code: dict[str, list[str]] = {}

    for node in nodes:
        course_code = node.courseCode.upper()
        node_ids_by_course_code.setdefault(course_code, []).append(node.id)

    return node_ids_by_course_code

def get_prerequisites_by_target(edges: list[RoadmapEdge]) -> dict[str, list[str]]:
    prerequisites_by_target: dict[str, list[str]] = {}

    for edge in edges:
        prerequisites_by_target.setdefault(edge.target, []).append(edge.source)

    return prerequisites_by_target

def deduplicate_edges(edges: list[RoadmapEdge]) -> list[RoadmapEdge]:
    edge_keys = set()
    deduplicated_edges = []

    for edge in edges:
        edge_key = f"{edge.source}->{edge.target}"

        if edge_key not in edge_keys:
            deduplicated_edges.append(edge)
            edge_keys.add(edge_key)

    return deduplicated_edges
