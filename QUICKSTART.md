# 🚀 LitLingua Quick Start

Get up and running with LitLingua in 5 minutes!

## Prerequisites
- Python 3.9+
- Node.js 18+
- Tesseract OCR

## Setup Steps

### 1. Install Tesseract OCR

**Windows:**
```powershell
# Download from: https://github.com/UB-Mannheim/tesseract/wiki
# Install with Nepali & Sinhalese language packs
```

**macOS:**
```bash
brew install tesseract tesseract-lang
```

**Linux:**
```bash
sudo apt-get install tesseract-ocr tesseract-ocr-nep tesseract-ocr-sin
```

### 2. Clone & Setup

```bash
# Clone repository
git clone https://github.com/yourusername/LitLingua.git
cd LitLingua

# Backend setup
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt

# Frontend setup
cd ../frontend
npm install

# Configure environment
cp .env.example .env
```

### 3. Download AI Models

```bash
cd backend
python scripts/download_models.py
```

### 4. Run Application

**Terminal 1 - Backend:**
```bash
cd backend
uvicorn app:app --reload
```

**Terminal 2 - Frontend:**
```bash
cd frontend
npm run dev
```

### 5. Access Application

- **Frontend**: http://localhost:5173
- **API Docs**: http://localhost:8000/docs

## First Translation

1. Go to http://localhost:5173/translator
2. Select source language (Nepali or Sinhalese)
3. Upload an image or PDF
4. Click "Translate"
5. View results and export to PDF!

## Docker Alternative

```bash
docker-compose up --build
```

That's it! You're ready to translate! 🎉

For detailed setup, see [SETUP.md](SETUP.md)
