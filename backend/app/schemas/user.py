"""Pydantic schemas for user-related operations."""
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr, ConfigDict


class UserBase(BaseModel):
    """Shared user attributes for create/read operations."""

    username: str
    email: Optional[EmailStr] = None


class UserCreate(UserBase):
    """Payload for creating a new user (same fields as base for now)."""

    pass


class UserRead(UserBase):
    """Representation of a user returned by the API."""

    id: int
    xp_total: int
    nivel: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
