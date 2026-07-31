"""
Tests for OCR functionality
"""

import pytest
from pathlib import Path
from models.ocr_model import OCRModel


@pytest.fixture
def ocr_model():
    return OCRModel()


def test_ocr_model_initialization(ocr_model):
    """Test OCR model initializes correctly"""
    assert ocr_model is not None
    assert hasattr(ocr_model, 'language_map')


def test_language_mapping(ocr_model):
    """Test language code mapping"""
    assert ocr_model.language_map['ne'] == 'nep'
    assert ocr_model.language_map['si'] == 'sin'
    assert ocr_model.language_map['en'] == 'eng'


@pytest.mark.asyncio
async def test_extract_text_from_image(ocr_model, tmp_path):
    """Test text extraction from image"""
    # This would require a test image file
    # Placeholder test
    pass


def test_get_available_languages(ocr_model):
    """Test getting available languages"""
    languages = ocr_model.get_available_languages()
    assert isinstance(languages, list)
    assert 'eng' in languages
