"""Progress endpoints."""
from fastapi import APIRouter, Depends, HTTPException

from app.schemas.progress import ProgressCreate, ProgressRead
from app.services.progress_service import complete_lab
from app.db.session import get_db

router = APIRouter(prefix="/progress", tags=["progress"])


def get_current_user_id() -> int:
    """
    Fake auth dependency.
    TODO: Replace with real authentication that returns the authenticated user's ID.
    """
    return 1


@router.post("/complete", response_model=ProgressRead, summary="Completar un lab")
def complete(progress_in: ProgressCreate, db=Depends(get_db), current_user_id: int = Depends(get_current_user_id)):
    """Mark a lab as completed for the current user."""
    try:
        return complete_lab(db, current_user_id, progress_in.lab_id, progress_in.doc_url)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
