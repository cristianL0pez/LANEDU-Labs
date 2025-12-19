"""Application configuration settings."""
from pydantic import BaseSettings


class Settings(BaseSettings):
    """Project settings loaded from environment variables."""

    database_url: str = "postgresql+psycopg2://lanedu:lanedu_pass@db:5432/lanedu_labs"

    class Config:
        env_prefix = ""
        case_sensitive = False


settings = Settings()
