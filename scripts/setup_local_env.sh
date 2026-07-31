#!/bin/bash

# LitLingua Local Environment Setup Script

echo "🚀 Setting up LitLingua local environment..."

# Check for Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.9 or higher."
    exit 1
fi

# Check for Node.js
if ! command -v node &> /dev/null; then
    echo "❌ Node.js is not installed. Please install Node.js 18 or higher."
    exit 1
fi

# Check for Tesseract
if ! command -v tesseract &> /dev/null; then
    echo "⚠️  Tesseract OCR is not installed."
    echo "Please install Tesseract with Nepali and Sinhalese language packs:"
    echo "  Ubuntu/Debian: sudo apt-get install tesseract-ocr tesseract-ocr-nep tesseract-ocr-sin"
    echo "  macOS: brew install tesseract tesseract-lang"
    echo "  Windows: Download from https://github.com/UB-Mannheim/tesseract/wiki"
fi

echo ""
echo "📦 Setting up backend..."
cd backend

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install Python dependencies
pip install --upgrade pip
pip install -r requirements.txt

# Create .env file
if [ ! -f ../.env ]; then
    cp ../.env.example ../.env
    echo "✅ Created .env file from template"
fi

# Download AI models
echo ""
echo "📥 Downloading AI models (this may take a while)..."
python scripts/download_models.py

cd ..

echo ""
echo "📦 Setting up frontend..."
cd frontend

# Install Node dependencies
npm install

cd ..

echo ""
echo "✨ Setup complete!"
echo ""
echo "To start the application:"
echo ""
echo "1. Start backend (in one terminal):"
echo "   cd backend"
echo "   source venv/bin/activate  # On Windows: venv\\Scripts\\activate"
echo "   uvicorn app:app --reload --host 0.0.0.0 --port 8000"
echo ""
echo "2. Start frontend (in another terminal):"
echo "   cd frontend"
echo "   npm run dev"
echo ""
echo "3. Open http://localhost:5173 in your browser"
echo ""
echo "🎉 Happy translating with LitLingua!"
