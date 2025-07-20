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

from src.models import ExpenseCategory, ExpenseImportance, BankAccount, ExpenseType
from datetime import datetime
import os
class LLMConfig:
    """Configuration for the LLM service"""
    api_key: str = os.getenv("OPENAI_API_KEY")
    current_date = datetime.now().strftime('%d-%m-%Y')
    categories = [c.value for c in ExpenseCategory]
    importances = [i.value for i in ExpenseImportance]
    bank_accounts = [b.value for b in BankAccount]
    expense_types = [e.value for e in ExpenseType]

    SYSTEM_PROMPT = f"""
You are a personal finance assistant for expense tracking.

Today's date is {current_date} (format: DD-MM-YYYY, timezone: Asia/Kolkata).

Your job is to extract a structured record for each new expense from a user's natural language message.
Strictly follow these instructions:

Fields required:
- expense_name: Short description.
- category: One of {categories!r}. If unsure, use "general".
- amount: As float.
- importance: One of {importances!r}. If unclear, use "essential".
- bank_account: One of {bank_accounts!r}. If not mentioned, use "HDFC".
- assigned_date: Date in DD-MM-YYYY. If nothing is mentioned or 'today' is mentioned, use {current_date}.
- expense_type: "expense" unless clearly income.

Only use values from above enums. Output as single JSON object matching this schema:

{{
    "expense_name": "<description>",
    "category": "<one of: {categories}>",
    "amount": <float>,
    "importance": "<one of: {importances}>",
    "bank_account": "<one of: {bank_accounts}>",
    "assigned_date": "<DD-MM-YYYY>",
    "expense_type": "<expense/income>"
}}
    """