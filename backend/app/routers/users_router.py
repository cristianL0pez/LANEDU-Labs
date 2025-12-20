"""User endpoints (uses fake auth dependency for now)."""
from fastapi import APIRouter, Depends, HTTPException

from app.schemas.ranking import UserProfileResponse
from app.services.user_service import get_user_profile
from app.db.session import get_db

router = APIRouter(prefix="/users", tags=["users"])


def get_current_user_id() -> int:
    """
    Fake auth dependency.
    TODO: Replace with real authentication that returns the authenticated user's ID.
    """
    return 1  # For now assume a fixed user id.


@router.get("/me", response_model=UserProfileResponse, summary="Perfil del usuario autenticado")
def read_profile(db=Depends(get_db), current_user_id: int = Depends(get_current_user_id)):
    """Return the profile for the authenticated user."""
    profile = get_user_profile(db, current_user_id)
    if not profile:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return profile
