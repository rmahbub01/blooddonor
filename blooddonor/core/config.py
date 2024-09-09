import secrets
from pathlib import Path
from typing import Any

from pydantic import AnyHttpUrl, EmailStr, field_validator, model_validator
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    SECRET_KEY: str = secrets.token_urlsafe(32)
    # 60 minutes * 24 hours * 8 days = 8 days
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8
    SERVER_NAME: str = "127.0.0.1"
    SERVER_HOST: AnyHttpUrl
    # BACKEND_CORS_ORIGINS is a JSON-formatted list of origins
    # e.g: '["http://localhost", "http://localhost:4200", "http://localhost:3000", \
    # "http://localhost:8080", "http://local.dockertoolbox.tiangolo.com"]'
    BACKEND_CORS_ORIGINS: list[AnyHttpUrl] = []

    @field_validator("BACKEND_CORS_ORIGINS", mode="before")
    def assemble_cors_origins(cls, v: str | list[str]) -> list[str] | str:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(f"Invalid value for BACKEND_CORS_ORIGINS: {v}")

    PROJECT_NAME: str

    SQLALCHEMY_DATABASE_URI: str | None = None

    SMTP_TLS: bool = False
    SMTP_PORT: int | None = None
    SMTP_HOST: str | None = None
    SMTP_USER: str | None = None
    SMTP_PASSWORD: str | None = None
    EMAILS_FROM_EMAIL: EmailStr | None = None
    EMAILS_FROM_NAME: str | None = None
    EMAIL_RESET_TOKEN_EXPIRE_HOURS: int = 48
    EMAIL_TEMPLATES_DIR: str = "./blooddonor/email_templates"
    EMAILS_ENABLED: bool = False

    @model_validator(mode="before")
    def get_emails_enabled(cls, values: dict[str, Any]) -> dict[str, Any]:
        if (
            values.get("SMTP_HOST")
            and values.get("SMTP_PORT")
            and values.get("EMAILS_FROM_EMAIL")
        ):
            values["EMAILS_ENABLED"] = True
        return values

    EMAIL_TEST_USER: EmailStr | None = None  # type: ignore
    FIRST_SUPERUSER: str
    FIRST_SUPERUSER_GENDER: str
    FIRST_SUPERUSER_PASSWORD: str
    FIRST_SUPERUSER_MOBILE: str
    FIRST_SUPERUSER_EMAIL: str
    FIRST_SUPERUSER_NID: str
    FIRST_SUPERUSER_DISTRICT: str
    FIRST_SUPERUSER_BLOOD_GROUP: str
    FIRST_SUPERUSER_STUDENTSHIP_STATUS: str
    USERS_OPEN_REGISTRATION: bool = True

    # Automatics Documentations UI
    DOCS_URL: str | None = "/docs"
    REDOC_URL: str | None = "/redoc"

    class Config:
        case_sensitive = True
        env_file = ".env"
        env_file_encoding = "utf-8"


BASE_DIR = Path(__file__).resolve().parent.parent.parent
settings = Settings()
