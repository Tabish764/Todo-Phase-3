from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    app_name: str = "Task Backend API"
    app_version: str = "1.0.0"
    debug: bool = False
    frontend_origin: str = "http://localhost:3000"  # Default frontend URL

    class Config:
        env_file = ".env"


settings = Settings()