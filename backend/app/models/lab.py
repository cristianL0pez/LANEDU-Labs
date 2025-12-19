"""SQLAlchemy model representing a lab or challenge."""
from datetime import datetime
from enum import Enum

from sqlalchemy import CheckConstraint, Column, DateTime, Enum as PgEnum, Integer, String, Text, func
from sqlalchemy.orm import relationship

from app.db.base import Base


class DifficultyLevel(str, Enum):
    """Allowed difficulty levels for labs."""

    BEGINNER = "BEGINNER"
    INTERMEDIATE = "INTERMEDIATE"
    ADVANCED = "ADVANCED"


class LabInitialState(str, Enum):
    """Initial availability state for a lab."""

    DISPONIBLE = "DISPONIBLE"
    BLOQUEADO = "BLOQUEADO"


class Lab(Base):
    """Represents a hands-on lab experience in the platform."""

    __tablename__ = "labs"
    __table_args__ = (
        CheckConstraint("xp_otorgado >= 0", name="ck_labs_xp_otorgado_non_negative"),
        CheckConstraint("orden_desbloqueo >= 0", name="ck_labs_orden_desbloqueo_non_negative"),
    )

    id = Column(Integer, primary_key=True, index=True)
    codigo = Column(String(50), unique=True, nullable=False, index=True)
    titulo = Column(String(255), nullable=False)
    nivel_dificultad = Column(PgEnum(DifficultyLevel, name="difficulty_level"), nullable=False)
    xp_otorgado = Column(Integer, nullable=False)
    estado_inicial = Column(PgEnum(LabInitialState, name="lab_initial_state"), nullable=False)
    historia = Column(Text, nullable=False)
    objetivo = Column(Text, nullable=False)
    reglas = Column(Text, nullable=False)
    entregable_descripcion = Column(Text, nullable=False)
    orden_desbloqueo = Column(Integer, nullable=False, default=0, server_default="0")
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False
    )

    # Relationship to show which users have progress records for this lab.
    user_progress = relationship(
        "UserLabProgress",
        back_populates="lab",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )

    def __repr__(self) -> str:
        return f"<Lab id={self.id} codigo={self.codigo!r}>"
