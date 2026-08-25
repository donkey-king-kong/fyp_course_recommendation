from __future__ import annotations

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from backend.database.connection import Base

# One row means module_code requires prerequisite_code.
# Unlocks are derived by querying this table in reverse.
class ModulePrerequisiteModel(Base):
    __tablename__ = "module_prerequisites"

    module_code: Mapped[str] = mapped_column(String(20), primary_key=True, index=True)
    prerequisite_code: Mapped[str] = mapped_column(String(20), primary_key=True, index=True)
