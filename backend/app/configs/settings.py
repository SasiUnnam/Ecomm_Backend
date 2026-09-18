import json
from pathlib import Path

from pydantic import AliasChoices, Field, SecretStr, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    database_url: str
    database_ssl_require: bool = False

    secret_key: str
    algorithm: str = "HS256"

    access_token_expire_minutes: int = 30
    refresh_token_expire_days: int = 7

    smtp_host: str = Field(
        default="smtp-relay.brevo.com",
        validation_alias=AliasChoices("SMTP_HOST", "smtp_host"),
    )
    smtp_port: int = Field(
        default=587,
        validation_alias=AliasChoices("SMTP_PORT", "smtp_port"),
    )
    smtp_user: str = Field(
        default="",
        validation_alias=AliasChoices("SMTP_USER", "smtp_user"),
    )
    smtp_password: SecretStr = Field(
        default="",
        validation_alias=AliasChoices("SMTP_PASSWORD", "smtp_password"),
    )
    smtp_from: str = Field(
        default="",
        validation_alias=AliasChoices("SMTP_FROM", "smtp_from", "MAIL_FROM"),
    )

    allowed_origins: list[str] = Field(
        default_factory=lambda: [
            "http://localhost:3000",
            "http://127.0.0.1:3000",
            "http://localhost:5173",
            "http://127.0.0.1:5173",
            "http://localhost:8080",
            "http://127.0.0.1:8080",
        ],
        validation_alias=AliasChoices("ALLOWED_ORIGINS", "allowed_origins"),
    )

    spaces_access_key: str = Field(
        default="",
        validation_alias=AliasChoices("SPACES_ACCESS_KEY", "DO_SPACES_KEY", "AWS_ACCESS_KEY_ID"),
    )
    spaces_secret_key: str = Field(
        default="",
        validation_alias=AliasChoices("SPACES_SECRET_KEY", "DO_SPACES_SECRET", "AWS_SECRET_ACCESS_KEY"),
    )
    spaces_region: str = Field(
        default="nyc3",
        validation_alias=AliasChoices("SPACES_REGION", "DO_SPACES_REGION", "AWS_REGION"),
    )
    spaces_bucket: str = Field(
        default="",
        validation_alias=AliasChoices("SPACES_BUCKET", "DO_SPACES_BUCKET", "AWS_S3_BUCKET"),
    )
    spaces_endpoint: str = Field(
        default="",
        validation_alias=AliasChoices("SPACES_ENDPOINT", "DO_SPACES_ENDPOINT"),
    )

    @field_validator("allowed_origins", mode="before")
    @classmethod
    def parse_allowed_origins(cls, value):
        if isinstance(value, str):
            value = value.strip()
            if not value:
                return []
            if value.startswith("["):
                return json.loads(value)
            return [item.strip() for item in value.split(",") if item.strip()]
        return value

    model_config = SettingsConfigDict(
        env_file=Path(__file__).resolve().parents[2] / ".env",
        env_file_encoding="utf-8",
        extra="ignore",
        case_sensitive=False,
    )


settings = Settings()