from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str

    class Config:
        env_file = "app/core/.env"
        extra = "allow"

# from pydantic import Field
# from pydantic_settings import SettingsConfigDict
# class Settings(BaseSettings):
#     database_url: str = Field(..., env="DATABASE_URL")

#     model_config = SettingsConfigDict(
#         env_file="app/core/.env",
#         extra="ignore"
#     )


settings = Settings()
