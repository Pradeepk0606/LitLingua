"""
LitLingua - AI-Powered Multilingual Translation Platform
Main FastAPI Application Entry Point
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
import os
from pathlib import Path

from routers import ocr_router, translate_router, audio_router, file_router, feedback_router
from database.db_config import engine, Base
from utils.language_detection import LanguageDetector

# Create necessary directories
STATIC_DIR = Path("static")
UPLOAD_DIR = STATIC_DIR / "uploaded_files"
TRANSLATED_DIR = STATIC_DIR / "translated_pdfs"
AUDIO_DIR = STATIC_DIR / "audio"

for directory in [STATIC_DIR, UPLOAD_DIR, TRANSLATED_DIR, AUDIO_DIR]:
    directory.mkdir(parents=True, exist_ok=True)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup and shutdown events"""
    # Startup
    print("🚀 Starting LitLingua Backend...")
    
    # Create database tables
    Base.metadata.create_all(bind=engine)
    print("✅ Database initialized")
    
    # Initialize language detector
    try:
        detector = LanguageDetector()
        app.state.language_detector = detector
        print("✅ Language detector loaded")
    except Exception as e:
        print(f"⚠️  Language detector initialization warning: {e}")
    
    print("✅ LitLingua Backend is ready!")
    
    yield
    
    # Shutdown
    print("👋 Shutting down LitLingua Backend...")


# Initialize FastAPI app
app = FastAPI(
    title="LitLingua API",
    description="AI-Powered Multilingual Translation Platform - Nepali & Sinhalese to English",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)

# CORS Configuration
origins = os.getenv("CORS_ORIGINS", "http://localhost:5173,http://localhost:3000").split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Include routers
app.include_router(ocr_router.router, prefix="/api/ocr", tags=["OCR"])
app.include_router(translate_router.router, prefix="/api/translate", tags=["Translation"])
app.include_router(audio_router.router, prefix="/api/audio", tags=["Audio"])
app.include_router(file_router.router, prefix="/api/files", tags=["Files"])
app.include_router(feedback_router.router, prefix="/api/feedback", tags=["Feedback"])


@app.get("/")
async def root():
    """Root endpoint - API health check"""
    return {
        "message": "Welcome to LitLingua API",
        "version": "1.0.0",
        "status": "online",
        "features": {
            "ocr": True,
            "translation": True,
            "audio": True,
            "offline_mode": True,
            "retraining": os.getenv("ENABLE_RETRAINING", "True") == "True"
        }
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "database": "connected",
        "models": "loaded"
    }


@app.get("/api/languages")
async def get_supported_languages():
    """Get list of supported languages"""
    return {
        "source_languages": [
            {"code": "ne", "name": "Nepali", "script": "Devanagari"},
            {"code": "si", "name": "Sinhalese", "script": "Sinhala"}
        ],
        "target_languages": [
            {"code": "en", "name": "English", "script": "Latin"}
        ]
    }


@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    """Custom HTTP exception handler"""
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": exc.detail,
            "status_code": exc.status_code
        }
    )


@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    """General exception handler"""
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal server error",
            "detail": str(exc) if os.getenv("DEBUG") == "True" else "An unexpected error occurred"
        }
    )


if __name__ == "__main__":
    import uvicorn
    
    port = int(os.getenv("BACKEND_PORT", 8000))
    host = os.getenv("BACKEND_HOST", "0.0.0.0")
    
    uvicorn.run(
        "app:app",
        host=host,
        port=port,
        reload=os.getenv("DEBUG", "True") == "True",
        log_level="info"
    )
