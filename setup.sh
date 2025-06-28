#!/bin/bash

# Expense Dashboard Setup Script
echo "🚀 Setting up Expense Dashboard..."

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${BLUE}📦 Setting up Backend...${NC}"
cd backend

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo -e "${YELLOW}⚠️  Python 3 is required but not installed.${NC}"
    exit 1
fi

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "Creating Python virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Install Python dependencies
echo "Installing Python dependencies..."
pip install -r requirements.txt

# Create .env file if it doesn't exist
if [ ! -f ".env" ]; then
    echo "Creating .env file..."
    cp .env.example .env
    echo -e "${YELLOW}📝 Please edit backend/.env with your database configuration${NC}"
fi

echo -e "${GREEN}✅ Backend setup complete!${NC}"

# Setup Frontend
echo -e "${BLUE}📦 Setting up Frontend...${NC}"
cd ../frontend

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo -e "${YELLOW}⚠️  Node.js is required but not installed.${NC}"
    exit 1
fi

# Install Node.js dependencies
echo "Installing Node.js dependencies..."
npm install

echo -e "${GREEN}✅ Frontend setup complete!${NC}"

# Go back to root directory
cd ..

echo -e "${GREEN}🎉 Setup complete!${NC}"
echo ""
echo -e "${BLUE}To start the application:${NC}"
echo "1. Backend:  cd backend && ./start.sh"
echo "2. Frontend: cd frontend && npm run dev"
echo ""
echo -e "${BLUE}Access points:${NC}"
echo "• Frontend: http://localhost:3000"
echo "• Backend API: http://localhost:8000"
echo "• API Docs: http://localhost:8000/docs"
