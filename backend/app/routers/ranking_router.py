"""Ranking endpoints."""
from fastapi import APIRouter, Depends

from app.schemas.ranking import RankingEntry
from app.services.ranking_service import get_ranking
from app.db.session import get_db

router = APIRouter(prefix="/ranking", tags=["ranking"])


@router.get("", response_model=list[RankingEntry], summary="Top usuarios por XP")
def list_ranking(limit: int = 10, db=Depends(get_db)):
    """Return the top users ordered by XP."""
    return get_ranking(db, limit=limit)
