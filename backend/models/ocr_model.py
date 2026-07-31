"""
OCR Model - Tesseract integration for text extraction
"""

import pytesseract
from PIL import Image
import cv2
import numpy as np
from typing import Optional, List, Dict
import os


class OCRModel:
    """OCR model using Tesseract for Nepali and Sinhalese text extraction"""
    
    def __init__(self):
        # Set Tesseract path if specified in environment
        tesseract_path = os.getenv('TESSERACT_PATH')
        if tesseract_path:
            pytesseract.pytesseract.tesseract_cmd = tesseract_path
        
        # Language mappings
        self.language_map = {
            'ne': 'nep',  # Nepali
            'si': 'sin',  # Sinhalese
            'en': 'eng'   # English
        }
    
    async def extract_text(
        self,
        image_path: str,
        language: Optional[str] = None,
        preprocess: bool = True
    ) -> str:
        """
        Extract text from image using Tesseract OCR
        
        Args:
            image_path: Path to image file
            language: Language code ('ne', 'si', 'en')
            preprocess: Apply image preprocessing
        
        Returns:
            Extracted text
        """
        try:
            # Load image
            image = Image.open(image_path)
            
            # Preprocess image if requested
            if preprocess:
                image = self._preprocess_image(image)
            
            # Determine Tesseract language
            if language:
                tesseract_lang = self.language_map.get(language, 'eng')
            else:
                # Try multiple languages
                tesseract_lang = 'nep+sin+eng'
            
            # Extract text
            custom_config = r'--oem 3 --psm 6'
            text = pytesseract.image_to_string(
                image,
                lang=tesseract_lang,
                config=custom_config
            )
            
            return text.strip()
            
        except Exception as e:
            raise Exception(f"OCR extraction failed: {str(e)}")
    
    async def get_word_confidences(
        self,
        image_path: str,
        language: Optional[str] = None
    ) -> List[Dict]:
        """
        Get confidence scores for each extracted word
        
        Returns:
            List of {word, confidence, bbox} dictionaries
        """
        try:
            image = Image.open(image_path)
            
            tesseract_lang = self.language_map.get(language, 'eng') if language else 'nep+sin+eng'
            
            # Get detailed data
            data = pytesseract.image_to_data(
                image,
                lang=tesseract_lang,
                output_type=pytesseract.Output.DICT
            )
            
            word_confidences = []
            n_boxes = len(data['text'])
            
            for i in range(n_boxes):
                if int(data['conf'][i]) > 0:  # Valid confidence
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
            
        except Exception as e:
            return []
    
    def _preprocess_image(self, image: Image.Image) -> Image.Image:
        """
        Preprocess image for better OCR accuracy
        
        Args:
            image: PIL Image
        
        Returns:
            Preprocessed PIL Image
        """
        # Convert PIL to OpenCV format
        img_cv = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
        
        # Convert to grayscale
        gray = cv2.cvtColor(img_cv, cv2.COLOR_BGR2GRAY)
        
        # Apply denoising
        denoised = cv2.fastNlMeansDenoising(gray)
        
        # Apply adaptive thresholding
        thresh = cv2.adaptiveThreshold(
            denoised,
            255,
            cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
            cv2.THRESH_BINARY,
            11,
            2
        )
        
        # Convert back to PIL
        processed_image = Image.fromarray(thresh)
        
        return processed_image
    
    def get_available_languages(self) -> List[str]:
        """Get list of available Tesseract languages"""
        try:
            langs = pytesseract.get_languages()
            return langs
        except:
            return ['eng', 'nep', 'sin']
