"""
Pydantic models for request/response schemas
"""

from pydantic import BaseModel, Field
from typing import Optional, Dict, Any
from datetime import datetime
from enum import Enum

class ExpenseCategory(str, Enum):
    BILLS_UTILITIES = "bills & utilities"
    GENERAL = "general"
    EDUCATION = "education"
    EXPERIENCES = "experiences"
    FOOD = "food"
    ENTERTAINMENT = "entertainment"
    COMMUTE = "commute"
    GIFT = "gift"
    PENDING = "pending"
    GROCERIES = "groceries"
    MEDS = "meds"
    CLOTHING = "clothing"
    VEHICLE = "vehicle"
    TRAVEL = "travel"
    HEALTH = "health"
    GADGETS = "gadgets"
    INVEST = "invest"

class ExpenseImportance(str, Enum):
    EXTRA = "extra"
    WANT = "want"
    NEED = "need"
    ESSENTIAL = "essential"
    INVESTMENT = "investment"

class ExpenseType(str, Enum):
    INCOME = "income"
    EXPENSE = "expense"

class BankAccount(str, Enum):
    IND = "IND"
    HDFC = "HDFC"
    ICICI_CC_3009 = "ICICI CC 3009"
    INDUSIND_CC_6421 = "INDUSIND CC 6421"
    HDFC_CC_6409 = "HDFC CC 6409"

class ExpenseInput(BaseModel):
    text: str = Field(..., description="Natural language expense input", example="snacks food 200 essential yesterday")

class ExpenseData(BaseModel):
    expense_name: str
    category: ExpenseCategory
    amount: float
    importance: ExpenseImportance
    bank_account: BankAccount
    assigned_date: str
    expense_type: ExpenseType = ExpenseType.EXPENSE

class ChatbotResponse(BaseModel):
    message: str
    success: bool
    data: Optional[Dict[str, Any]] = None
    parsed_expense: Optional[ExpenseData] = None

class NotionPageResponse(BaseModel):
    page_id: str
    url: str
    success: bool
    message: str
