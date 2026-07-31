"""
Language Detection Utility
"""

from langdetect import detect, detect_langs
from typing import Dict, Optional
import re


class LanguageDetector:
    """Detect language of input text"""
    
    def __init__(self):
        self.supported_languages = {
            'ne': 'Nepali',
            'si': 'Sinhalese',
            'en': 'English'
        }
    
    def detect(self, text: str) -> Dict:
        """
        Detect language of text
        
        Args:
            text: Input text
        
        Returns:
            Dictionary with language code and confidence
        """
        try:
            # Clean text
            text = text.strip()
            
            if not text:
                return {'language': 'unknown', 'confidence': 0.0}
            
            # Check for Devanagari script (Nepali)
            if self._is_devanagari(text):
                return {'language': 'ne', 'confidence': 0.95}
            
            # Check for Sinhala script
            if self._is_sinhala(text):
                return {'language': 'si', 'confidence': 0.95}
            
            # Use langdetect for other cases
            detected_lang = detect(text)
            langs = detect_langs(text)
            
            # Get confidence for detected language
            confidence = 0.0
            for lang in langs:
                if lang.lang == detected_lang:
                    confidence = lang.prob
                    break
            
            return {
                'language': detected_lang,
                'confidence': confidence
            }
            
        except Exception as e:
            return {'language': 'unknown', 'confidence': 0.0}
    
    def _is_devanagari(self, text: str) -> bool:
        """Check if text contains Devanagari script"""
        devanagari_pattern = re.compile(r'[\u0900-\u097F]')
        return bool(devanagari_pattern.search(text))
    
    def _is_sinhala(self, text: str) -> bool:
        """Check if text contains Sinhala script"""
        sinhala_pattern = re.compile(r'[\u0D80-\u0DFF]')
        return bool(sinhala_pattern.search(text))
    
    def get_supported_languages(self) -> Dict:
        """Get list of supported languages"""
        return self.supported_languages
