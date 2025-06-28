#!/bin/bash

# Expense Dashboard Backend Startup Script

echo "🚀 Starting Expense Dashboard Backend..."

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "📚 Installing dependencies..."
pip install -r requirements.txt

# Create .env file if it doesn't exist
if [ ! -f ".env" ]; then
    echo "⚙️ Creating .env file..."
    cp .env.example .env
    echo "✏️ Please edit .env file with your database configuration"
fi

# Run database migrations (if using Alembic)
# echo "🗄️ Running database migrations..."
# alembic upgrade head

echo "🎯 Starting FastAPI server..."
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
