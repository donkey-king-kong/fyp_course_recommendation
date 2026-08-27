from backend.database.connection import Base
from backend.models.faculty import FacultyModel
from backend.models.module import ModuleModel
from backend.models.module_prerequisite import ModulePrerequisiteModel

__all__ = ["Base", "FacultyModel", "ModuleModel", "ModulePrerequisiteModel"]
