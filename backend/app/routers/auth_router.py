"""Authentication endpoints (MVP placeholder)."""
from fastapi import APIRouter, Depends, HTTPException

from app.schemas.user import UserCreate, UserRead
from app.services.user_service import create_user, get_user_by_username
from app.db.session import get_db

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=UserRead, summary="Registro de usuario (MVP)")
def register(user_in: UserCreate, db=Depends(get_db)):
    """Register a new user. In MVP we just check username uniqueness."""
    existing = get_user_by_username(db, user_in.username)
    if existing:
        raise HTTPException(status_code=400, detail="El usuario ya existe")
    return create_user(db, user_in)


@router.post("/login", summary="Login simple por username (token simulado)")
def login(username: str, db=Depends(get_db)):
    """
    MVP login without password.
    TODO: Replace with real authentication (password hashing + JWT/OAuth2).
    """
    user = get_user_by_username(db, username)
    if not user:
        raise HTTPException(status_code=400, detail="Usuario no encontrado")
    # Simulated token: in production, return a signed JWT.
    return {"access_token": f"fake-token-for-{user.username}", "token_type": "bearer"}
