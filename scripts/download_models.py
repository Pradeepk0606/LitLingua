"""
Download and cache AI models for offline use
"""

from transformers import MarianMTModel, MarianTokenizer, M2M100ForConditionalGeneration, M2M100Tokenizer
from pathlib import Path
import os

# Model cache directory
CACHE_DIR = Path("backend/data/offline_models")
CACHE_DIR.mkdir(parents=True, exist_ok=True)

# Models to download
MODELS = {
    'ne-en': 'Helsinki-NLP/opus-mt-ne-en',
    'si-en': 'Helsinki-NLP/opus-mt-si-en',
    'm2m100': 'facebook/m2m100_418M'
}


def download_marian_model(model_key: str, model_name: str):
    """Download MarianMT model"""
    print(f"📥 Downloading {model_key} model...")
    
    save_path = CACHE_DIR / model_key
    save_path.mkdir(parents=True, exist_ok=True)
    
    try:
        tokenizer = MarianTokenizer.from_pretrained(model_name)
        model = MarianMTModel.from_pretrained(model_name)
        
        tokenizer.save_pretrained(str(save_path))
        model.save_pretrained(str(save_path))
        
        print(f"✅ {model_key} model downloaded successfully")
        
    except Exception as e:
        print(f"❌ Failed to download {model_key}: {str(e)}")


def download_m2m100_model(model_name: str):
    """Download M2M100 model"""
    print(f"📥 Downloading M2M100 model (this may take a while)...")
    
    save_path = CACHE_DIR / 'm2m100'
    save_path.mkdir(parents=True, exist_ok=True)
    
    try:
        tokenizer = M2M100Tokenizer.from_pretrained(model_name)
        model = M2M100ForConditionalGeneration.from_pretrained(model_name)
        
        tokenizer.save_pretrained(str(save_path))
        model.save_pretrained(str(save_path))
        
        print(f"✅ M2M100 model downloaded successfully")
        
    except Exception as e:
        print(f"❌ Failed to download M2M100: {str(e)}")


def main():
    """Download all models"""
    print("🚀 Starting model download for LitLingua...")
    print(f"📁 Cache directory: {CACHE_DIR.absolute()}\n")
    
    # Download MarianMT models
    for model_key, model_name in MODELS.items():
        if model_key == 'm2m100':
            download_m2m100_model(model_name)
        else:
            download_marian_model(model_key, model_name)
        print()
    
    print("✨ All models downloaded successfully!")
    print("🔒 LitLingua is now ready for offline use.")


if __name__ == "__main__":
    main()
