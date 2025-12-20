"""Lab endpoints."""
from fastapi import APIRouter, Depends, HTTPException

from app.schemas.lab import LabRead, LabSummary
from app.services.lab_service import get_lab, list_labs_for_user
from app.db.session import get_db

router = APIRouter(prefix="/labs", tags=["labs"])


def get_current_user_id() -> int:
    """
    Fake auth dependency.
    TODO: Replace with real authentication that returns the authenticated user's ID.
    """
    return 1


@router.get("", response_model=list[LabSummary], summary="Listar labs con estado para el usuario")
def list_labs(db=Depends(get_db), current_user_id: int = Depends(get_current_user_id)):
    """Return all labs with user-specific state (progress-aware)."""
    return list_labs_for_user(db, current_user_id)


@router.get("/{lab_id}", response_model=LabRead, summary="Detalle de un lab")
def read_lab(lab_id: int, db=Depends(get_db)):
    """Return lab details by id."""
    lab = get_lab(db, lab_id)
    if not lab:
        raise HTTPException(status_code=404, detail="Lab no encontrado")
    return lab
