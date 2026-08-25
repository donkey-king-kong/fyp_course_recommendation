from __future__ import annotations

from sqlalchemy import Boolean, String
from sqlalchemy.orm import Mapped, mapped_column

from backend.database.connection import Base

# Stores whether a faculty should appear in the module catalogue.
class FacultyModel(Base):
    __tablename__ = "faculties"

    name: Mapped[str] = mapped_column(String(100), primary_key=True, index=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False, index=True)
