"""
Chatbot conversation API routes
"""

from fastapi import APIRouter, HTTPException, Depends
from typing import Dict, Any, List
import logging

from src.models import ExpenseInput, ChatbotResponse
from src.services.nlp_service import ExpenseNLPService
from src.services.notion_service import NotionService
from src.services.llm_service import ExpenseLLMService

logger = logging.getLogger(__name__)

router = APIRouter()

def get_nlp_service():
    return ExpenseNLPService()

def get_notion_service():
    return NotionService()

def get_llm_service():
    return ExpenseLLMService()

@router.post("/chat", response_model=Dict[str, Any])
async def chat_with_bot(
    expense_input: ExpenseInput,
    nlp_service: ExpenseNLPService = Depends(get_nlp_service),
    notion_service: NotionService = Depends(get_notion_service),
    llm_service: ExpenseLLMService = Depends(get_llm_service)
):
    """
    Main chatbot endpoint - processes natural language expense input
    """
    try:
        user_message = expense_input.text.strip()

        # Process expense
        try:
            # Parse the expense
            # parsed_expense = nlp_service.parse_expense(user_message)
            parsed_expense = llm_service.parse_expense(user_message)

            # Validate that we have essential information
            if parsed_expense.amount <= 0:
                raise HTTPException(
                    status_code=400,
                    detail="Invalid expense amount. Please include a valid expense amount greater than 0."
                )

            # Add to Notion
            notion_result = notion_service.create_expense_page(parsed_expense)

            if notion_result.get("success", False):
                response_message = f"""✅ **Expense added successfully!**

💰 **Amount:** ₹{parsed_expense.amount}
🏷️ **Item:** {parsed_expense.expense_name}
📂 **Category:** {parsed_expense.category.value}
⭐ **Importance:** {parsed_expense.importance.value}
🏦 **Account:** {parsed_expense.bank_account.value}
📅 **Date:** {parsed_expense.assigned_date}

Your expense has been added to Notion! 🎉"""

                return {
                    "response": response_message,
                    "success": True,
                    "type": "expense_added",
                    "parsed_expense": {
                        "expense_name": parsed_expense.expense_name,
                        "category": parsed_expense.category.value,
                        "amount": parsed_expense.amount,
                        "importance": parsed_expense.importance.value,
                        "bank_account": parsed_expense.bank_account.value,
                        "assigned_date": parsed_expense.assigned_date
                    },
                    "notion_page_url": notion_result.get("url", "")
                }
            else:
                raise HTTPException(
                    status_code=500,
                    detail=f"Failed to add expense to Notion: {notion_result.get('message', 'Unknown error')}"
                )

        except HTTPException:
            # Re-raise HTTPExceptions so they maintain their status codes
            raise
        except Exception as e:
            logger.error(f"Error processing expense: {str(e)}")
            raise HTTPException(
                status_code=500,
                detail=f"Error processing expense: {str(e)}"
            )

    except HTTPException:
        # Re-raise HTTPExceptions so they maintain their status codes
        raise
    except Exception as e:
        logger.error(f"Error in chat endpoint: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Chatbot error: {str(e)}")

@router.get("/examples")
async def get_example_messages():
    """
    Get example expense messages for the user
    """
    return {
        "examples": [
            {
                "input": "coffee food 50 want today",
                "description": "Simple coffee purchase"
            },
            {
                "input": "uber ride transport 200 essential yesterday hdfc cc",
                "description": "Transportation expense with specific bank account"
            },
            {
                "input": "groceries 1200 essential 15 july icici cc",
                "description": "Groceries with specific date"
            },
            {
                "input": "haircut general 300 need",
                "description": "General expense with importance level"
            },
            {
                "input": "electricity bill 2500 essential indusind cc",
                "description": "Utility bill payment"
            }
        ]
    }
