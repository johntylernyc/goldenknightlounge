#!/bin/bash

# Golden Knight Lounge startup script for Replit

echo "Starting Golden Knight Lounge..."

# Install Python dependencies if needed
if [ ! -d "venv" ]; then
    echo "Creating Python virtual environment..."
    python -m venv venv
fi

source venv/bin/activate
pip install -r backend/requirements.txt

# Install Node dependencies if needed
if [ ! -d "frontend/node_modules" ]; then
    echo "Installing Node dependencies..."
    cd frontend && npm install && cd ..
fi

# Start both servers
echo "Starting backend server on port 5000..."
python backend/src/app.py &
BACKEND_PID=$!

echo "Starting frontend server on port 3000..."
cd frontend && npm start &
FRONTEND_PID=$!

# Keep the script running
wait $BACKEND_PID $FRONTEND_PID