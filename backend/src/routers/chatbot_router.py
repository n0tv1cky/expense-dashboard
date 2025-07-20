"""
Chatbot conversation API routes
"""

from fastapi import APIRouter, HTTPException, Depends
from typing import Dict, Any, List
import logging

from src.models import ExpenseInput, ChatbotResponse
from src.services.nlp_service import ExpenseNLPService
from src.services.notion_service import NotionService

logger = logging.getLogger(__name__)

router = APIRouter()

def get_nlp_service():
    return ExpenseNLPService()

def get_notion_service():
    return NotionService()

@router.post("/chat", response_model=Dict[str, Any])
async def chat_with_bot(
    expense_input: ExpenseInput,
    nlp_service: ExpenseNLPService = Depends(get_nlp_service),
    notion_service: NotionService = Depends(get_notion_service)
):
    """
    Main chatbot endpoint - processes natural language expense input
    """
    try:
        user_message = expense_input.text.strip()

        # Handle greeting messages
        if any(greeting in user_message.lower() for greeting in ['hello', 'hi', 'hey', 'start']):
            return {
                "response": "Hello! I'm your expense tracker assistant. You can tell me about your expenses in natural language. For example: \"snacks food 200 essential yesterday\" or \"uber ride 150 need today\". I'll parse it and add it to your Notion database!",
                "success": True,
                "type": "greeting"
            }

        # Handle help messages
        if any(help_word in user_message.lower() for help_word in ['help', 'how', 'example']):
            return {
                "response": """I can help you track expenses! Here are some examples of how to format your expenses:

📝 **Format**: [Item] [Category] [Amount] [Importance] [Date] [Bank Account]

**Examples:**
• "coffee food 50 want today"
• "uber transport 200 essential yesterday hdfc cc"
• "haircut general 300 need 15 july"
• "groceries food 1200 essential icici cc"

**Categories:** food, transport, general, entertainment, health, bills, groceries, etc.
**Importance:** essential, need, want, extra, investment
**Bank Accounts:** hdfc, icici cc, indusind cc, etc.
**Dates:** today, yesterday, tomorrow, or specific dates like "15 july"

Just type your expense and I'll add it to your Notion database! 🎯""",
                "success": True,
                "type": "help"
            }

        # Process expense
        try:
            # Parse the expense
            parsed_expense = nlp_service.parse_expense(user_message)

            # Validate that we have essential information
            if parsed_expense.amount <= 0:
                return {
                    "response": "I couldn't find a valid amount in your message. Please include the expense amount. For example: 'coffee 50' or 'lunch 200'",
                    "success": False,
                    "type": "error"
                }

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
                return {
                    "response": f"❌ Failed to add expense to Notion: {notion_result.get('message', 'Unknown error')}",
                    "success": False,
                    "type": "error"
                }

        except Exception as e:
            logger.error(f"Error processing expense: {str(e)}")
            return {
                "response": f"❌ Sorry, I encountered an error processing your expense: {str(e)}. Please try again.",
                "success": False,
                "type": "error"
            }

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
