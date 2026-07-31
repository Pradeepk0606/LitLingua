"""
File Router - Handles file upload/download and PDF generation
"""

from fastapi import APIRouter, HTTPException, Form
from fastapi.responses import FileResponse
from typing import Optional
from pathlib import Path
import uuid
from datetime import datetime

from utils.pdf_parser import PDFParser
from utils.format_preserver import FormatPreserver
from scripts.export_to_pdf import PDFExporter

router = APIRouter()

# Initialize utilities
pdf_parser = PDFParser()
format_preserver = FormatPreserver()
pdf_exporter = PDFExporter()


@router.post("/export-pdf")
async def export_to_pdf(
    original_text: str = Form(...),
    translated_text: str = Form(...),
    source_language: str = Form(...),
    title: Optional[str] = Form(None),
    include_original: bool = Form(True),
    layout: str = Form('side-by-side')  # 'side-by-side' or 'sequential'
):
    """
    Export translation to formatted PDF
    
    Args:
        original_text: Original text
        translated_text: Translated text
        source_language: Source language code
        title: Optional document title
        include_original: Include original text in PDF
        layout: PDF layout style
    
    Returns:
        PDF file
    """
    try:
        # Generate unique filename
        pdf_id = str(uuid.uuid4())
        pdf_dir = Path("static/translated_pdfs")
        pdf_dir.mkdir(parents=True, exist_ok=True)
        pdf_path = pdf_dir / f"translation_{pdf_id}.pdf"
        
        # Create PDF
        await pdf_exporter.create_translation_pdf(
            original_text=original_text,
            translated_text=translated_text,
            output_path=str(pdf_path),
            source_language=source_language,
            title=title or f"Translation - {datetime.now().strftime('%Y-%m-%d')}",
            include_original=include_original,
            layout=layout
        )
        
        return FileResponse(
            path=pdf_path,
            media_type="application/pdf",
            filename=f"litlingua_translation_{pdf_id}.pdf",
            headers={
                "X-PDF-ID": pdf_id
            }
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"PDF export failed: {str(e)}")


@router.post("/export-docx")
async def export_to_docx(
    original_text: str = Form(...),
    translated_text: str = Form(...),
    source_language: str = Form(...),
    title: Optional[str] = Form(None)
):
    """
    Export translation to DOCX format
    """
    try:
        # Generate unique filename
        docx_id = str(uuid.uuid4())
        docx_dir = Path("static/translated_pdfs")
        docx_dir.mkdir(parents=True, exist_ok=True)
        docx_path = docx_dir / f"translation_{docx_id}.docx"
        
        # Create DOCX (implementation would use python-docx)
        # Placeholder for now
        
        return {
            "success": True,
            "message": "DOCX export feature coming soon",
            "file_id": docx_id
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"DOCX export failed: {str(e)}")


@router.post("/export-txt")
async def export_to_txt(
    text: str = Form(...),
    filename: Optional[str] = Form(None)
):
    """
    Export text to TXT file
    """
    try:
        # Generate unique filename
        txt_id = str(uuid.uuid4())
        txt_dir = Path("static/translated_pdfs")
        txt_dir.mkdir(parents=True, exist_ok=True)
        txt_path = txt_dir / f"{filename or 'translation'}_{txt_id}.txt"
        
        # Write text to file
        with open(txt_path, 'w', encoding='utf-8') as f:
            f.write(text)
        
        return FileResponse(
            path=txt_path,
            media_type="text/plain",
            filename=f"{filename or 'translation'}.txt"
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"TXT export failed: {str(e)}")


@router.get("/download/{file_id}")
async def download_file(file_id: str, file_type: str = 'pdf'):
    """
    Download previously generated file
    """
    try:
        file_dir = Path("static/translated_pdfs")
        file_path = file_dir / f"translation_{file_id}.{file_type}"
        
        if not file_path.exists():
            raise HTTPException(status_code=404, detail="File not found")
        
        media_types = {
            'pdf': 'application/pdf',
            'docx': 'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
            'txt': 'text/plain'
        }
        
        return FileResponse(
            path=file_path,
            media_type=media_types.get(file_type, 'application/octet-stream'),
            filename=f"litlingua_{file_id}.{file_type}"
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Download failed: {str(e)}")


@router.delete("/cleanup/{file_id}")
async def cleanup_exported_file(file_id: str):
    """Delete exported file"""
    try:
        file_dir = Path("static/translated_pdfs")
        deleted = False
        
        for ext in ['pdf', 'docx', 'txt']:
            file_path = file_dir / f"translation_{file_id}.{ext}"
            if file_path.exists():
                file_path.unlink()
                deleted = True
        
        if deleted:
            return {"success": True, "message": "File deleted successfully"}
        else:
            raise HTTPException(status_code=404, detail="File not found")
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Cleanup failed: {str(e)}")
