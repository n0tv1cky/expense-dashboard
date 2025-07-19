"""
Expense-related API routes
"""

from fastapi import APIRouter, HTTPException, Depends
from typing import List, Dict, Any
import logging

from backend.models import ExpenseInput, ExpenseData, ChatbotResponse, NotionPageResponse
from backend.services.nlp_service import ExpenseNLPService
from backend.services.notion_service import NotionService

logger = logging.getLogger(__name__)

router = APIRouter()

# Dependency injection
def get_nlp_service():
    return ExpenseNLPService()

def get_notion_service():
    return NotionService()

@router.post("/parse", response_model=ChatbotResponse)
async def parse_expense_text(
    expense_input: ExpenseInput,
    nlp_service: ExpenseNLPService = Depends(get_nlp_service)
):
    """
    Parse natural language expense text into structured data
    """
    try:
        parsed_expense = nlp_service.parse_expense(expense_input.text)

        return ChatbotResponse(
            message="Successfully parsed expense text",
            success=True,
            parsed_expense=parsed_expense,
            data={
                "original_text": expense_input.text,
                "parsed_fields": {
                    "expense_name": parsed_expense.expense_name,
                    "category": parsed_expense.category.value,
                    "amount": parsed_expense.amount,
                    "importance": parsed_expense.importance.value,
                    "bank_account": parsed_expense.bank_account.value,
                    "assigned_date": parsed_expense.assigned_date,
                    "expense_type": parsed_expense.expense_type.value
                }
            }
        )
    except Exception as e:
        logger.error(f"Error parsing expense text: {str(e)}")
        raise HTTPException(status_code=400, detail=f"Failed to parse expense: {str(e)}")

@router.post("/add-to-notion", response_model=NotionPageResponse)
async def add_expense_to_notion(
    expense_data: ExpenseData,
    notion_service: NotionService = Depends(get_notion_service)
):
    """
    Add parsed expense data to Notion database
    """
    try:
        result = notion_service.create_expense_page(expense_data)

        return NotionPageResponse(
            page_id=result.get("page_id", ""),
            url=result.get("url", ""),
            success=result.get("success", False),
            message=result.get("message", "Unknown error occurred")
        )
    except Exception as e:
        logger.error(f"Error adding expense to Notion: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to add expense to Notion: {str(e)}")

@router.post("/process", response_model=Dict[str, Any])
async def process_complete_expense(
    expense_input: ExpenseInput,
    nlp_service: ExpenseNLPService = Depends(get_nlp_service),
    notion_service: NotionService = Depends(get_notion_service)
):
    """
    Complete workflow: Parse expense text and add to Notion in one step
    """
    try:
        # Parse the expense
        parsed_expense = nlp_service.parse_expense(expense_input.text)
        logger.info(f"Parsed expense: {parsed_expense}")

        # Add to Notion
        notion_result = notion_service.create_expense_page(parsed_expense)
        logger.info(f"Notion result: {notion_result}")

        return {
            "success": notion_result.get("success", False),
            "message": notion_result.get("message", ""),
            "original_text": expense_input.text,
            "parsed_expense": {
                "expense_name": parsed_expense.expense_name,
                "category": parsed_expense.category.value,
                "amount": parsed_expense.amount,
                "importance": parsed_expense.importance.value,
                "bank_account": parsed_expense.bank_account.value,
                "assigned_date": parsed_expense.assigned_date,
                "expense_type": parsed_expense.expense_type.value
            },
            "notion_page": {
                "page_id": notion_result.get("page_id", ""),
                "url": notion_result.get("url", "")
            }
        }
    except Exception as e:
        logger.error(f"Error processing expense: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to process expense: {str(e)}")

@router.get("/test-notion")
async def test_notion_connection(
    notion_service: NotionService = Depends(get_notion_service)
):
    """
    Test connection to Notion database
    """
    try:
        result = notion_service.test_connection()
        return result
    except Exception as e:
        logger.error(f"Error testing Notion connection: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to test Notion connection: {str(e)}")

@router.get("/list-databases")
async def list_notion_databases(
    notion_service: NotionService = Depends(get_notion_service)
):
    """
    List all databases accessible by the Notion integration
    """
    try:
        result = notion_service.list_databases()
        return result
    except Exception as e:
        logger.error(f"Error listing Notion databases: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to list Notion databases: {str(e)}")

@router.get("/database-schema")
async def get_database_schema(
    notion_service: NotionService = Depends(get_notion_service)
):
    """
    Get the schema of the current Notion database
    """
    try:
        result = notion_service.get_database_schema()
        return result
    except Exception as e:
        logger.error(f"Error getting database schema: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to get database schema: {str(e)}")
