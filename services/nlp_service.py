"""
Natural Language Processing service for parsing expense text
"""

import re
from datetime import datetime, timedelta
from typing import Dict, Any
from models import ExpenseData, ExpenseCategory, ExpenseImportance, BankAccount, ExpenseType

class ExpenseNLPService:
    def __init__(self):
        # Category keyword mapping
        self.categories = {
            ExpenseCategory.FOOD: ['snacks', 'lunch', 'dinner', 'breakfast', 'restaurant', 'coffee', 'pizza', 'burger', 'food'],
            ExpenseCategory.COMMUTE: ['uber', 'taxi', 'bus', 'train', 'fuel', 'petrol', 'metro', 'auto', 'transport'],
            ExpenseCategory.GENERAL: ['haircut', 'shopping', 'clothes', 'misc', 'general'],
            ExpenseCategory.ENTERTAINMENT: ['movie', 'cinema', 'games', 'book', 'music'],
            ExpenseCategory.HEALTH: ['medicine', 'doctor', 'hospital', 'pharmacy'],
            ExpenseCategory.BILLS_UTILITIES: ['electricity', 'water', 'phone', 'internet', 'rent', 'bill'],
            ExpenseCategory.GROCERIES: ['vegetables', 'grocery', 'supermarket', 'mart'],
            ExpenseCategory.MEDS: ['medicine', 'pills', 'pharmacy', 'medical'],
            ExpenseCategory.CLOTHING: ['shirt', 'pants', 'dress', 'shoes', 'clothing'],
            ExpenseCategory.GADGETS: ['phone', 'laptop', 'computer', 'gadget', 'electronic']
        }

        # Bank account mapping
        self.bank_accounts = {
            'hdfc cc': BankAccount.HDFC_CC_6409,
            'icici cc': BankAccount.ICICI_CC_3009,
            'indusind cc': BankAccount.INDUSIND_CC_6421,
            'hdfc': BankAccount.HDFC,
            'ind': BankAccount.IND
        }

        # Month mapping for date parsing
        self.months = {
            'jan': 1, 'feb': 2, 'mar': 3, 'apr': 4, 'may': 5, 'jun': 6,
            'jul': 7, 'aug': 8, 'sep': 9, 'oct': 10, 'nov': 11, 'dec': 12,
            'january': 1, 'february': 2, 'march': 3, 'april': 4, 'may': 5, 'june': 6,
            'july': 7, 'august': 8, 'september': 9, 'october': 10, 'november': 11, 'december': 12
        }

    def parse_expense(self, text: str) -> ExpenseData:
        """Parse natural language text into structured expense data"""

        # Initialize with defaults
        result = {
            'expense_name': '',
            'category': ExpenseCategory.GENERAL,
            'amount': 0.0,
            'importance': ExpenseImportance.NEED,
            'bank_account': BankAccount.HDFC,
            'assigned_date': datetime.now().strftime('%Y-%m-%d'),
            'expense_type': ExpenseType.EXPENSE
        }

        text_lower = text.lower().strip()
        tokens = re.split(r'[\s,]+', text_lower)

        # Extract amount
        amount_pattern = r'\b\d+(?:\.\d+)?\b'
        amounts = re.findall(amount_pattern, text)
        if amounts:
            result['amount'] = float(amounts[0])

        # Extract date
        result['assigned_date'] = self._extract_date(text_lower)

        # Extract category
        result['category'] = self._extract_category(text_lower)

        # Extract importance
        result['importance'] = self._extract_importance(text_lower)

        # Extract bank account
        result['bank_account'] = self._extract_bank_account(text_lower)

        # Extract expense name
        result['expense_name'] = self._extract_expense_name(tokens)

        return ExpenseData(**result)

    def _extract_date(self, text: str) -> str:
        """Extract date from text"""
        # Handle relative dates
        if 'today' in text:
            return datetime.now().strftime('%Y-%m-%d')
        elif 'yesterday' in text:
            return (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
        elif 'tomorrow' in text:
            return (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d')

        # Handle specific dates like "9 july"
        date_pattern = r'\b(\d{1,2})\s+(\w+)\b'
        date_match = re.search(date_pattern, text)
        if date_match:
            day = int(date_match.group(1))
            month_str = date_match.group(2).lower()
            if month_str in self.months:
                month = self.months[month_str]
                year = datetime.now().year
                try:
                    parsed_date = datetime(year, month, day)
                    return parsed_date.strftime('%Y-%m-%d')
                except ValueError:
                    pass

        return datetime.now().strftime('%Y-%m-%d')

    def _extract_category(self, text: str) -> ExpenseCategory:
        """Extract category from text"""
        for category, keywords in self.categories.items():
            for keyword in keywords:
                if keyword in text:
                    return category
        return ExpenseCategory.GENERAL

    def _extract_importance(self, text: str) -> ExpenseImportance:
        """Extract importance level from text"""
        importance_keywords = {
            'essential': ExpenseImportance.ESSENTIAL,
            'need': ExpenseImportance.NEED,
            'want': ExpenseImportance.WANT,
            'extra': ExpenseImportance.EXTRA,
            'investment': ExpenseImportance.INVESTMENT
        }

        for keyword, importance in importance_keywords.items():
            if keyword in text:
                return importance
        return ExpenseImportance.NEED

    def _extract_bank_account(self, text: str) -> BankAccount:
        """Extract bank account from text"""
        for bank_key, bank_value in self.bank_accounts.items():
            if bank_key in text:
                return bank_value
        return BankAccount.HDFC

    def _extract_expense_name(self, tokens: list) -> str:
        """Extract expense name from tokens"""
        skip_words = [
            'essential', 'need', 'want', 'extra', 'investment',
            'today', 'yesterday', 'tomorrow', 'hdfc', 'icici', 'indusind',
            'cc', 'jan', 'feb', 'mar', 'apr', 'may', 'jun',
            'jul', 'aug', 'sep', 'oct', 'nov', 'dec'
        ]

        expense_words = []
        for token in tokens:
            if (not re.match(r'^\d+(?:\.\d+)?$', token) and 
                token not in skip_words and 
                len(expense_words) < 3):
                expense_words.append(token)

        return ' '.join(expense_words) if expense_words else 'Expense'
