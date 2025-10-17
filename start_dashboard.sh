#!/bin/bash

# VectorQuant Live Crypto Dashboard Startup Script
# This script starts both the FastAPI backend and Streamlit frontend

echo "🚀 Starting VectorQuant Live Crypto Dashboard..."
echo "=============================================="

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "❌ Virtual environment not found. Please run setup first:"
    echo "   python3 -m venv venv"
    echo "   source venv/bin/activate"
    echo "   pip install -r requirements.txt"
    exit 1
fi

# Activate virtual environment
source venv/bin/activate

# Check if required files exist
if [ ! -f "fastapi_server.py" ] || [ ! -f "streamlit_app.py" ]; then
    echo "❌ Required files not found. Please ensure fastapi_server.py and streamlit_app.py exist."
    exit 1
fi

echo "✅ Virtual environment activated"
echo "✅ Required files found"

# Function to cleanup background processes
cleanup() {
    echo ""
    echo "🛑 Shutting down services..."
    kill $FASTAPI_PID 2>/dev/null
    kill $STREAMLIT_PID 2>/dev/null
    echo "✅ Services stopped"
    exit 0
}

# Set up signal handlers
trap cleanup SIGINT SIGTERM

# Start FastAPI backend
echo "🔧 Starting FastAPI backend on http://127.0.0.1:8000"
uvicorn fastapi_server:app --reload --host 127.0.0.1 --port 8000 &
FASTAPI_PID=$!

# Wait a moment for FastAPI to start
sleep 3

# Start Streamlit frontend
echo "🎨 Starting Streamlit frontend on http://localhost:8501"
streamlit run streamlit_app.py --server.port 8501 &
STREAMLIT_PID=$!

echo ""
echo "🎉 Dashboard is starting up!"
echo "================================"
echo "📊 Streamlit Dashboard: http://localhost:8501"
echo "🔧 FastAPI Backend: http://127.0.0.1:8000"
echo "📚 API Documentation: http://127.0.0.1:8000/docs"
echo ""
echo "Press Ctrl+C to stop all services"

# Wait for processes
wait
