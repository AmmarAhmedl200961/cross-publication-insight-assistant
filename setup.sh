#!/bin/bash

echo "🚀 Publication Assistant Quick Setup"
echo "==================================="

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    if ! command -v python &> /dev/null; then
        echo "❌ Python is not installed"
        echo "Please install Python 3.8+ and try again"
        exit 1
    else
        PYTHON_CMD="python"
    fi
else
    PYTHON_CMD="python3"
fi

# Check Python version
PYTHON_VERSION=$($PYTHON_CMD --version 2>&1 | cut -d' ' -f2)
echo "✅ Using Python $PYTHON_VERSION"

# Run setup
$PYTHON_CMD setup.py

echo ""
echo "🎯 Setup completed!"
echo ""
echo "To get started:"
echo "1. Edit .env file with your API keys"
echo "2. Run: source venv/bin/activate"
echo "3. Run: python main.py --repo-url \"https://github.com/owner/repo\""
echo ""
