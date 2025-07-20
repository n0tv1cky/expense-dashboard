"""
FastAPI Expense Tracker Chatbot Backend
Main application entry point
"""

from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, Dict, Any
import os
from datetime import datetime
import logging

from src.routers import expense_router, chatbot_router
from src.services.nlp_service import ExpenseNLPService
from src.services.notion_service import NotionService
from src.config import settings

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title="Expense Tracker Chatbot API",
    description="A smart chatbot that parses natural language expense inputs and adds them to Notion",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure properly for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(expense_router.router, prefix="/api/v1/expenses", tags=["Expenses"])
app.include_router(chatbot_router.router, prefix="/api/v1/chatbot", tags=["Chatbot"])

@app.get("/")
async def root():
    return {"message": "Expense Tracker Chatbot API", "version": "1.0.0"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}

# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
