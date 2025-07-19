"""
Configuration settings for the FastAPI application
"""

from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    # Notion API Configuration
    notion_token: str = "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"
    notion_database_id: str = "ea13a4a3-454f-4237-ba71-86801be0b703"  # June '25 Expenses database

    # API Configuration
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    debug: bool = False

    # CORS Configuration
    cors_origins: list = ["*"]

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()