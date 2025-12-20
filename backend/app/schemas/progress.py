"""Pydantic schemas for user progress on labs."""
from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class ProgressCreate(BaseModel):
    """Payload for creating or updating a progress entry."""

    lab_id: int
    doc_url: Optional[str] = None


class ProgressRead(BaseModel):
    """Detailed view of a user's progress on a lab."""

    id: int
    user_id: int
    lab_id: int
    estado: str  # PENDIENTE | COMPLETADO
    doc_url: Optional[str] = None
    xp_obtenido: int
    completed_at: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
