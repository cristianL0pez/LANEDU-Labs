"""Declarative base and model registry for SQLAlchemy."""
from sqlalchemy.orm import declarative_base

Base = declarative_base()

# Import models here so that Alembic and metadata discovery work automatically.
# These imports should stay at the bottom to avoid circular dependencies.
from app.models.user import User  # noqa: E402,F401
from app.models.lab import Lab  # noqa: E402,F401
from app.models.user_lab_progress import UserLabProgress  # noqa: E402,F401
