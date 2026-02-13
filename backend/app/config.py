from __future__ import annotations

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    APP_NAME: str = "TaxSupportPlatform"
    APP_ENV: str = "development"
    DEBUG: bool = False
    SECRET_KEY: str = "change-me"
    API_V1_PREFIX: str = "/api/v1"

    DATABASE_URL: str = "postgresql+asyncpg://taxapp:taxapp_secret@localhost:5432/taxapp"
    DATABASE_ECHO: bool = False

    REDIS_URL: str = "redis://localhost:6379/0"

    JWT_SECRET_KEY: str = "change-me-jwt-secret"
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 15
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    CORS_ORIGINS: list[str] = ["http://localhost:3000"]

    RATE_LIMIT_PER_MINUTE: int = 100
    EVALUATION_RATE_LIMIT_PER_MINUTE: int = 10

    model_config = {"env_file": ".env", "case_sensitive": True}

    @property
    def sync_database_url(self) -> str:
        return self.DATABASE_URL.replace("+asyncpg", "")


settings = Settings()
