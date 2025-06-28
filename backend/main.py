from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine, Column, Integer, String, Float, Boolean, DateTime, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Database configuration
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://username:password@localhost/expenditure_db")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Database Models
class ExpenseModel(Base):
    __tablename__ = "expenses"
    
    id = Column(Integer, primary_key=True, index=True)
    done = Column(Boolean, default=False)
    expense_details = Column(String, nullable=False)
    category = Column(String, nullable=False)
    occurrence = Column(Integer, default=1)
    budget = Column(Float, nullable=False)
    total_spend = Column(Float, nullable=False)
    month = Column(String, nullable=True)
    essential = Column(String, nullable=True)
    deleted = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    deleted_at = Column(DateTime, nullable=True)

class UserSettingsModel(Base):
    __tablename__ = "user_settings"
    
    id = Column(Integer, primary_key=True, index=True)
    yearly_earning = Column(Float, default=1000000)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

# Create tables
Base.metadata.create_all(bind=engine)

# Pydantic Models
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

# FastAPI App
app = FastAPI(title="Expenditure Forecast API", version="1.0.0")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173"],  # React dev servers
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dependency to get database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Initialize default settings
@app.on_event("startup")
async def startup_event():
    db = SessionLocal()
    try:
        # Check if settings exist, if not create default
        settings = db.query(UserSettingsModel).first()
        if not settings:
            default_settings = UserSettingsModel(yearly_earning=1000000)
            db.add(default_settings)
            db.commit()
            
        # Create sample data if no expenses exist
        expense_count = db.query(ExpenseModel).count()
        if expense_count == 0:
            sample_expenses = [
                ExpenseModel(
                    expense_details="Parekatta Donation",
                    category="Essential",
                    occurrence=1,
                    budget=25000,
                    total_spend=25000,
                    month="Dec",
                    essential="Must Do"
                ),
                ExpenseModel(
                    expense_details="Maamu Gift",
                    category="Essential",
                    occurrence=1,
                    budget=2000,
                    total_spend=2000,
                    month="Jun",
                    essential="Must Do",
                    done=True
                ),
                ExpenseModel(
                    expense_details="Ather EMI",
                    category="Needs",
                    occurrence=12,
                    budget=7000,
                    total_spend=84000,
                    essential="Essential"
                ),
                ExpenseModel(
                    expense_details="Food (227 / day)",
                    category="Needs",
                    occurrence=12,
                    budget=5000,
                    total_spend=60000
                ),
                ExpenseModel(
                    expense_details="Netflix Subscription",
                    category="Wants",
                    occurrence=12,
                    budget=800,
                    total_spend=9600
                )
            ]
            
            for expense in sample_expenses:
                db.add(expense)
            db.commit()
    finally:
        db.close()

# API Routes

@app.get("/")
async def root():
    return {"message": "Expenditure Forecast API is running!"}

# Expense endpoints
@app.get("/expenses", response_model=List[ExpenseResponse])
async def get_expenses(
    include_deleted: bool = False,
    category: Optional[str] = None,
    db: Session = Depends(get_db)
):
    query = db.query(ExpenseModel)
    
    if not include_deleted:
        query = query.filter(ExpenseModel.deleted == False)
    
    if category:
        query = query.filter(ExpenseModel.category == category)
    
    expenses = query.order_by(ExpenseModel.created_at.desc()).all()
    return expenses

@app.get("/expenses/{expense_id}", response_model=ExpenseResponse)
async def get_expense(expense_id: int, db: Session = Depends(get_db)):
    expense = db.query(ExpenseModel).filter(ExpenseModel.id == expense_id).first()
    if not expense:
        raise HTTPException(status_code=404, detail="Expense not found")
    return expense

@app.post("/expenses", response_model=ExpenseResponse)
async def create_expense(expense: ExpenseCreate, db: Session = Depends(get_db)):
    # Calculate total spend
    total_spend = expense.budget * expense.occurrence
    
    db_expense = ExpenseModel(
        expense_details=expense.expense_details,
        category=expense.category,
        occurrence=expense.occurrence,
        budget=expense.budget,
        total_spend=total_spend,
        month=expense.month,
        essential=expense.essential
    )
    
    db.add(db_expense)
    db.commit()
    db.refresh(db_expense)
    return db_expense

@app.put("/expenses/{expense_id}", response_model=ExpenseResponse)
async def update_expense(
    expense_id: int, 
    expense_update: ExpenseUpdate, 
    db: Session = Depends(get_db)
):
    db_expense = db.query(ExpenseModel).filter(ExpenseModel.id == expense_id).first()
    if not db_expense:
        raise HTTPException(status_code=404, detail="Expense not found")
    
    # Update fields if provided
    update_data = expense_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_expense, field, value)
    
    # Recalculate total spend if budget or occurrence changed
    if 'budget' in update_data or 'occurrence' in update_data:
        db_expense.total_spend = db_expense.budget * db_expense.occurrence
    
    db_expense.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(db_expense)
    return db_expense

