"""SQLAlchemy model tracking a user's progress through labs."""
from datetime import datetime
from enum import Enum

from sqlalchemy import (
    Column,
    DateTime,
    Enum as PgEnum,
    ForeignKey,
    Integer,
    String,
    func,
)
from sqlalchemy.orm import relationship

from app.db.base_class import Base


class ProgressState(str, Enum):
    """Allowed states for lab completion tracking."""

    PENDIENTE = "PENDIENTE"
    COMPLETADO = "COMPLETADO"


class UserLabProgress(Base):
    """Associative table linking users to labs and tracking completion state."""

    __tablename__ = "user_lab_progress"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    lab_id = Column(Integer, ForeignKey("labs.id", ondelete="CASCADE"), nullable=False, index=True)
    estado = Column(
        PgEnum(ProgressState, name="progress_state", create_type=False), nullable=False
    )
    doc_url = Column(String(500), nullable=True)
    xp_obtenido = Column(Integer, nullable=False, default=0, server_default="0")
    completed_at = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False
    )

    user = relationship("User", back_populates="lab_progress")
    lab = relationship("Lab", back_populates="user_progress")

    def __repr__(self) -> str:
        return f"<UserLabProgress id={self.id} user_id={self.user_id} lab_id={self.lab_id}>"
