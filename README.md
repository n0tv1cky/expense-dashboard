# 💰 Expense Dashboard

A full-stack web application for comprehensive expense tracking and financial management, built with React, FastAPI, and PostgreSQL.

## 🌟 Features

### 📊 Dashboard Analytics

- **Category-wise Spending**: Visual breakdown of expenses by category
- **Monthly Trends**: Track spending patterns over time
- **Budget vs Actual**: Compare planned vs actual expenses
- **Financial Overview**: Total spending, monthly expenses, and earnings analysis

### 💼 Expense Management

- **CRUD Operations**: Create, read, update, and delete expenses
- **Smart Categorization**: Organize expenses into Essential, Needs, Wants, and Invest
- **Recurring Expenses**: Handle monthly and one-time expenses
- **Priority Levels**: Mark expenses as "Must Do" or "Essential"

### 🗑️ Trash & Recovery

- **Soft Delete**: Safely delete expenses with recovery option
- **Trash Bin**: View and manage deleted expenses
- **Restore Functionality**: Easily restore accidentally deleted items
- **Permanent Delete**: Option to permanently remove expenses

### 🎨 Modern UI/UX

- **Responsive Design**: Works perfectly on desktop and mobile
- **Clean Interface**: Minimalistic and intuitive design
- **Real-time Updates**: Instant feedback on all operations
- **Beautiful Charts**: Interactive visualizations with Recharts

## 🏗️ Architecture

```
expense-dashboard/
├── frontend/          # React + Vite + TailwindCSS
│   ├── src/
│   ├── App.jsx
│   ├── package.json
│   └── ...
├── backend/           # FastAPI + SQLAlchemy + PostgreSQL
│   ├── main.py
│   ├── models.py
│   ├── schemas.py
│   ├── requirements.txt
│   └── ...
└── README.md
```

## 🚀 Quick Start

### Prerequisites

- **Node.js** 16+ (for frontend)
- **Python** 3.8+ (for backend)
- **PostgreSQL** (optional, SQLite is used by default)

### 1. Clone the Repository

```bash
git clone <repository-url>
cd expense-dashboard
```

### 2. Backend Setup

```bash
cd backend

# Run the startup script (recommended)
./start.sh

# OR manual setup:
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
uvicorn main:app --reload
```

The backend will be available at `http://localhost:8000`

### 3. Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

The frontend will be available at `http://localhost:3000`

### 4. Access the Application

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs

## 📱 Usage

### Adding Expenses

1. Click the "+" button to add a new expense
2. Fill in the expense details:
   - **Description**: What the expense is for
   - **Category**: Essential, Needs, Wants, or Invest
   - **Budget**: Amount allocated
   - **Occurrence**: 1 for one-time, 12 for monthly
   - **Month**: Specific month (for one-time expenses)
   - **Priority**: Must Do, Essential, or leave empty

### Managing Expenses

- **Edit**: Click the edit icon on any expense row
- **Delete**: Click the trash icon to soft delete
- **Mark Done**: Check the checkbox to mark as completed
- **Restore**: Go to trash tab to restore deleted items

### Dashboard Insights

- View spending by category in the pie chart
- Track monthly trends in the line chart
- Monitor budget vs actual spending
- See financial summaries and projections

## 🔧 Configuration

### Environment Variables

**Backend (.env)**:

```env
DATABASE_URL=postgresql://username:password@localhost:5432/expenditure_db
DEBUG=True
SECRET_KEY=your-secret-key
ALLOWED_ORIGINS=http://localhost:3000,http://localhost:5173
```

**Frontend**:

```env
VITE_API_URL=http://localhost:8000
```

### Database Setup

**SQLite (Default)**:
No additional setup required - database file created automatically.

**PostgreSQL**:

1. Install PostgreSQL
2. Create database: `CREATE DATABASE expenditure_db;`
3. Update `DATABASE_URL` in `.env`

## 🧪 API Documentation

The FastAPI backend provides comprehensive API documentation:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### Key Endpoints

- `GET /expenses` - List all expenses
- `POST /expenses` - Create new expense
- `PUT /expenses/{id}` - Update expense
- `DELETE /expenses/{id}` - Delete expense
- `GET /dashboard` - Dashboard summary
- `GET /expenses/trash` - Trash bin contents

## 🎯 Future Enhancements

### 🤖 AI Integration (Planned)

- **Auto-categorization**: Automatically categorize expenses using AI
- **Spending Insights**: AI-powered spending pattern analysis
- **Budget Suggestions**: Smart budget recommendations
- **Local LLM Support**: Integration with Langchain VLLMOpenAI

### 📈 Advanced Analytics

- **Yearly Comparisons**: Compare spending across years
- **Forecasting**: Predict future expenses based on trends
- **Goal Tracking**: Set and track financial goals
- **Export Features**: Export data to Excel/PDF

### 🔐 User Management

- **Multi-user Support**: Individual user accounts
- **Authentication**: Login/logout functionality
- **Data Privacy**: User-specific data isolation

## 🛠️ Development

### Frontend Development

```bash
cd frontend
npm run dev     # Start development server
npm run build   # Build for production
npm run preview # Preview production build
```

### Backend Development

```bash
cd backend
source venv/bin/activate
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Database Migrations

```bash
cd backend
alembic revision --autogenerate -m "Migration description"
alembic upgrade head
```

## 📦 Deployment

### Backend Deployment

1. Set up PostgreSQL database
2. Update environment variables
3. Install dependencies: `pip install -r requirements.txt`
4. Run with Gunicorn: `gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker`

### Frontend Deployment

1. Build the project: `npm run build`
2. Deploy the `dist` folder to your hosting service
3. Configure environment variables for production API URL

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Commit changes: `git commit -m 'Add amazing feature'`
4. Push to branch: `git push origin feature/amazing-feature`
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

If you encounter any issues or have questions:

1. Check the [API Documentation](http://localhost:8000/docs)
2. Review the setup instructions above
3. Open an issue on GitHub

---

**Happy expense tracking! 💰📊**
