"""Configuration module for the Todo AI Chatbot application."""
from typing import Optional
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field
import os


class Settings(BaseSettings):
    """Application settings."""
    database_url: str = Field(
        default="postgresql+asyncpg://user:password@localhost/dbname",
        alias="DATABASE_URL"
    )
    db_echo: bool = False
    google_ai_api_key: Optional[str] = None
    mcp_server_url: Optional[str] = "http://localhost:3000"
    debug: bool = False

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,  # Allow case-insensitive env var matching
        extra="allow",  
    )


settings = Settings()
