from __future__ import annotations

from typing import Optional

from sqlalchemy import Boolean, Float, Integer, JSON, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from backend.database.connection import Base

# SQLAlchemy model for one row in the PostgreSQL modules table.
class ModuleModel(Base):
    __tablename__ = "modules"

    code: Mapped[str] = mapped_column(String(20), primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    au: Mapped[Optional[float]] = mapped_column(Float)
    faculty: Mapped[Optional[str]] = mapped_column(String(100), index=True)
    description: Mapped[Optional[str]] = mapped_column(Text)
    level: Mapped[Optional[int]] = mapped_column(Integer, index=True)
    categories: Mapped[list[str]] = mapped_column(JSON, default=list)
    recommendation_tags: Mapped[list[str]] = mapped_column(JSON, default=list)
    latest_year: Mapped[Optional[str]] = mapped_column(String(10), index=True)
    latest_semester: Mapped[Optional[str]] = mapped_column(String(10), index=True)
    is_current_semester: Mapped[bool] = mapped_column(Boolean, default=False, index=True)
    not_available_to_programme: Mapped[Optional[str]] = mapped_column(Text)
