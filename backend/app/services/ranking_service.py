"""Service layer for ranking and leaderboard operations."""
from typing import List

from sqlalchemy.orm import Session

from app.models.user import User


def get_ranking(db: Session, limit: int = 10) -> List[dict]:
    """Return the top users ordered by XP (descending)."""
    users = (
        db.query(User)
        .order_by(User.xp_total.desc(), User.nivel.desc(), User.id.asc())
        .limit(limit)
        .all()
    )
    return [
        {"username": user.username, "xp_total": user.xp_total, "nivel": user.nivel}
        for user in users
    ]
