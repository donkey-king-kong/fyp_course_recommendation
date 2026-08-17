from pydantic import BaseModel

class CourseNode(BaseModel):
    id: str
    courseCode: str
    title: str
    type: str
    year: int
    semester: int
    academicUnits: int
    prerequisites: list[str]
    isCompleted: bool
    jobSkills: list[str]

class RoadmapEdge(BaseModel):
    source: str
    target: str

class RoadmapResponse(BaseModel):
    nodes: list[CourseNode]
    edges: list[RoadmapEdge]
