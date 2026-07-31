# LitLingua Setup Guide

Complete setup instructions for the LitLingua AI Translation Platform.

## 📋 Prerequisites

### Required Software
- **Python 3.9+** - [Download](https://www.python.org/downloads/)
- **Node.js 18+** - [Download](https://nodejs.org/)
- **Tesseract OCR** - Installation instructions below
- **Git** - [Download](https://git-scm.com/)

### Tesseract OCR Installation

#### Windows
1. Download installer from [UB-Mannheim](https://github.com/UB-Mannheim/tesseract/wiki)
2. Install with Nepali and Sinhalese language packs
3. Add to PATH or set `TESSERACT_PATH` in `.env`

#### macOS
```bash
brew install tesseract
brew install tesseract-lang  # Includes Nepali & Sinhalese
```

#### Linux (Ubuntu/Debian)
```bash
sudo apt-get update
sudo apt-get install tesseract-ocr
sudo apt-get install tesseract-ocr-nep  # Nepali
sudo apt-get install tesseract-ocr-sin  # Sinhalese
```

---

## 🚀 Quick Start

### Option 1: Automated Setup (Recommended)

#### Linux/macOS
```bash
chmod +x scripts/setup_local_env.sh
./scripts/setup_local_env.sh
```

#### Windows (PowerShell)
```powershell
# Run setup commands manually (see Manual Setup below)
```

### Option 2: Docker Setup

```bash
# Build and run with Docker Compose
docker-compose up --build

# Access the application
# Frontend: http://localhost:5173
# Backend API: http://localhost:8000
# API Docs: http://localhost:8000/docs
```

---

## 🔧 Manual Setup

### 1. Clone Repository
```bash
git clone https://github.com/yourusername/LitLingua.git
cd LitLingua
```

### 2. Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Linux/macOS:
source venv/bin/activate

# Install dependencies
pip install --upgrade pip
pip install -r requirements.txt

# Create .env file
cp ../.env.example ../.env

# Edit .env and configure settings
# Especially set TESSERACT_PATH if needed
```

### 3. Download AI Models

```bash
# Download translation models for offline use
python scripts/download_models.py
```

This will download:
- MarianMT Nepali-English model (~300MB)
- MarianMT Sinhalese-English model (~300MB)
- M2M100 multilingual model (~1.5GB)

**Note:** First run will take time to download models. Subsequent runs will use cached models.

### 4. Frontend Setup

```bash
cd ../frontend

# Install dependencies
npm install

# Optional: Install additional dependencies
npm install --legacy-peer-deps  # If you encounter peer dependency issues
```

### 5. Database Initialization

The SQLite database will be created automatically on first run. No manual setup needed.

---

## ▶️ Running the Application

### Development Mode

#### Terminal 1 - Backend
```bash
cd backend
source venv/bin/activate  # Windows: venv\Scripts\activate
uvicorn app:app --reload --host 0.0.0.0 --port 8000
```

#### Terminal 2 - Frontend
```bash
cd frontend
npm run dev
```

### Access Points
- **Frontend**: http://localhost:5173
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

---

## 🧪 Testing

### Backend Tests
```bash
cd backend
pytest tests/ -v
pytest tests/ --cov=. --cov-report=html
```

### Frontend Tests
```bash
cd frontend
npm test
npm run test:coverage
```

---

## 🔒 Environment Configuration

Edit `.env` file with your settings:

```env
# Backend
BACKEND_HOST=0.0.0.0
BACKEND_PORT=8000
DEBUG=True

# Database
DATABASE_URL=sqlite:///./litlingua.db

# CORS
CORS_ORIGINS=http://localhost:5173,http://localhost:3000

# Tesseract (Windows example)
TESSERACT_PATH=C:/Program Files/Tesseract-OCR/tesseract.exe

# Models
MODEL_CACHE_DIR=./backend/data/offline_models

# Features
ENABLE_OFFLINE_MODE=True
ENABLE_RETRAINING=True
```

---

## 📦 Production Deployment

### Build Frontend
```bash
cd frontend
npm run build
```

### Run Backend in Production
```bash
cd backend
uvicorn app:app --host 0.0.0.0 --port 8000 --workers 4
```

### Using Docker
```bash
docker-compose -f docker-compose.prod.yml up -d
```

---

## 🐛 Troubleshooting

### Issue: Tesseract not found
**Solution:** 
- Ensure Tesseract is installed
- Set `TESSERACT_PATH` in `.env`
- Verify with: `tesseract --version`

### Issue: Model download fails
**Solution:**
- Check internet connection
- Ensure sufficient disk space (~2GB)
- Try downloading models manually from HuggingFace

### Issue: Port already in use
**Solution:**
```bash
# Change port in .env or use different port
uvicorn app:app --port 8001
npm run dev -- --port 5174
```

### Issue: CORS errors
**Solution:**
- Add your frontend URL to `CORS_ORIGINS` in `.env`
- Restart backend server

### Issue: Module not found
**Solution:**
```bash
# Backend
pip install -r requirements.txt

# Frontend
rm -rf node_modules package-lock.json
npm install
```

---

## 📱 PWA Installation

The frontend is a Progressive Web App (PWA):

1. Open http://localhost:5173 in Chrome/Edge
2. Click the install icon in the address bar
3. Use LitLingua as a standalone app

---

## 🔄 Updating

```bash
git pull origin main

# Update backend
cd backend
pip install -r requirements.txt

# Update frontend
cd ../frontend
npm install

# Restart services
```

---

## 📊 Performance Tips

1. **Use Offline Mode**: Download models once, use without internet
2. **GPU Acceleration**: Install CUDA for faster translation (optional)
3. **Batch Processing**: Use batch endpoints for multiple translations
4. **Caching**: Enable browser caching for static assets

---

## 🆘 Getting Help

- **Documentation**: Check `/docs` folder
- **API Reference**: http://localhost:8000/docs
- **Issues**: [GitHub Issues](https://github.com/yourusername/LitLingua/issues)
- **Contributing**: See [CONTRIBUTING.md](docs/CONTRIBUTING.md)

---

## ✅ Verification Checklist

After setup, verify everything works:

- [ ] Backend server starts without errors
- [ ] Frontend loads at http://localhost:5173
- [ ] Can upload an image/PDF
- [ ] OCR extracts text successfully
- [ ] Translation works
- [ ] Can export to PDF
- [ ] Text-to-speech works
- [ ] Settings save correctly
- [ ] History is saved

---

## 🎉 You're Ready!

LitLingua is now set up and ready to use. Start translating Nepali and Sinhalese text to English with AI-powered accuracy!

For advanced features and customization, refer to the full documentation in the `/docs` folder.
