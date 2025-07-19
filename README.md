# Expense Tracker Chatbot - FastAPI Backend

A smart chatbot that parses natural language expense inputs and automatically adds them to your Notion expense tracker database.

## Features

🤖 **Natural Language Processing**: Parse expenses like "snacks food 200 essential yesterday"
📊 **Notion Integration**: Automatically add expenses to your Notion database
🏦 **Multi-Account Support**: Track expenses across different bank accounts
📅 **Smart Date Parsing**: Handles "today", "yesterday", specific dates like "15 july"
⚡ **FastAPI Backend**: High-performance async API with automatic documentation
🐳 **Docker Ready**: Easy deployment with Docker and docker-compose

## Quick Start

### 1. Clone and Setup

```bash
git clone <your-repo>
cd expense-tracker-chatbot
```

### 2. Configure Environment

Copy `.env.example` to `.env` and fill in your Notion credentials:

```bash
cp .env.example .env
```

Edit `.env`:
```
NOTION_TOKEN=your_notion_integration_token_here
NOTION_DATABASE_ID=your_notion_database_id_here
```

### 3. Setup Notion Database

Create a Notion database with these properties:
- **expense name** (Title)
- **category** (Select): bills & utilities, general, food, transport, etc.
- **amount** (Number)
- **importance** (Select): essential, need, want, extra, investment
- **bank account** (Select): HDFC, ICICI CC 3009, etc.
- **assigned date** (Date)
- **expense type** (Select): income, expense
- **Date** (Date)

### 4. Run with Docker (Recommended)

```bash
docker-compose up --build
```

### 5. Or Run Locally

```bash
pip install -r requirements.txt
uvicorn main:app --reload
```

## API Endpoints

- `POST /api/v1/chatbot/chat` - Main chatbot interface
- `POST /api/v1/expenses/process` - Process complete expense
- `GET /docs` - API documentation
- `GET /health` - Health check

## Usage Examples

### Chat Interface
```bash
curl -X POST "http://localhost:8000/api/v1/chatbot/chat" \
     -H "Content-Type: application/json" \
     -d '{"text": "coffee food 50 want today"}'
```

### Direct Expense Processing
```bash
curl -X POST "http://localhost:8000/api/v1/expenses/process" \
     -H "Content-Type: application/json" \
     -d '{"text": "uber ride 200 essential yesterday hdfc cc"}'
```

## Supported Expense Formats

- `"snacks food 200 essential yesterday"`
- `"haircut general 150 need 9 july hdfc cc"`
- `"uber ride 250 essential today"`
- `"coffee 50 want"`
- `"electricity bill 1200 essential icici cc"`

## Categories
- food, transport, general, entertainment, health
- bills, groceries, meds, clothing, gadgets, etc.

## Bank Accounts
- HDFC, ICICI CC 3009, INDUSIND CC 6421, HDFC CC 6409, IND

## Importance Levels
- essential, need, want, extra, investment

## Development

### Project Structure
```
├── main.py                 # FastAPI application entry point
├── config.py              # Configuration settings
├── models.py              # Pydantic models
├── routers/               # API route handlers
│   ├── chatbot_router.py  # Chatbot conversation endpoints
│   └── expense_router.py  # Expense processing endpoints
├── services/              # Business logic
│   ├── nlp_service.py     # Natural language processing
│   └── notion_service.py  # Notion API integration
└── requirements.txt       # Python dependencies
```

### Testing

Access the interactive API documentation at `http://localhost:8000/docs`

## License

MIT License
