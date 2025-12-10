#!/bin/bash

# BlackMamba Smart Farming - Web Application Setup Script
# This script helps set up and run the web applications

set -e

echo "🌱 BlackMamba Smart Farming - Web Application Setup"
echo "=================================================="
echo ""

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if we're in the right directory
if [ ! -f "package.json" ]; then
    echo "❌ Error: This script must be run from the frontend directory"
    echo "   Run: cd frontend && ./setup-web.sh"
    exit 1
fi

echo "📋 Step 1: Checking dependencies..."
# Check for Node.js
if ! command -v node &> /dev/null; then
    echo "❌ Node.js is not installed"
    echo "   Please install Node.js 16+ from https://nodejs.org/"
    exit 1
else
    echo -e "${GREEN}✓${NC} Node.js $(node --version) installed"
fi

# Check for npm
if ! command -v npm &> /dev/null; then
    echo "❌ npm is not installed"
    exit 1
else
    echo -e "${GREEN}✓${NC} npm $(npm --version) installed"
fi

echo ""
echo "📦 Step 2: Installing dependencies..."
npm install

echo ""
echo "⚙️  Step 3: Setting up environment variables..."
if [ ! -f ".env" ]; then
    if [ -f ".env.example" ]; then
        cp .env.example .env
        echo -e "${GREEN}✓${NC} Created .env file from .env.example"
        echo -e "${YELLOW}⚠${NC}  Please edit .env file if you need to change API URL or device ID"
    else
        echo "❌ .env.example not found"
        exit 1
    fi
else
    echo -e "${GREEN}✓${NC} .env file already exists"
fi

echo ""
echo "=================================================="
echo -e "${GREEN}✅ Setup complete!${NC}"
echo ""
echo "Available commands:"
echo "  npm start        - Start React development server (port 3000)"
echo "  npm run build    - Build production version"
echo "  npm test         - Run tests"
echo ""
echo "Simple HTML Dashboard:"
echo "  Open web/index.html in your browser for a simple dashboard"
echo "  Or use: python3 -m http.server 8080 --directory web"
echo ""
echo "To start the React app now, run:"
echo "  npm start"
echo ""
