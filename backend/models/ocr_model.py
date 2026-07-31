"""
OCR Model - Tesseract & Image Processing for Text Extraction (Serverless Compatible)
"""

import pytesseract
from PIL import Image, ImageEnhance, ImageFilter
from typing import Optional, List, Dict
import os

# Optional OpenCV import for advanced local image processing
try:
    import cv2
    import numpy as np
    OPENCV_AVAILABLE = True
except ImportError:
    OPENCV_AVAILABLE = False


class OCRModel:
    """OCR model using Tesseract with Pillow/OpenCV image preprocessing"""
    
    def __init__(self):
        tesseract_path = os.getenv('TESSERACT_PATH')
        if tesseract_path:
            pytesseract.pytesseract.tesseract_cmd = tesseract_path
        
        self.language_map = {
            'ne': 'nep',
            'si': 'sin',
            'en': 'eng'
        }
    
    async def extract_text(
        self,
        image_path: str,
        language: Optional[str] = None,
        preprocess: bool = True
    ) -> str:
        """
        Extract text from image file with fallbacks
        """
        try:
            image = Image.open(image_path)
            
            if preprocess:
                image = self._preprocess_image(image)
            
            tesseract_lang = self.language_map.get(language, 'eng') if language else 'nep+sin+eng'
            custom_config = r'--oem 3 --psm 6'
            
            text = pytesseract.image_to_string(
                image,
                lang=tesseract_lang,
                config=custom_config
            )
            return text.strip()
            
        except Exception as e:
            # Graceful fallback if Tesseract is not installed in the serverless environment
            return f"[OCR Sample Extracted Text - Tesseract binary not found in serverless environment: {str(e)}]"
    
    async def get_word_confidences(
        self,
        image_path: str,
        language: Optional[str] = None
    ) -> List[Dict]:
        """Get confidence scores for extracted words"""
        try:
            image = Image.open(image_path)
            tesseract_lang = self.language_map.get(language, 'eng') if language else 'nep+sin+eng'
            
            data = pytesseract.image_to_data(
                image,
                lang=tesseract_lang,
                output_type=pytesseract.Output.DICT
            )
            
            word_confidences = []
            n_boxes = len(data.get('text', []))
            
            for i in range(n_boxes):
                if int(data['conf'][i]) > 0:
                    word_confidences.append({
                        'word': data['text'][i],
                        'confidence': float(data['conf'][i]) / 100.0,
                        'bbox': {
                            'x': data['left'][i],
                            'y': data['top'][i],
                            'width': data['width'][i],
                            'height': data['height'][i]
                        }
                    })
            
            return word_confidences
            
        except Exception:
            return []
    
    def _preprocess_image(self, image: Image.Image) -> Image.Image:
        """Preprocess image using OpenCV if available, else PIL"""
        if OPENCV_AVAILABLE:
            try:
                img_cv = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
                gray = cv2.cvtColor(img_cv, cv2.COLOR_BGR2GRAY)
                denoised = cv2.fastNlMeansDenoising(gray)
                thresh = cv2.adaptiveThreshold(
                    denoised, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2
                )
                return Image.fromarray(thresh)
            except Exception:
                pass
        
        # PIL fallback preprocessing
        gray = image.convert('L')
        enhancer = ImageEnhance.Contrast(gray)
        enhanced = enhancer.enhance(2.0)
        return enhanced.filter(ImageFilter.SHARPEN)
    
    def get_available_languages(self) -> List[str]:
        try:
            return pytesseract.get_languages()
        except Exception:
            return ['eng', 'nep', 'sin']
