"""
Notion API service for creating expense entries
"""

import requests
from typing import Dict, Any
from src.config import settings
from src.models import ExpenseData
import logging

logger = logging.getLogger(__name__)

class NotionService:
    def __init__(self):
        self.token = settings.notion_token
        self.database_id = self._format_database_id(settings.notion_database_id)
        self.headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json",
            "Notion-Version": "2022-06-28",
        }

    def _format_database_id(self, database_id: str) -> str:
        """Format database ID to proper UUID format with hyphens"""
        # Remove any existing hyphens
        clean_id = database_id.replace("-", "")
        
        # Check if it's the right length (32 characters)
        if len(clean_id) != 32:
            logger.warning(f"Database ID has unexpected length: {len(clean_id)}")
            return database_id
        
        # Format as UUID: 8-4-4-4-12
        formatted_id = f"{clean_id[:8]}-{clean_id[8:12]}-{clean_id[12:16]}-{clean_id[16:20]}-{clean_id[20:]}"
        logger.info(f"Formatted database ID")
        return formatted_id

    def create_expense_page(self, expense: ExpenseData) -> Dict[str, Any]:
        """Create a new page in the Notion database with expense data"""

        url = "https://api.notion.com/v1/pages"

        # Construct the payload according to Notion API format
        payload = {
            "parent": {"database_id": self.database_id},
            "properties": {
                "Expense Name": {
                    "title": [
                        {
                            "text": {
                                "content": expense.expense_name
                            }
                        }
                    ]
                },
                "Category": {
                    "multi_select": [
                        {
                            "name": expense.category.value.replace("_", " ").title()  # Handle underscores and capitalize
                        }
                    ]
                },
                "Amount": {
                    "number": expense.amount
                },
                "Importance": {
                    "select": {
                        "name": expense.importance.value.title()  # Capitalize first letter
                    }
                },
                "Bank Account": {
                    "select": {
                        "name": expense.bank_account.value
                    }
                },
                "Assigned Date": {
                    "date": {
                        "start": expense.assigned_date
                    }
                },
                "Expense Type": {
                    "select": {
                        "name": expense.expense_type.value.title()  # Capitalize first letter
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
            error_details = ""
            if hasattr(e, 'response') and e.response is not None:
                logger.error(f"Response status: {e.response.status_code}")
                logger.error(f"Response body: {e.response.text}")
                try:
                    error_json = e.response.json()
                    error_details = f" - {error_json.get('message', 'Unknown error')}"
                except:
                    error_details = f" - Response: {e.response.text}"
            
            return {
                "success": False,
                "page_id": "",
                "url": "",
                "message": f"Failed to add expense to Notion: {str(e)}{error_details}"
            }

    def test_connection(self) -> Dict[str, Any]:
        """Test connection to Notion database"""
        database_url = f"https://api.notion.com/v1/databases/{self.database_id}"
        page_url = f"https://api.notion.com/v1/pages/{self.database_id}"

        try:
            logger.info(f"Testing Notion connection to database: {self.database_id}")
            logger.info(f"Using URL: {database_url}")
            
            # First try as database
            response = requests.get(database_url, headers=self.headers)
            
            # Log response details for debugging
            logger.info(f"Database API response status: {response.status_code}")
            
            if response.status_code == 200:
                return {
                    "success": True,
                    "message": "Successfully connected to Notion database",
                    "database_id": self.database_id,
                    "response_status": response.status_code,
                    "type": "database"
                }
            elif response.status_code == 400:
                # Check if it's a page instead of database
                logger.info("Database API failed, checking if ID is a page...")
                page_response = requests.get(page_url, headers=self.headers)
                logger.info(f"Page API response status: {page_response.status_code}")
                
                if page_response.status_code == 200:
                    return {
                        "success": False,
                        "message": f"ID {self.database_id} is a Notion PAGE, not a database. Please provide a database ID instead.",
                        "database_id": self.database_id,
                        "type": "page",
                        "error_details": response.json() if response.content else None
                    }
            
            # If neither worked, raise the original error
            response.raise_for_status()

        except requests.exceptions.RequestException as e:
            logger.error(f"Notion API error: {str(e)}")
            if hasattr(e, 'response') and e.response is not None:
                logger.error(f"Response status: {e.response.status_code}")
                logger.error(f"Response body: {e.response.text}")
            
    def get_database_schema(self) -> Dict[str, Any]:
        """Get the schema of the current database to inspect properties"""
        url = f"https://api.notion.com/v1/databases/{self.database_id}"
        
        try:
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            
            result = response.json()
            properties = result.get("properties", {})
            
            # Format properties for better readability
            formatted_properties = {}
            for prop_name, prop_data in properties.items():
                formatted_properties[prop_name] = {
                    "type": prop_data.get("type"),
                    "id": prop_data.get("id"),
                    "name": prop_data.get("name", prop_name)
                }
                
                # Add additional info for select properties
                if prop_data.get("type") == "select":
                    options = prop_data.get("select", {}).get("options", [])
                    formatted_properties[prop_name]["options"] = [opt.get("name") for opt in options]
            
            return {
                "success": True,
                "message": "Database schema retrieved successfully",
                "database_title": result.get("title", [{}])[0].get("plain_text", "Untitled"),
                "properties": formatted_properties,
                "property_names": list(properties.keys())
            }
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Error getting database schema: {str(e)}")
            return {
                "success": False,
                "message": f"Failed to get database schema: {str(e)}",
                "properties": {}
            }

    def list_databases(self) -> Dict[str, Any]:
        """List all databases accessible by the integration"""
        url = "https://api.notion.com/v1/search"
        
        payload = {
            "filter": {
                "value": "database",
                "property": "object"
            }
        }
        
        try:
            response = requests.post(url, json=payload, headers=self.headers)
            response.raise_for_status()
            
            result = response.json()
            databases = []
            
            for db in result.get("results", []):
                databases.append({
                    "id": db.get("id", ""),
                    "title": db.get("title", [{}])[0].get("plain_text", "Untitled") if db.get("title") else "Untitled",
                    "url": db.get("url", ""),
                    "created_time": db.get("created_time", ""),
                    "last_edited_time": db.get("last_edited_time", "")
                })
            
            return {
                "success": True,
                "message": f"Found {len(databases)} databases",
                "databases": databases,
                "total_results": result.get("has_more", False)
            }
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Error listing databases: {str(e)}")
            return {
                "success": False,
                "message": f"Failed to list databases: {str(e)}",
                "databases": []
            }
