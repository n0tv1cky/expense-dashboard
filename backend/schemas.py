from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class ExpenseCreate(BaseModel):
    expense_details: str
    category: str
    occurrence: int = 1
    budget: float
    month: Optional[str] = None
    essential: Optional[str] = None

class ExpenseUpdate(BaseModel):
    expense_details: Optional[str] = None
    category: Optional[str] = None
    occurrence: Optional[int] = None
    budget: Optional[float] = None
    month: Optional[str] = None
    essential: Optional[str] = None
    done: Optional[bool] = None

class ExpenseResponse(BaseModel):
    id: int
    done: bool
    expense_details: str
    category: str
    occurrence: int
    budget: float
    total_spend: float
    month: Optional[str]
    essential: Optional[str]
    deleted: bool
    created_at: datetime
    updated_at: datetime
    deleted_at: Optional[datetime]

    class Config:
        from_attributes = True

class UserSettingsCreate(BaseModel):
    yearly_earning: float

class UserSettingsResponse(BaseModel):
    id: int
    yearly_earning: float
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class DashboardSummary(BaseModel):
    total_budget: float
    total_spent: float
    monthly_expenses: float
    one_time_expenses: float
    yearly_earning: float
    expenses_by_category: List[dict]
    monthly_trend: List[dict]

class CategoryResponse(BaseModel):
    categories: List[str]
    essential_types: List[str]
    months: List[str]