@app.delete("/expenses/{expense_id}")
async def delete_expense(expense_id: int, db: Session = Depends(get_db)):
    db_expense = db.query(ExpenseModel).filter(ExpenseModel.id == expense_id).first()
    if not db_expense:
        raise HTTPException(status_code=404, detail="Expense not found")
    
    # Soft delete
    db_expense.deleted = True
    db_expense.deleted_at = datetime.utcnow()
    db.commit()
    
    return {"message": "Expense deleted successfully"}

@app.put("/expenses/{expense_id}/restore")
async def restore_expense(expense_id: int, db: Session = Depends(get_db)):
    db_expense = db.query(ExpenseModel).filter(ExpenseModel.id == expense_id).first()
    if not db_expense:
        raise HTTPException(status_code=404, detail="Expense not found")
    
    db_expense.deleted = False
    db_expense.deleted_at = None
    db_expense.updated_at = datetime.utcnow()
    db.commit()
    return {"message": "Expense restored successfully"}

@app.put("/expenses/{expense_id}/toggle-done")
async def toggle_expense_done(expense_id: int, db: Session = Depends(get_db)):
    db_expense = db.query(ExpenseModel).filter(ExpenseModel.id == expense_id).first()
    if not db_expense:
        raise HTTPException(status_code=404, detail="Expense not found")
    
    db_expense.done = not db_expense.done
    db_expense.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(db_expense)
    return db_expense

# Trash endpoints
@app.get("/expenses/trash", response_model=List[ExpenseResponse])
async def get_trashed_expenses(db: Session = Depends(get_db)):
    expenses = db.query(ExpenseModel).filter(ExpenseModel.deleted == True).order_by(ExpenseModel.deleted_at.desc()).all()
    return expenses

@app.delete("/expenses/{expense_id}/permanent")
async def permanently_delete_expense(expense_id: int, db: Session = Depends(get_db)):
    db_expense = db.query(ExpenseModel).filter(ExpenseModel.id == expense_id).first()
    if not db_expense:
        raise HTTPException(status_code=404, detail="Expense not found")
    
    db.delete(db_expense)
    db.commit()
    return {"message": "Expense permanently deleted"}

# User Settings endpoints
@app.get("/settings", response_model=UserSettingsResponse)
async def get_user_settings(db: Session = Depends(get_db)):
    settings = db.query(UserSettingsModel).first()
    if not settings:
        # Create default settings if none exist
        settings = UserSettingsModel(yearly_earning=1000000)
        db.add(settings)
        db.commit()
        db.refresh(settings)
    return settings

@app.put("/settings", response_model=UserSettingsResponse)
async def update_user_settings(settings_update: UserSettingsCreate, db: Session = Depends(get_db)):
    settings = db.query(UserSettingsModel).first()
    if not settings:
        settings = UserSettingsModel(yearly_earning=settings_update.yearly_earning)
        db.add(settings)
    else:
        settings.yearly_earning = settings_update.yearly_earning
        settings.updated_at = datetime.utcnow()
    
    db.commit()
    db.refresh(settings)
    return settings

# Dashboard endpoint
@app.get("/dashboard", response_model=DashboardSummary)
async def get_dashboard_summary(db: Session = Depends(get_db)):
    # Get user settings
    settings = db.query(UserSettingsModel).first()
    yearly_earning = settings.yearly_earning if settings else 1000000
    
    # Get all active expenses
    expenses = db.query(ExpenseModel).filter(ExpenseModel.deleted == False).all()
    
    # Calculate summary data
    total_budget = sum(expense.budget * expense.occurrence for expense in expenses)
    total_spent = sum(expense.total_spend for expense in expenses if expense.done)
    monthly_expenses = sum(expense.budget for expense in expenses if expense.occurrence == 12)
    one_time_expenses = sum(expense.budget for expense in expenses if expense.occurrence == 1)
    
    # Calculate expenses by category
    category_totals = {}
    for expense in expenses:
        if expense.category not in category_totals:
            category_totals[expense.category] = 0
        category_totals[expense.category] += expense.budget * expense.occurrence
    
    expenses_by_category = [
        {"name": category, "value": total}
        for category, total in category_totals.items()
    ]
    
    # Calculate monthly trend (simplified - you can enhance this)
    months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    monthly_trend = []
    
    for month in months:
        month_expenses = sum(
            expense.budget for expense in expenses 
            if expense.month == month or (expense.occurrence == 12 and not expense.month)
        )
        month_budget = sum(
            expense.budget for expense in expenses 
            if expense.month == month or expense.occurrence == 12
        )
        
        monthly_trend.append({
            "month": month,
            "expenses": month_expenses,
            "budget": month_budget
        })
    
    return DashboardSummary(
        total_budget=total_budget,
        total_spent=total_spent,
        monthly_expenses=monthly_expenses,
        one_time_expenses=one_time_expenses,
        yearly_earning=yearly_earning,
        expenses_by_category=expenses_by_category,
        monthly_trend=monthly_trend
    )

# Category and utility endpoints
@app.get("/categories")
async def get_categories():
    return {
        "categories": ["Essential", "Needs", "Wants", "Invest"],
        "essential_types": ["Must Do", "Essential", ""],
        "months": ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    }

# Health check
@app.get("/health")
async def health_check():
    return {"status": "healthy", "timestamp": datetime.utcnow()}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)