from pydantic_settings import BaseSettings
from pydantic import ConfigDict


class Settings(BaseSettings):
    port: int = 8000
    database_url: str = (
        "postgresql://clinic_user:clinic_password@localhost:5432/clinic_db"
    )
    secret_key: str = "secret-key"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30

    model_config = ConfigDict(env_file=".env")


settings = Settings()
