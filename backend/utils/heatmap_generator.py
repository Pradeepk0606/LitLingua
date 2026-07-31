"""
Heatmap Generator - Confidence visualization
"""

from typing import List, Dict


class HeatmapGenerator:
    """Generate confidence heatmap for translations"""
    
    def __init__(self):
        self.confidence_thresholds = {
            'high': 0.8,
            'medium': 0.5,
            'low': 0.0
        }
    
    def generate_heatmap(
        self,
        original_text: str,
        translated_text: str,
        word_scores: List[float] = None
    ) -> List[Dict]:
        """
        Generate confidence heatmap data
        
        Args:
            original_text: Original text
            translated_text: Translated text
            word_scores: Optional confidence scores per word
        
        Returns:
            List of word-level confidence data
        """
        words = translated_text.split()
        
        # If no scores provided, use default high confidence
        if not word_scores or len(word_scores) != len(words):
            word_scores = [0.9] * len(words)
        
        heatmap_data = []
        
        for i, (word, score) in enumerate(zip(words, word_scores)):
            confidence_level = self._get_confidence_level(score)
            color = self._get_color_for_confidence(score)
            
            heatmap_data.append({
                'word': word,
                'position': i,
                'confidence': score,
                'level': confidence_level,
                'color': color
            })
        
        return heatmap_data
    
    def _get_confidence_level(self, score: float) -> str:
        """Get confidence level from score"""
        if score >= self.confidence_thresholds['high']:
            return 'high'
        elif score >= self.confidence_thresholds['medium']:
            return 'medium'
        else:
            return 'low'
    
    def _get_color_for_confidence(self, score: float) -> str:
        """Get color code for confidence score"""
        if score >= 0.8:
            return '#4ade80'  # Green
        elif score >= 0.5:
            return '#fbbf24'  # Yellow
        else:
            return '#f87171'  # Red
