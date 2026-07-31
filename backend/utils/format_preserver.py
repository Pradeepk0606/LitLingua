"""
Format Preserver Utility - Maintains document structure
"""

from typing import Dict, List
import re


class FormatPreserver:
    """Preserve document formatting during translation"""
    
    def __init__(self):
        self.formatting_markers = {
            'paragraph': r'\n\n',
            'line_break': r'\n',
            'bullet': r'[•\-\*]\s',
            'numbering': r'\d+\.\s',
            'heading': r'^#{1,6}\s'
        }
    
    def extract_structure(self, text: str) -> Dict:
        """
        Extract document structure
        
        Args:
            text: Original text
        
        Returns:
            Dictionary with structure information
        """
        structure = {
            'paragraphs': [],
            'bullets': [],
            'numbering': [],
            'headings': []
        }
        
        lines = text.split('\n')
        
        for i, line in enumerate(lines):
            line = line.strip()
            
            if not line:
                continue
            
            # Check for headings
            if re.match(self.formatting_markers['heading'], line):
                structure['headings'].append({
                    'line': i,
                    'text': line,
                    'level': len(re.match(r'^(#+)', line).group(1))
                })
            
            # Check for bullets
            elif re.match(self.formatting_markers['bullet'], line):
                structure['bullets'].append({
                    'line': i,
                    'text': line
                })
            
            # Check for numbering
            elif re.match(self.formatting_markers['numbering'], line):
                structure['numbering'].append({
                    'line': i,
                    'text': line
                })
            
            else:
                structure['paragraphs'].append({
                    'line': i,
                    'text': line
                })
        
        return structure
    
    def apply_structure(
        self,
        translated_text: str,
        original_structure: Dict
    ) -> str:
        """
        Apply original structure to translated text
        
        Args:
            translated_text: Translated text
            original_structure: Structure from extract_structure
        
        Returns:
            Formatted translated text
        """
        # This is a simplified implementation
        # In production, this would intelligently map structure
        
        return translated_text
    
    def preserve_special_elements(self, text: str) -> Dict:
        """Preserve special elements like URLs, emails, numbers"""
        
        elements = {
            'urls': re.findall(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', text),
            'emails': re.findall(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', text),
            'numbers': re.findall(r'\b\d+(?:\.\d+)?\b', text),
            'dates': re.findall(r'\b\d{1,2}[/-]\d{1,2}[/-]\d{2,4}\b', text)
        }
        
        return elements
