from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime

Base = declarative_base()

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
