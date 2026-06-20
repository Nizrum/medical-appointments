from pydantic_settings import BaseSettings
from pydantic import ConfigDict, Field


class Settings(BaseSettings):
    database_url: str = (
        "postgresql://clinic_user:clinic_password@localhost:5432/clinic_db"
    )
    secret_key: str = Field(..., description="JWT secret key - must be set")
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    host: str = "0.0.0.0"
    port: int = 8000
    admin_email: str = Field(..., description="Admin email - must be set")
    admin_password: str = Field(..., description="Admin password - must be set")

    model_config = ConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )


settings = Settings()
