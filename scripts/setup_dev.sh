#!/bin/bash

# Development setup script for Product Management API

set -e

echo "🚀 Setting up Product Management API development environment..."

# Check if running in project root
if [ ! -f "requirements.txt" ]; then
    echo "❌ Please run this script from the project root directory"
    exit 1
fi

# Check if Python 3 is available
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.11+ first."
    exit 1
fi

# Check Python version
PYTHON_VERSION=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
REQUIRED_VERSION="3.11"
echo "📦 Python version: $PYTHON_VERSION"

# Validate minimum Python version
if python3 -c "import sys; exit(0 if sys.version_info >= (3,11) else 1)"; then
    echo "✅ Python version meets requirements (>= $REQUIRED_VERSION)"
else
    echo "❌ Python $PYTHON_VERSION is too old. Please install Python $REQUIRED_VERSION or newer."
    exit 1
fi

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "🔧 Creating virtual environment..."
    python3 -m venv venv
    echo "✅ Virtual environment created at: venv/"
else
    echo "✅ Virtual environment already exists at: venv/"
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "📦 Upgrading pip..."
pip install --upgrade pip

# Install dependencies
echo "📦 Installing dependencies..."
pip install -r requirements.txt

# Copy environment file if it doesn't exist
if [ ! -f ".env" ]; then
    echo "📄 Creating .env file from template..."
    cp env.example .env
    echo "✅ .env file created. Please edit it with your configuration."
else
    echo "✅ .env file already exists."
fi

echo ""
# Test installation
echo "🧪 Testing installation..."
if ./venv/bin/python -c "import fastapi, sqlalchemy, pydantic" 2>/dev/null; then
    echo "✅ All dependencies installed successfully"
else
    echo "⚠️  Some dependencies may not be installed correctly"
fi

echo ""
echo "🎉 Development environment setup complete!"
echo ""
echo "📋 Next steps:"
echo "1. Edit .env file with your database configuration"
echo "2. Activate the virtual environment: source venv/bin/activate"
echo "3. Set up database: make migrate"
echo "4. Run tests: make test"
echo "5. Run the application: make run"
echo "6. Or use Docker: make docker-run"
echo ""
echo "🔗 Useful commands:"
echo "  make help          - Show all available commands"
echo "  make run           - Run application locally"
echo "  make test          - Run tests"
echo "  make docker-run    - Run with Docker"
echo "" 