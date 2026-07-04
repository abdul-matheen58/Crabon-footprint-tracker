#!/bin/bash

# Carbon Footprint Platform — Quick Start Script for Linux/macOS
# This script sets up the entire project for development

set -e

echo "🌍 Carbon Footprint Platform — Setup Script"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# Check Python version
echo "✓ Checking Python version..."
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.13 or higher."
    exit 1
fi

PYTHON_VERSION=$(python3 --version | cut -d' ' -f2 | cut -d'.' -f1,2)
echo "  Found Python $PYTHON_VERSION"

# Check Node version
echo "✓ Checking Node.js version..."
if ! command -v node &> /dev/null; then
    echo "❌ Node.js is not installed. Please install Node.js 18 or higher."
    exit 1
fi

NODE_VERSION=$(node --version | cut -d'v' -f2 | cut -d'.' -f1)
echo "  Found Node.js v$(node --version | cut -d'v' -f2)"

# Setup Backend
echo ""
echo "📦 Setting up Backend..."
cd backend

# Create virtual environment
if [ ! -d "venv" ]; then
    echo "  Creating Python virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Install dependencies
echo "  Installing Python dependencies..."
pip install -q -r requirements.txt

# Create .env file if it doesn't exist
if [ ! -f ".env" ]; then
    echo "  Creating .env file..."
    cp .env.example .env
    echo "  ℹ️  .env file created. Review and update if needed."
fi

cd ..

# Setup Frontend
echo ""
echo "📦 Setting up Frontend..."
cd frontend

# Install dependencies
echo "  Installing Node dependencies..."
npm install --quiet

# Create .env.local file if it doesn't exist
if [ ! -f ".env.local" ]; then
    echo "  Creating .env.local file..."
    cp .env.local.example .env.local
    echo "  ℹ️  .env.local file created."
fi

cd ..

echo ""
echo "✅ Setup Complete!"
echo ""
echo "🚀 Next Steps:"
echo ""
echo "Terminal 1 - Start Backend:"
echo "  cd backend"
echo "  source venv/bin/activate"
echo "  uvicorn main:app --reload --host 0.0.0.0 --port 8000"
echo ""
echo "Terminal 2 - Start Frontend:"
echo "  cd frontend"
echo "  npm run dev"
echo ""
echo "🌐 Then open:"
echo "  Frontend:     http://localhost:3000"
echo "  Backend API:  http://localhost:8000/docs"
echo ""
