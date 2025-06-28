# Expense Dashboard Backend

A FastAPI-based backend for the Expense Dashboard application that provides comprehensive expense tracking and financial management capabilities.

## 🚀 Features

- **RESTful API** for expense management (CRUD operations)
- **Soft Delete** with trash/recycle bin functionality
- **Dashboard Analytics** with category-wise and monthly trends
- **PostgreSQL/SQLite Support** for data persistence
- **Database Migrations** with Alembic
- **User Settings** for yearly earning configuration
- **CORS Support** for frontend integration

## 📋 API Endpoints

### Expenses

- `GET /expenses` - Get all expenses (with optional filters)
- `GET /expenses/{id}` - Get specific expense
- `POST /expenses` - Create new expense
- `PUT /expenses/{id}` - Update expense
- `DELETE /expenses/{id}` - Soft delete expense
- `PUT /expenses/{id}/restore` - Restore deleted expense
- `PUT /expenses/{id}/toggle-done` - Toggle expense completion status
- `DELETE /expenses/{id}/permanent` - Permanently delete expense

### Trash Management

- `GET /expenses/trash` - Get all deleted expenses

### Dashboard

- `GET /dashboard` - Get dashboard summary with analytics

### User Settings

- `GET /settings` - Get user settings
- `PUT /settings` - Update user settings

### Utilities

- `GET /categories` - Get available categories and options
- `GET /health` - Health check endpoint

## 🛠️ Setup Instructions

### Prerequisites

- Python 3.8+
- PostgreSQL (optional, SQLite is used by default for development)

### Quick Start

1. **Clone and navigate to the backend directory:**

```bash
cd backend
```

2. **Run the startup script:**

```bash
./start.sh
```

This script will:

- Create a virtual environment
- Install dependencies
- Set up environment variables
- Start the FastAPI server

### Manual Setup

1. **Create virtual environment:**

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. **Install dependencies:**

```bash
pip install -r requirements.txt
```

3. **Environment Configuration:**

```bash
cp .env.example .env
# Edit .env with your database configuration
```

4. **Start the server:**

```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

## 🗄️ Database Configuration

### SQLite (Default for Development)

```env
DATABASE_URL=sqlite:///./expenditure.db
```

### PostgreSQL (Production)

```env
DATABASE_URL=postgresql://username:password@localhost:5432/expenditure_db
```

## 📊 Data Models

### Expense Model

- `id`: Unique identifier
- `done`: Completion status
- `expense_details`: Description of the expense
- `category`: Category (Essential, Needs, Wants, Invest)
- `occurrence`: Number of times per year (1 for one-time, 12 for monthly)
- `budget`: Budgeted amount
- `total_spend`: Calculated total spend (budget × occurrence)
- `month`: Specific month (for one-time expenses)
- `essential`: Priority level (Must Do, Essential, or empty)
- `deleted`: Soft delete flag
- `created_at`, `updated_at`, `deleted_at`: Timestamps

### User Settings Model

- `id`: Unique identifier
- `yearly_earning`: Annual income
- `created_at`, `updated_at`: Timestamps

## 🧪 Testing the API

### Using curl:

```bash
# Get all expenses
curl http://localhost:8000/expenses

# Create new expense
curl -X POST http://localhost:8000/expenses \
  -H "Content-Type: application/json" \
  -d '{
    "expense_details": "Test Expense",
    "category": "Needs",
    "budget": 1000,
    "occurrence": 12
  }'

# Get dashboard summary
curl http://localhost:8000/dashboard
```

### Using the interactive docs:

Visit `http://localhost:8000/docs` for Swagger UI documentation.

## 🔧 Development

### Database Migrations (Optional)

If you want to use Alembic for database migrations:

```bash
# Initialize Alembic (already done)
alembic init alembic

# Create a new migration
alembic revision --autogenerate -m "Create tables"

# Apply migrations
alembic upgrade head
```

### Adding New Features

1. Update models in `main.py` or `models.py`
2. Add corresponding Pydantic schemas in `schemas.py`
3. Implement API endpoints in `main.py`
4. Update documentation

## 🌐 Frontend Integration

The backend is configured to accept requests from:

- `http://localhost:3000` (React dev server)
- `http://localhost:5173` (Vite dev server)

Update CORS settings in `main.py` if needed.

## 📁 Project Structure

```
backend/
├── main.py              # Main FastAPI application
├── requirements.txt     # Python dependencies
├── .env.example        # Environment variables template
├── .env               # Environment variables (local)
├── start.sh           # Startup script
├── database.py        # Database configuration
├── models.py          # SQLAlchemy models
├── schemas.py         # Pydantic schemas
├── alembic.ini        # Alembic configuration
├── alembic/           # Database migrations
│   ├── env.py
│   ├── script.py.mako
│   └── versions/
└── README.md          # This file
```

## 🚀 Deployment

For production deployment:

1. Update environment variables in `.env`
2. Use PostgreSQL instead of SQLite
3. Set `DEBUG=False`
4. Use a production WSGI server like Gunicorn:

```bash
pip install gunicorn
gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is part of the Expense Dashboard application.
