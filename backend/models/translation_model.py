"""
Translation Model - MarianMT/M2M100 integration for translation
"""

from transformers import MarianMTModel, MarianTokenizer, M2M100ForConditionalGeneration, M2M100Tokenizer
import torch
from typing import Optional, Dict, List
import os
from pathlib import Path


class TranslationModel:
    """Translation model using HuggingFace Transformers"""
    
    def __init__(self):
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.models = {}
        self.tokenizers = {}
        self.model_cache_dir = os.getenv('MODEL_CACHE_DIR', './data/offline_models')
        
        # Model mappings
        self.model_names = {
            'ne-en': 'Helsinki-NLP/opus-mt-ne-en',
            'si-en': 'Helsinki-NLP/opus-mt-si-en',
            'm2m100': 'facebook/m2m100_418M'
        }
        
        # Load models lazily
        self._loaded_models = set()
    
    async def translate(
        self,
        text: str,
        source_lang: str,
        target_lang: str = 'en',
        use_m2m: bool = False
    ) -> Dict:
        """
        Translate text from source language to target language
        
        Args:
            text: Text to translate
            source_lang: Source language code ('ne', 'si')
            target_lang: Target language code (default: 'en')
            use_m2m: Use M2M100 model instead of MarianMT
        
        Returns:
            Dictionary with translated text and metadata
        """
        try:
            if use_m2m:
                return await self._translate_m2m100(text, source_lang, target_lang)
            else:
                return await self._translate_marian(text, source_lang, target_lang)
                
        except Exception as e:
            raise Exception(f"Translation failed: {str(e)}")
    
    async def _translate_marian(
        self,
        text: str,
        source_lang: str,
        target_lang: str
    ) -> Dict:
        """Translate using MarianMT model"""
        
        model_key = f"{source_lang}-{target_lang}"
        
        # Load model if not already loaded
        if model_key not in self._loaded_models:
            await self._load_marian_model(model_key)
        
        model = self.models[model_key]
        tokenizer = self.tokenizers[model_key]
        
        # Tokenize
        inputs = tokenizer(text, return_tensors="pt", padding=True, truncation=True, max_length=512)
        inputs = {k: v.to(self.device) for k, v in inputs.items()}
        
        # Generate translation
        with torch.no_grad():
            outputs = model.generate(
                **inputs,
                max_length=512,
                num_beams=5,
                early_stopping=True,
                return_dict_in_generate=True,
                output_scores=True
            )
        
        # Decode
        translated_text = tokenizer.decode(outputs.sequences[0], skip_special_tokens=True)
        
        # Calculate confidence (approximation from scores)
        confidence = self._calculate_confidence(outputs.scores) if hasattr(outputs, 'scores') else 0.95
        
        return {
            'translated_text': translated_text,
            'confidence': confidence,
            'model_name': f'MarianMT-{model_key}',
            'word_scores': [],
            'alignments': []
        }
    
    async def _translate_m2m100(
        self,
        text: str,
        source_lang: str,
        target_lang: str
    ) -> Dict:
        """Translate using M2M100 model"""
        
        model_key = 'm2m100'
        
        # Load model if not already loaded
        if model_key not in self._loaded_models:
            await self._load_m2m100_model()
        
        model = self.models[model_key]
        tokenizer = self.tokenizers[model_key]
        
        # Set source and target languages
        tokenizer.src_lang = source_lang
        
        # Tokenize
        inputs = tokenizer(text, return_tensors="pt", padding=True, truncation=True)
        inputs = {k: v.to(self.device) for k, v in inputs.items()}
        
        # Generate translation
        generated_tokens = model.generate(
            **inputs,
            forced_bos_token_id=tokenizer.get_lang_id(target_lang),
            max_length=512,
            num_beams=5
        )
        
        # Decode
        translated_text = tokenizer.batch_decode(generated_tokens, skip_special_tokens=True)[0]
        
        return {
            'translated_text': translated_text,
            'confidence': 0.92,
            'model_name': 'M2M100',
            'word_scores': [],
            'alignments': []
        }
    
    async def _load_marian_model(self, model_key: str):
        """Load MarianMT model"""
        model_name = self.model_names.get(model_key)
        
        if not model_name:
            raise ValueError(f"No model available for {model_key}")
        
        try:
            # Try to load from cache first
            cache_path = Path(self.model_cache_dir) / model_key
            
            if cache_path.exists():
                tokenizer = MarianTokenizer.from_pretrained(str(cache_path))
                model = MarianMTModel.from_pretrained(str(cache_path))
            else:
                # Download from HuggingFace
                tokenizer = MarianTokenizer.from_pretrained(model_name)
                model = MarianMTModel.from_pretrained(model_name)
                
                # Save to cache
                cache_path.mkdir(parents=True, exist_ok=True)
                tokenizer.save_pretrained(str(cache_path))
                model.save_pretrained(str(cache_path))
            
            model.to(self.device)
            model.eval()
            
            self.models[model_key] = model
            self.tokenizers[model_key] = tokenizer
            self._loaded_models.add(model_key)
            
        except Exception as e:
            raise Exception(f"Failed to load model {model_key}: {str(e)}")
    
    async def _load_m2m100_model(self):
        """Load M2M100 model"""
        model_key = 'm2m100'
        model_name = self.model_names[model_key]
        
        try:
            cache_path = Path(self.model_cache_dir) / model_key
            
            if cache_path.exists():
                tokenizer = M2M100Tokenizer.from_pretrained(str(cache_path))
                model = M2M100ForConditionalGeneration.from_pretrained(str(cache_path))
            else:
                tokenizer = M2M100Tokenizer.from_pretrained(model_name)
                model = M2M100ForConditionalGeneration.from_pretrained(model_name)
                
                cache_path.mkdir(parents=True, exist_ok=True)
                tokenizer.save_pretrained(str(cache_path))
                model.save_pretrained(str(cache_path))
            
            model.to(self.device)
            model.eval()
            
            self.models[model_key] = model
            self.tokenizers[model_key] = tokenizer
            self._loaded_models.add(model_key)
            
        except Exception as e:
            raise Exception(f"Failed to load M2M100 model: {str(e)}")
    
    def _calculate_confidence(self, scores) -> float:
        """Calculate average confidence from generation scores"""
        if not scores:
            return 0.95
        
        try:
            # Average probability of top predictions
            probs = [torch.softmax(score, dim=-1).max().item() for score in scores]
            return sum(probs) / len(probs)
        except:
            return 0.95
    
    async def improve_translation(
        self,
        original: str,
        translation: str,
        source_lang: str
    ) -> Dict:
        """Improve translation quality (placeholder for GPT enhancement)"""
        # This would integrate with GPT for refinement
        # For now, return the same translation
        return {
            'text': translation,
            'changes': [],
            'confidence_delta': 0.0
        }
    
    async def explain_translation(
        self,
        original: str,
        translation: str,
        source_lang: str
    ) -> Dict:
        """Explain translation decisions"""
        # Placeholder implementation
        return {
            'text': f"The text was translated from {source_lang} to English using neural machine translation.",
            'decisions': [],
            'cultural_notes': [],
            'alternatives': []
        }
    
    async def align_texts(
        self,
        source: str,
        target: str,
        source_lang: str
    ) -> Dict:
        """Create bilingual text alignment"""
        # Split into sentences
        source_sentences = source.split('.')
        target_sentences = target.split('.')
        
        segments = []
        for i, (src, tgt) in enumerate(zip(source_sentences, target_sentences)):
            if src.strip() and tgt.strip():
                segments.append({
                    'index': i,
                    'source': src.strip(),
                    'target': tgt.strip()
                })
        
        return {
            'segments': segments,
            'sentence_pairs': segments,
            'word_mappings': []
        }
