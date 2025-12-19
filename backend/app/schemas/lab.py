"""Pydantic schemas describing labs."""
from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class LabBase(BaseModel):
    """Editable fields for creating or updating a lab."""

    codigo: str
    titulo: str
    nivel_dificultad: str  # BEGINNER | INTERMEDIATE | ADVANCED
    xp_otorgado: int
    estado_inicial: str  # DISPONIBLE | BLOQUEADO
    historia: str
    objetivo: str
    reglas: str
    entregable_descripcion: str
    orden_desbloqueo: int


class LabRead(LabBase):
    """Full lab data returned to the frontend."""

    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


class LabSummary(BaseModel):
    """Lightweight view for listing labs with user-specific state."""

    id: int
    titulo: str
    nivel_dificultad: str
    xp_otorgado: int
    estado: Optional[str] = None  # State for the requesting user (e.g., DISPONIBLE/BLOQUEADO)

    class Config:
        orm_mode = True
