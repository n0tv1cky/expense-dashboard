from src.models import ExpenseData
from src.config import LLMConfig

class ExpenseLLMService:
    """
    Service for interacting with the LLM to parse expense data from natural language input.
    """
    
    def __init__(self):
        self.config = LLMConfig()

    def get_system_prompt(self) -> str:
        """
        Returns the system prompt for the LLM.
        """
        return self.config.SYSTEM_PROMPT
    
    def parse_expense(self, user_message: str) -> ExpenseData:
        from openai import OpenAI
        client = OpenAI(api_key=self.config.api_key)
        try:
            response = client.beta.chat.completions.parse(
                model="gpt-4.1-nano",
                messages=[
                    {"role": "system", "content": self.get_system_prompt()},
                    {"role": "user", "content": user_message}
                ],
                response_format=ExpenseData
            )
            
            return response.choices[0].message.parsed
        except Exception as e:
            raise RuntimeError(f"Failed to parse expense data: {str(e)}")


if __name__ == "__main__":
    service = ExpenseLLMService()
    test_message = "coffee 200 need day before yesterday"
    parsed_expense = service.parse_expense(test_message)
    print(parsed_expense)