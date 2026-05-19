from functools import lru_cache
from typing import Any

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    app_name: str = "KoyunChat"
    app_env: str = "development"
    app_url: str = "http://localhost"
    # Keep this as a plain string so pydantic-settings does not try to JSON-decode
    # comma-separated values from Docker/.env files before validators run.
    allowed_origins: str | list[str] | None = "http://localhost,http://localhost:3000"

    database_url: str = "postgresql+psycopg://koyunchat:change_me@localhost:5432/koyunchat"
    redis_url: str = "redis://localhost:6379/0"

    jwt_secret: str = "change_me_long_random_string"
    jwt_expire_minutes: int = 10080
    jwt_algorithm: str = "HS256"

    openai_api_key: str | None = None
    openai_base_url: str = "https://api.openai.com/v1"
    openai_model: str = "gpt-4o-mini"

    smtp_host: str | None = None
    smtp_port: int = 587
    smtp_user: str | None = None
    smtp_password: str | None = None
    smtp_from: str | None = None

    stripe_secret_key: str | None = None
    stripe_webhook_secret: str | None = None

    easypay_pid: str | None = None
    easypay_key: str | None = None
    easypay_notify_url: str | None = None

    @field_validator("allowed_origins", mode="before")
    @classmethod
    def parse_allowed_origins(cls, value: Any) -> str | list[str] | None:
        return value

    @property
    def cors_origins(self) -> list[str]:
        value = self.allowed_origins
        if not value:
            return ["http://localhost", "http://localhost:3000"]
        if isinstance(value, list):
            return [str(item).strip() for item in value if str(item).strip()]
        raw = str(value).strip()
        if raw.startswith("[") and raw.endswith("]"):
            # Lightweight support for JSON-like env values without requiring them.
            try:
                import json

                parsed = json.loads(raw)
                if isinstance(parsed, list):
                    return [str(item).strip() for item in parsed if str(item).strip()]
            except Exception:
                pass
        return [item.strip() for item in raw.split(",") if item.strip()]


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
