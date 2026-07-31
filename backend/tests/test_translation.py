"""
Tests for translation functionality
"""

import pytest
from models.translation_model import TranslationModel


@pytest.fixture
def translation_model():
    return TranslationModel()


def test_translation_model_initialization(translation_model):
    """Test translation model initializes correctly"""
    assert translation_model is not None
    assert hasattr(translation_model, 'model_names')


def test_model_names(translation_model):
    """Test model name mappings"""
    assert 'ne-en' in translation_model.model_names
    assert 'si-en' in translation_model.model_names
    assert 'm2m100' in translation_model.model_names


@pytest.mark.asyncio
async def test_translate_simple_text(translation_model):
    """Test simple translation"""
    # This would require loaded models
    # Placeholder test
    pass
