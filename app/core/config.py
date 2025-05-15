from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    SUPER_ADMIN_USERNAME: str
    SUPER_ADMIN_PASSWORD: str

    class Config:
        env_file = ".env"
        extra = "allow"


settings = Settings()
