"""
Translation Router - Handles AI-powered translation
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

from models.translation_model import TranslationModel
from utils.glossary_manager import GlossaryManager
from utils.heatmap_generator import HeatmapGenerator
from database.db_config import get_db
from database.models import TranslationHistory

router = APIRouter()

# Initialize models
translation_model = TranslationModel()
glossary_manager = GlossaryManager()
heatmap_generator = HeatmapGenerator()


class TranslationRequest(BaseModel):
    text: str
    source_language: str  # 'ne' or 'si'
    target_language: str = 'en'
    use_glossary: bool = True
    preserve_formatting: bool = True


class TranslationResponse(BaseModel):
    original_text: str
    translated_text: str
    source_language: str
    target_language: str
    confidence_score: float
    word_alignments: List[dict]
    confidence_heatmap: List[dict]
    translation_time: float
    model_used: str


@router.post("/translate", response_model=TranslationResponse)
async def translate_text(request: TranslationRequest):
    """
    Translate text from Nepali/Sinhalese to English
    
    Args:
        request: TranslationRequest with text and language parameters
    
    Returns:
        Translated text with confidence scores and alignments
    """
    try:
        start_time = datetime.now()
        
        # Apply custom glossary if enabled
        preprocessed_text = request.text
        if request.use_glossary:
            preprocessed_text = glossary_manager.apply_glossary(
                preprocessed_text,
                request.source_language
            )
        
        # Perform translation
        translation_result = await translation_model.translate(
            text=preprocessed_text,
            source_lang=request.source_language,
            target_lang=request.target_language
        )
        
        # Generate confidence heatmap
        heatmap_data = heatmap_generator.generate_heatmap(
            original_text=request.text,
            translated_text=translation_result['translated_text'],
            word_scores=translation_result.get('word_scores', [])
        )
        
        # Calculate translation time
        translation_time = (datetime.now() - start_time).total_seconds()
        
        # Save to history (async)
        # This would be done in a background task in production
        
        return TranslationResponse(
            original_text=request.text,
            translated_text=translation_result['translated_text'],
            source_language=request.source_language,
            target_language=request.target_language,
            confidence_score=translation_result.get('confidence', 0.95),
            word_alignments=translation_result.get('alignments', []),
            confidence_heatmap=heatmap_data,
            translation_time=translation_time,
            model_used=translation_result.get('model_name', 'MarianMT')
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Translation failed: {str(e)}"
        )


@router.post("/translate-batch")
async def translate_batch(texts: List[str], source_language: str, target_language: str = 'en'):
    """
    Translate multiple texts in batch for better performance
    """
    try:
        results = []
        
        for text in texts:
            request = TranslationRequest(
                text=text,
                source_language=source_language,
                target_language=target_language
            )
            result = await translate_text(request)
            results.append(result)
        
        return {
            "total": len(texts),
            "results": results
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Batch translation failed: {str(e)}")


@router.post("/improve")
async def improve_translation(
    original_text: str,
    current_translation: str,
    source_language: str
):
    """
    Improve translation quality using advanced techniques
    """
    try:
        improved = await translation_model.improve_translation(
            original=original_text,
            translation=current_translation,
            source_lang=source_language
        )
        
        return {
            "original_translation": current_translation,
            "improved_translation": improved['text'],
            "improvements": improved.get('changes', []),
            "confidence_improvement": improved.get('confidence_delta', 0.0)
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Translation improvement failed: {str(e)}")


@router.post("/explain")
async def explain_translation(
    original_text: str,
    translated_text: str,
    source_language: str
):
    """
    Explain translation decisions in plain English
    """
    try:
        explanation = await translation_model.explain_translation(
            original=original_text,
            translation=translated_text,
            source_lang=source_language
        )
        
        return {
            "explanation": explanation['text'],
            "key_decisions": explanation.get('decisions', []),
            "cultural_notes": explanation.get('cultural_notes', []),
            "alternative_translations": explanation.get('alternatives', [])
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Explanation generation failed: {str(e)}")


@router.get("/models")
async def get_available_models():
    """Get list of available translation models"""
    return {
        "models": [
            {
                "id": "marian-ne-en",
                "name": "MarianMT Nepali-English",
                "source": "ne",
                "target": "en",
                "status": "available",
                "offline": True
            },
            {
                "id": "marian-si-en",
                "name": "MarianMT Sinhalese-English",
                "source": "si",
                "target": "en",
                "status": "available",
                "offline": True
            },
            {
                "id": "m2m100",
                "name": "M2M100 Multilingual",
                "source": "multi",
                "target": "multi",
                "status": "available",
                "offline": True
            }
        ]
    }


@router.post("/align")
async def align_bilingual_text(
    source_text: str,
    target_text: str,
    source_language: str
):
    """
    Create bilingual text alignment for educational purposes
    """
    try:
        alignment = await translation_model.align_texts(
            source=source_text,
            target=target_text,
            source_lang=source_language
        )
        
        return {
            "aligned_segments": alignment['segments'],
            "sentence_pairs": alignment.get('sentence_pairs', []),
            "word_mappings": alignment.get('word_mappings', [])
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Text alignment failed: {str(e)}")
