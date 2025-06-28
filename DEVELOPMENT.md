# 🛠️ Development Guide

This guide provides detailed instructions for developers working on the Expense Dashboard project.

## 🏗️ Project Structure

```
expense-dashboard/
├── backend/                 # FastAPI Backend
│   ├── main.py             # Main FastAPI application
│   ├── models.py           # SQLAlchemy database models
│   ├── schemas.py          # Pydantic schemas for API
│   ├── database.py         # Database configuration
│   ├── requirements.txt    # Python dependencies
│   ├── .env.example       # Environment variables template
│   ├── start.sh           # Backend startup script
│   ├── alembic.ini        # Alembic configuration
│   └── alembic/           # Database migrations
├── frontend/               # React Frontend
│   ├── src/
│   │   ├── main.jsx       # React entry point
│   │   ├── index.css      # Global styles
│   │   └── api.js         # API service functions
│   ├── App.jsx            # Main React component
│   ├── package.json       # Node.js dependencies
│   ├── vite.config.js     # Vite configuration
│   ├── tailwind.config.js # Tailwind CSS configuration
│   └── index.html         # HTML template
├── setup.sh               # Project setup script
└── README.md              # Main documentation
```

## 🚀 Getting Started

### 1. Initial Setup

```bash
# Clone the repository
git clone <repository-url>
cd expense-dashboard

# Run the setup script
./setup.sh
```

### 2. Development Workflow

**Start Backend:**

```bash
cd backend
source venv/bin/activate
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

**Start Frontend:**

```bash
cd frontend
npm run dev
```

### 3. API Testing

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 🔧 Backend Development

### Adding New Models

1. Add model class in `models.py`
2. Create Pydantic schemas in `schemas.py`
3. Generate migration: `alembic revision --autogenerate -m "Description"`
4. Apply migration: `alembic upgrade head`

### Adding New Endpoints

1. Define route in `main.py`
2. Add corresponding schemas if needed
3. Test endpoint in Swagger UI
4. Update frontend API service

### Database Operations

```bash
# Create migration
alembic revision --autogenerate -m "Add new table"

# Apply migrations
alembic upgrade head

# Downgrade to previous migration
alembic downgrade -1

# View migration history
alembic history
```

### Environment Configuration

```env
# Development
DATABASE_URL=sqlite:///./expenditure.db
DEBUG=True

# Production
DATABASE_URL=postgresql://user:pass@localhost:5432/expenditure_db
DEBUG=False
```

## 🎨 Frontend Development

### Component Structure

- **App.jsx**: Main application component
- **Components**: Reusable UI components
- **Services**: API communication logic
- **Styles**: Tailwind CSS classes and custom styles

### Adding New Features

1. Create component or update existing one
2. Add API service functions in `src/api.js`
3. Update state management logic
4. Test in browser

### Styling Guidelines

- Use Tailwind CSS utility classes
- Follow existing design patterns
- Ensure responsive design
- Use custom CSS classes for complex styles

### State Management

Currently using React's built-in `useState` and `useEffect`. For complex state, consider:

- React Context API
- Redux Toolkit
- Zustand

## 🧪 Testing

### Backend Testing

```bash
# Install test dependencies
pip install pytest pytest-asyncio httpx

# Run tests
pytest
```

### Frontend Testing

```bash
# Install test dependencies
npm install --save-dev @testing-library/react @testing-library/jest-dom vitest

# Run tests
npm test
```

## 📦 Deployment

### Backend Deployment

1. **Production Environment Setup:**

```bash
# Install dependencies
pip install -r requirements.txt

# Set environment variables
export DATABASE_URL="postgresql://user:pass@localhost:5432/expenditure_db"
export DEBUG=False

# Run with Gunicorn
pip install gunicorn
gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker
```

2. **Docker Deployment:**

```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["gunicorn", "main:app", "-w", "4", "-k", "uvicorn.workers.UvicornWorker", "--bind", "0.0.0.0:8000"]
```

### Frontend Deployment

```bash
# Build for production
npm run build

# Deploy dist/ folder to your hosting service
# Update VITE_API_URL for production
```

## 🔍 Debugging

### Backend Debugging

- Use FastAPI's automatic API docs at `/docs`
- Check logs in terminal output
- Use Python debugger: `import pdb; pdb.set_trace()`
- Enable SQLAlchemy logging for database queries

### Frontend Debugging

- Use browser developer tools
- Check Network tab for API calls
- Use React Developer Tools extension
- Console.log for debugging state changes

## 🔐 Security Considerations

### Backend Security

- Input validation with Pydantic
- SQL injection prevention with SQLAlchemy ORM
- CORS configuration for allowed origins
- Environment variables for sensitive data

### Frontend Security

- Input sanitization
- Secure API communication (HTTPS in production)
- Environment variables for configuration

## 📋 Code Standards

### Python (Backend)

- Follow PEP 8 style guide
- Use type hints where appropriate
- Document functions with docstrings
- Keep functions small and focused

### JavaScript/React (Frontend)

- Use ES6+ features
- Follow React best practices
- Use meaningful component and variable names
- Keep components small and reusable

### Git Workflow

```bash
# Create feature branch
git checkout -b feature/new-feature

# Make changes and commit
git add .
git commit -m "Add new feature: description"

# Push and create pull request
git push origin feature/new-feature
```

## 🆘 Common Issues

### Backend Issues

- **Database connection errors**: Check DATABASE_URL in .env
- **Import errors**: Ensure virtual environment is activated
- **Port conflicts**: Change port in uvicorn command

### Frontend Issues

- **Build errors**: Check Node.js version compatibility
- **API connection**: Verify backend is running and CORS is configured
- **Module not found**: Run `npm install` to install dependencies

## 📚 Additional Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [React Documentation](https://react.dev/)
- [Tailwind CSS Documentation](https://tailwindcss.com/docs)
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)
- [Vite Documentation](https://vitejs.dev/)

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Follow code standards
4. Write tests if applicable
5. Submit pull request with clear description

---

Happy coding! 🚀
