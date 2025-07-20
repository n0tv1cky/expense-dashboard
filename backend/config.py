"""
Configuration settings for the FastAPI application
"""

from pydantic_settings import BaseSettings
from typing import Optional
from dotenv import load_dotenv
import os

load_dotenv("./backend/.env.dev")

class Settings(BaseSettings):
    # Notion API Configuration
    notion_token: str = os.getenv("NOTION_TOKEN")  # Notion Integration Token
    notion_database_id: str = os.getenv("NOTION_DATABASE_ID")  # Expenses Database

    # API Configuration
    api_host: str = os.getenv("BACKEND_API_HOST", "0.0.0.0")
    api_port: int = os.getenv("BACKEND_API_PORT", 8000)
    debug: bool = False

    # CORS Configuration
    cors_origins: list = ["*"]

settings = Settings()