# 🌍 LitLingua - AI-Powered Multilingual Translation Platform

![LitLingua Banner](docs/architecture_diagram.png)

**LitLingua** is a cutting-edge, offline-capable AI translation platform that converts printed Nepali and Sinhalese text into English using advanced OCR and neural machine translation models.

## ✨ Key Features

### 🎯 Core Capabilities
- **Smart OCR Extraction** - Extract text from images, PDFs, and scanned documents
- **AI-Powered Translation** - MarianMT/M2M100 models for accurate Nepali/Sinhalese → English translation
- **Offline Mode** - Fully functional without internet connectivity
- **Document Preservation** - Maintains original formatting in translated PDFs
- **Speech Integration** - Text-to-speech and voice input support

### 🚀 Innovation Features
- **Translation Confidence Heatmap** - Visual indicators for uncertain translations
- **AI Co-Learning** - System improves from user corrections
- **Bilingual Text Alignment** - Side-by-side comparison for educational use
- **Custom Glossary Management** - Build domain-specific dictionaries
- **Explain Translation Mode** - AI explains translation decisions

## 🛠️ Tech Stack

### Frontend
- **React 18** + **Vite** - Lightning-fast development
- **Framer Motion** - Smooth animations
- **TailwindCSS** - Modern glassmorphism UI
- **PWA Support** - Offline-first progressive web app

### Backend
- **FastAPI** - High-performance Python API
- **Tesseract OCR** - Multi-language text extraction
- **HuggingFace Transformers** - MarianMT/M2M100 translation models
- **SQLite** - Lightweight database for history and glossary
- **gTTS/Whisper** - Text-to-speech capabilities

## 📦 Installation

### Prerequisites
- Python 3.9+
- Node.js 18+
- Tesseract OCR
- Git

### Quick Start

```bash
# Clone the repository
git clone https://github.com/yourusername/LitLingua.git
cd LitLingua

# Run setup script
bash scripts/setup_local_env.sh

# Or manual setup:

# Backend setup
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
python scripts/download_models.py

# Frontend setup
cd ../frontend
npm install

# Start development servers
# Terminal 1 - Backend
cd backend
uvicorn app:app --reload --host 0.0.0.0 --port 8000

# Terminal 2 - Frontend
cd frontend
npm run dev
```

### Docker Setup

```bash
# Build and run with Docker Compose
docker-compose up --build

# Access the app at http://localhost:5173
```

## 🎨 Project Structure

```
LitLingua/
├── frontend/          # React + Vite frontend
│   ├── src/
│   │   ├── components/   # Reusable UI components
│   │   ├── pages/        # Main application pages
│   │   ├── hooks/        # Custom React hooks
│   │   └── context/      # Global state management
│   └── public/           # Static assets & PWA config
│
├── backend/           # FastAPI backend
│   ├── routers/          # API endpoints
│   ├── models/           # ML model integrations
│   ├── utils/            # Helper modules
│   ├── database/         # Database models
│   └── data/             # Offline models & user data
│
├── docs/              # Documentation
├── scripts/           # Utility scripts
└── docker-compose.yml # Container orchestration
```

## 🔧 Configuration

Copy `.env.example` to `.env` and configure:

```env
# Backend
BACKEND_PORT=8000
DATABASE_URL=sqlite:///./litlingua.db

# Models
TESSERACT_PATH=/usr/bin/tesseract
MODEL_CACHE_DIR=./backend/data/offline_models

# Features
ENABLE_OFFLINE_MODE=True
ENABLE_RETRAINING=True
```

## 📖 Usage

### 1. Upload Document
- Drag & drop images or PDFs
- Supports JPG, PNG, PDF formats

### 2. OCR Extraction
- Automatic language detection (Nepali/Sinhalese)
- Real-time text extraction with progress indicator

### 3. Translation
- AI-powered translation to English
- Editable dual-pane view
- Confidence scores for each segment

### 4. Export & Save
- Download as PDF, DOCX, or TXT
- Save to translation history
- Add custom glossary entries

## 🧪 Testing

```bash
# Backend tests
cd backend
pytest tests/

# Frontend tests
cd frontend
npm run test
```

## 🌐 API Documentation

Once the backend is running, visit:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 🎯 Roadmap

- [ ] Support for more languages (Hindi, Tamil, Bengali)
- [ ] Real-time collaborative translation
- [ ] Mobile apps (iOS/Android)
- [ ] Advanced neural adaptation with RLHF
- [ ] Integration with translation memory systems

## 🤝 Contributing

We welcome contributions! Please see [CONTRIBUTING.md](docs/CONTRIBUTING.md) for guidelines.

## 📄 License

MIT License - see [LICENSE](LICENSE) for details.

## 🏆 Hackathon Recognition

Built for **AI for Language & Inclusion** theme - empowering multilingual communication through privacy-first, offline-capable AI technology.

## 📞 Support

- **Documentation**: [docs/api_reference.md](docs/api_reference.md)
- **Issues**: [GitHub Issues](https://github.com/yourusername/LitLingua/issues)
- **Email**: support@litlingua.ai

---

**Made with ❤️ for global language accessibility**
