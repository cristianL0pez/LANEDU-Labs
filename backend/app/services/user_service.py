"""Service layer for user operations."""
from sqlalchemy.orm import Session

from app.models.user import User
from app.models.user_lab_progress import ProgressState, UserLabProgress
from app.schemas.user import UserCreate


def create_user(db: Session, user_create: UserCreate) -> User:
    """Create a new user with initial XP and level defaults."""
    user = User(username=user_create.username, email=user_create.email)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def get_user_by_username(db: Session, username: str) -> User | None:
    """Return a user by username, or None if not found."""
    return db.query(User).filter(User.username == username).first()


def get_user_profile(db: Session, user_id: int) -> dict:
    """Return profile data and aggregate progress stats for a user."""
    user = db.get(User, user_id)
    if not user:
        return {}

    labs_completados = (
        db.query(UserLabProgress)
        .filter(
            UserLabProgress.user_id == user_id,
            UserLabProgress.estado == ProgressState.COMPLETADO,
        )
        .count()
    )

    return {
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "xp_total": user.xp_total,
        "nivel": user.nivel,
        "labs_completados": labs_completados,
    }
