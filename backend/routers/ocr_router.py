"""
OCR Router - Handles text extraction from images and PDFs
"""

from fastapi import APIRouter, UploadFile, File, HTTPException, Form
from fastapi.responses import JSONResponse
from typing import Optional
import os
from pathlib import Path
import uuid

from models.ocr_model import OCRModel
from utils.pdf_parser import PDFParser
from utils.language_detection import LanguageDetector

router = APIRouter()

# Initialize models
ocr_model = OCRModel()
pdf_parser = PDFParser()
language_detector = LanguageDetector()


@router.post("/extract")
async def extract_text(
    file: UploadFile = File(...),
    language: Optional[str] = Form(None),
    detect_language: bool = Form(True)
):
    """
    Extract text from uploaded image or PDF file
    
    Args:
        file: Image (JPG, PNG) or PDF file
        language: Optional language hint ('ne' for Nepali, 'si' for Sinhalese)
        detect_language: Auto-detect language if True
    
    Returns:
        Extracted text, detected language, and confidence scores
    """
    try:
        # Validate file type
        allowed_extensions = {'.jpg', '.jpeg', '.png', '.pdf'}
        file_ext = Path(file.filename).suffix.lower()
        
        if file_ext not in allowed_extensions:
            raise HTTPException(
                status_code=400,
                detail=f"Unsupported file type. Allowed: {', '.join(allowed_extensions)}"
            )
        
        # Save uploaded file temporarily
        upload_dir = Path("static/uploaded_files")
        upload_dir.mkdir(parents=True, exist_ok=True)
        
        file_id = str(uuid.uuid4())
        temp_file_path = upload_dir / f"{file_id}{file_ext}"
        
        with open(temp_file_path, "wb") as buffer:
            content = await file.read()
            buffer.write(content)
        
        # Extract text based on file type
        if file_ext == '.pdf':
            # Extract text from PDF
            extracted_data = await pdf_parser.extract_text_from_pdf(
                str(temp_file_path),
                language=language
            )
            extracted_text = extracted_data['text']
            page_texts = extracted_data.get('pages', [])
        else:
            # Extract text from image using OCR
            extracted_text = await ocr_model.extract_text(
                str(temp_file_path),
                language=language
            )
            page_texts = [extracted_text]
        
        # Detect language if requested
        detected_language = None
        language_confidence = 0.0
        
        if detect_language and extracted_text.strip():
            lang_result = language_detector.detect(extracted_text)
            detected_language = lang_result['language']
            language_confidence = lang_result['confidence']
        
        # Get word-level confidence scores
        word_confidences = await ocr_model.get_word_confidences(
            str(temp_file_path),
            language=language or detected_language
        )
        
        return JSONResponse(content={
            "success": True,
            "file_id": file_id,
            "filename": file.filename,
            "text": extracted_text,
            "detected_language": detected_language,
            "language_confidence": language_confidence,
            "word_count": len(extracted_text.split()),
            "character_count": len(extracted_text),
            "pages": len(page_texts),
            "page_texts": page_texts,
            "word_confidences": word_confidences,
            "file_path": str(temp_file_path)
        })
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"OCR extraction failed: {str(e)}")


@router.post("/extract-batch")
async def extract_text_batch(
    files: list[UploadFile] = File(...),
    language: Optional[str] = Form(None)
):
    """
    Extract text from multiple files in batch
    """
    results = []
    
    for file in files:
        try:
            result = await extract_text(file, language=language)
            results.append({
                "filename": file.filename,
                "success": True,
                "data": result
            })
        except Exception as e:
            results.append({
                "filename": file.filename,
                "success": False,
                "error": str(e)
            })
    
    return JSONResponse(content={
        "total_files": len(files),
        "successful": sum(1 for r in results if r['success']),
        "failed": sum(1 for r in results if not r['success']),
        "results": results
    })


@router.get("/languages")
async def get_ocr_languages():
    """Get list of supported OCR languages"""
    return {
        "supported_languages": [
            {
                "code": "ne",
                "name": "Nepali",
                "script": "Devanagari",
                "tesseract_code": "nep"
            },
            {
                "code": "si",
                "name": "Sinhalese",
                "script": "Sinhala",
                "tesseract_code": "sin"
            },
            {
                "code": "en",
                "name": "English",
                "script": "Latin",
                "tesseract_code": "eng"
            }
        ]
    }


@router.delete("/cleanup/{file_id}")
async def cleanup_file(file_id: str):
    """Delete temporary uploaded file"""
    try:
        upload_dir = Path("static/uploaded_files")
        
        # Find and delete file with matching ID
        for file_path in upload_dir.glob(f"{file_id}.*"):
            file_path.unlink()
            return {"success": True, "message": "File deleted successfully"}
        
        raise HTTPException(status_code=404, detail="File not found")
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Cleanup failed: {str(e)}")
