#!/bin/bash

# Expense Tracker Development Server Startup Script

echo "🚀 Starting Expense Tracker Development Environment..."
echo ""

# Check if Python backend is running
if ! curl -s http://localhost:8000/health > /dev/null; then
    echo "📡 Starting Backend Server..."
    cd ../
    python main.py &
    BACKEND_PID=$!
    echo "Backend started with PID: $BACKEND_PID"
    sleep 3
else
    echo "✅ Backend server is already running on http://localhost:8000"
fi

# Start React frontend
echo "⚛️  Starting React Frontend..."
cd frontend-react
npm run dev &
FRONTEND_PID=$!

echo ""
echo "🎉 Development servers started!"
echo "📊 Backend API:  http://localhost:8000"
echo "💻 Frontend:     http://localhost:5173" 
echo "📚 API Docs:     http://localhost:8000/docs"
echo ""
echo "Press Ctrl+C to stop both servers"

# Wait for Ctrl+C
trap 'echo ""; echo "🛑 Stopping servers..."; kill $BACKEND_PID $FRONTEND_PID 2>/dev/null; exit' INT
wait
