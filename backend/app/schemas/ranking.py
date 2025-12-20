"""Pydantic schemas for ranking and profile responses."""
from typing import List, Optional

from pydantic import BaseModel, ConfigDict, EmailStr

from app.schemas.lab import LabSummary


class UserProfileResponse(BaseModel):
    """User profile data plus a lightweight progress summary."""

    id: int
    username: str
    email: Optional[EmailStr] = None
    xp_total: int
    nivel: int
    labs_completados: int
    labs: List[LabSummary] = []

    model_config = ConfigDict(from_attributes=True)


class RankingEntry(BaseModel):
    """Entry used for leaderboard/ranking responses."""

    username: str
    xp_total: int
    nivel: int

    model_config = ConfigDict(from_attributes=True)
