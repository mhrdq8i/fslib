# core/config.py
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str

    class Config:
        env_file = "app/core/.env"
        extra = "ignore"


settings = Settings()
