from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine, Column, Integer, String, Float, Boolean, DateTime, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional
import os
import json
from dotenv import load_dotenv

from models import ExpenseModel, UserSettingsModel
from schemas import (
    ExpenseCreate, ExpenseUpdate, ExpenseResponse,
    UserSettingsCreate, UserSettingsResponse, DashboardSummary
)

# Load environment variables
load_dotenv()

# Database configuration
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://username:password@localhost/expenditure_db")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Create tables
Base.metadata.create_all(bind=engine)

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
def load_seed_data_from_json(json_file_path: str = "./seed.json"):
    """
    Load seed data from JSON file and return parsed data
    """
    try:
        with open(json_file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
        return data
    except FileNotFoundError:
        print(f"JSON file {json_file_path} not found")
        return None
    except json.JSONDecodeError as e:
        print(f"Error parsing JSON: {e}")
        return None

def seed_database_from_json(db: Session, json_file_path: str = "seed_data.json"):
    """
    Seed the database with data from JSON file
    """
    try:
        # Load data from JSON
        seed_data = load_seed_data_from_json(json_file_path)
        if not seed_data:
            return False
        
        # Check if settings exist, if not create default
        settings = db.query(UserSettingsModel).first()
        if not settings:
            yearly_earning = seed_data.get("user_settings", {}).get("yearly_earning", 1000000)
            default_settings = UserSettingsModel(yearly_earning=yearly_earning)
            db.add(default_settings)
            db.commit()
            print(f"Created user settings with yearly earning: ₹{yearly_earning:,}")
        
        # Check if expenses already exist
        expense_count = db.query(ExpenseModel).count()
        if expense_count > 0:
            print(f"Database already has {expense_count} expenses. Skipping seed.")
            return True
        
        # Create expenses from JSON data
        expenses_data = seed_data.get("expenses", [])
        expenses_created = []
        
        for expense_data in expenses_data:
            expense = ExpenseModel(
                expense_details=expense_data["expense_details"],
                category=expense_data["category"],
                occurrence=expense_data["occurrence"],
                budget=expense_data["budget"],
                total_spend=expense_data["total_spend"],
                month=expense_data.get("month"),
                essential=expense_data.get("essential"),
                done=expense_data.get("done", False)
            )
            expenses_created.append(expense)
            db.add(expense)
        
        # Commit all expenses
        db.commit()
        print(f"Successfully seeded database with {len(expenses_created)} expenses from JSON")
        
        # Print summary
        categories = {}
        done_count = 0
        total_budget = 0
        
        for expense in expenses_created:
            categories[expense.category] = categories.get(expense.category, 0) + 1
            if expense.done:
                done_count += 1
            total_budget += expense.total_spend
        
        print("\n📊 Seed Summary:")
        print(f"   Total Expenses: {len(expenses_created)}")
        print(f"   Completed: {done_count}")
        print(f"   Pending: {len(expenses_created) - done_count}")
        print(f"   Total Budget: ₹{total_budget:,.2f}")
        print(f"   Categories: {dict(categories)}")
        
        return True
        
    except Exception as e:
        db.rollback()
        print(f"Error seeding database from JSON: {e}")
        return False

# Updated startup event using JSON
# @app.on_event("startup")
# async def startup_event():
#     db = SessionLocal()
#     try:
#         # Seed database from JSON file
#         success = seed_database_from_json(db, "seed_data.json")
#         if not success:
#             print("Failed to seed database from JSON, falling back to default data")
#             # You can add fallback logic here if needed
#     finally:
#         db.close()

# Alternative: Manual seeding function
@app.post("/seed_database")
async def manual_seed_from_json():
    """
    Manually seed the database from JSON - useful for testing or re-seeding
    """
    db = SessionLocal()
    try:
        return seed_database_from_json(db, "./seed.json")
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