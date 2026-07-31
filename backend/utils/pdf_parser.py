"""
PDF Parser Utility
"""

from PyPDF2 import PdfReader
from pdf2image import convert_from_path
from typing import Optional, List, Dict
from pathlib import Path
import os


class PDFParser:
    """Parse and extract text from PDF files"""
    
    def __init__(self):
        self.temp_dir = Path("static/temp")
        self.temp_dir.mkdir(parents=True, exist_ok=True)
    
    async def extract_text_from_pdf(
        self,
        pdf_path: str,
        language: Optional[str] = None
    ) -> Dict:
        """
        Extract text from PDF file
        
        Args:
            pdf_path: Path to PDF file
            language: Optional language hint for OCR
        
        Returns:
            Dictionary with extracted text and page information
        """
        try:
            # First try to extract text directly (for text-based PDFs)
            text = self._extract_text_direct(pdf_path)
            
            if text.strip():
                # Successfully extracted text
                reader = PdfReader(pdf_path)
                page_texts = [page.extract_text() for page in reader.pages]
                
                return {
                    'text': text,
                    'pages': page_texts,
                    'page_count': len(reader.pages),
                    'method': 'direct'
                }
            else:
                # PDF is image-based, use OCR
                return await self._extract_text_ocr(pdf_path, language)
                
        except Exception as e:
            raise Exception(f"PDF parsing failed: {str(e)}")
    
    def _extract_text_direct(self, pdf_path: str) -> str:
        """Extract text directly from text-based PDF"""
        try:
            reader = PdfReader(pdf_path)
            text = ""
            
            for page in reader.pages:
                text += page.extract_text() + "\n"
            
            return text.strip()
            
        except Exception as e:
            return ""
    
    async def _extract_text_ocr(
        self,
        pdf_path: str,
        language: Optional[str] = None
    ) -> Dict:
        """Extract text from image-based PDF using OCR"""
        try:
            # Convert PDF pages to images
            images = convert_from_path(pdf_path)
            
            # Import OCR model here to avoid circular imports
            from models.ocr_model import OCRModel
            ocr_model = OCRModel()
            
            page_texts = []
            all_text = ""
            
            for i, image in enumerate(images):
                # Save image temporarily
                temp_image_path = self.temp_dir / f"page_{i}.png"
                image.save(temp_image_path)
                
                # Extract text using OCR
                page_text = await ocr_model.extract_text(
                    str(temp_image_path),
                    language=language
                )
                
                page_texts.append(page_text)
                all_text += page_text + "\n"
                
                # Clean up temp image
                temp_image_path.unlink()
            
            return {
                'text': all_text.strip(),
                'pages': page_texts,
                'page_count': len(images),
                'method': 'ocr'
            }
            
        except Exception as e:
            raise Exception(f"OCR extraction from PDF failed: {str(e)}")
    
    def get_pdf_info(self, pdf_path: str) -> Dict:
        """Get PDF metadata"""
        try:
            reader = PdfReader(pdf_path)
            
            return {
                'page_count': len(reader.pages),
                'metadata': reader.metadata,
                'is_encrypted': reader.is_encrypted
            }
            
        except Exception as e:
            return {'error': str(e)}
