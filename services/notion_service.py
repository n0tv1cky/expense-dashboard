"""
Notion API service for creating expense entries
"""

import requests
from typing import Dict, Any
from config import settings
from models import ExpenseData
import logging

logger = logging.getLogger(__name__)

class NotionService:
    def __init__(self):
        self.token = settings.notion_token
        self.database_id = settings.notion_database_id
        self.headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json",
            "Notion-Version": "2022-06-28",
        }

    def create_expense_page(self, expense: ExpenseData) -> Dict[str, Any]:
        """Create a new page in the Notion database with expense data"""

        url = "https://api.notion.com/v1/pages"

        # Construct the payload according to Notion API format
        payload = {
            "parent": {"database_id": self.database_id},
            "properties": {
                "expense name": {
                    "title": [
                        {
                            "text": {
                                "content": expense.expense_name
                            }
                        }
                    ]
                },
                "category": {
                    "select": {
                        "name": expense.category.value
                    }
                },
                "amount": {
                    "number": expense.amount
                },
                "importance": {
                    "select": {
                        "name": expense.importance.value
                    }
                },
                "bank account": {
                    "select": {
                        "name": expense.bank_account.value
                    }
                },
                "assigned date": {
                    "date": {
                        "start": expense.assigned_date
                    }
                },
                "expense type": {
                    "select": {
                        "name": expense.expense_type.value
                    }
                },
                "Date": {
                    "date": {
                        "start": expense.assigned_date
                    }
                }
            }
        }

        try:
            response = requests.post(url, json=payload, headers=self.headers)
            response.raise_for_status()

            result = response.json()
            page_id = result.get("id", "")
            page_url = result.get("url", "")

            logger.info(f"Successfully created Notion page: {page_id}")

            return {
                "success": True,
                "page_id": page_id,
                "url": page_url,
                "message": "Expense added to Notion successfully!"
            }

        except requests.exceptions.RequestException as e:
            logger.error(f"Error creating Notion page: {str(e)}")
            return {
                "success": False,
                "page_id": "",
                "url": "",
                "message": f"Failed to add expense to Notion: {str(e)}"
            }

    def test_connection(self) -> Dict[str, Any]:
        """Test connection to Notion database"""
        url = f"https://api.notion.com/v1/databases/{self.database_id}"

        try:
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()

            return {
                "success": True,
                "message": "Successfully connected to Notion database"
            }

        except requests.exceptions.RequestException as e:
            return {
                "success": False,
                "message": f"Failed to connect to Notion database: {str(e)}"
            }
