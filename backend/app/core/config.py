from functools import lru_cache

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    app_name: str = "KoyunChat"
    app_env: str = "development"
    app_url: str = "http://localhost"
    allowed_origins: list[str] = Field(default_factory=lambda: ["http://localhost", "http://localhost:3000"])

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
    def split_allowed_origins(cls, value: str | list[str]) -> list[str]:
        if isinstance(value, str):
            return [item.strip() for item in value.split(",") if item.strip()]
        return value


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
