from pydantic import BaseModel, ConfigDict

class CurriculumCourse(BaseModel):
    id: str
    courseCode: str
    title: str
    type: str
    year: int
    semester: int
    academicUnits: int
    prerequisites: list[str]
    prerequisiteText: str
    isChoiceSlot: bool

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "id": "y1s1-sc1003-1",
                "courseCode": "SC1003",
                "title": "Introduction to Computational Thinking and Programming",
                "type": "Core",
                "year": 1,
                "semester": 1,
                "academicUnits": 3,
                "prerequisites": [],
                "prerequisiteText": "Nil",
                "isChoiceSlot": False,
            }
        }
    )

class CurriculumSemester(BaseModel):
    year: int
    semester: int
    totalAcademicUnits: int
    courses: list[CurriculumCourse]

class CurriculumEdge(BaseModel):
    source: str
    target: str

class CurriculumGuideResponse(BaseModel):
    major: str
    cohort: str
    totalAcademicUnits: int
    semesters: list[CurriculumSemester]
    nodes: list[CurriculumCourse]
    edges: list[CurriculumEdge]

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "major": "Computer Science",
                "cohort": "AY2023-24",
                "totalAcademicUnits": 135,
                "semesters": [
                    {
                        "year": 1,
                        "semester": 1,
                        "totalAcademicUnits": 19,
                        "courses": [],
                    }
                ],
                "nodes": [],
                "edges": [],
            }
        }
    )
