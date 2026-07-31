"""
Incremental model fine-tuning using user corrections
"""

import json
from pathlib import Path
from typing import List, Dict
import torch
from transformers import MarianMTModel, MarianTokenizer, Trainer, TrainingArguments
from torch.utils.data import Dataset


class TranslationDataset(Dataset):
    """Custom dataset for translation fine-tuning"""
    
    def __init__(self, source_texts: List[str], target_texts: List[str], tokenizer):
        self.source_texts = source_texts
        self.target_texts = target_texts
        self.tokenizer = tokenizer
    
    def __len__(self):
        return len(self.source_texts)
    
    def __getitem__(self, idx):
        source = self.source_texts[idx]
        target = self.target_texts[idx]
        
        inputs = self.tokenizer(source, max_length=128, truncation=True, padding='max_length', return_tensors='pt')
        labels = self.tokenizer(target, max_length=128, truncation=True, padding='max_length', return_tensors='pt')
        
        return {
            'input_ids': inputs['input_ids'].squeeze(),
            'attention_mask': inputs['attention_mask'].squeeze(),
            'labels': labels['input_ids'].squeeze()
        }


def load_feedback_data(feedback_file: str = 'backend/data/user_feedbacks.json') -> Dict:
    """Load user feedback data"""
    with open(feedback_file, 'r', encoding='utf-8') as f:
        feedbacks = json.load(f)
    
    # Separate by language
    data_by_lang = {}
    
    for fb in feedbacks:
        if fb.get('used_for_training', False):
            continue
        
        lang = fb['source_language']
        if lang not in data_by_lang:
            data_by_lang[lang] = {'source': [], 'target': []}
        
        data_by_lang[lang]['source'].append(fb['original_text'])
        data_by_lang[lang]['target'].append(fb['user_correction'])
    
    return data_by_lang


def fine_tune_model(
    model_path: str,
    source_texts: List[str],
    target_texts: List[str],
    output_path: str,
    epochs: int = 3
):
    """Fine-tune translation model"""
    
    print(f"🔧 Fine-tuning model: {model_path}")
    print(f"📊 Training samples: {len(source_texts)}")
    
    # Load model and tokenizer
    tokenizer = MarianTokenizer.from_pretrained(model_path)
    model = MarianMTModel.from_pretrained(model_path)
    
    # Create dataset
    dataset = TranslationDataset(source_texts, target_texts, tokenizer)
    
    # Training arguments
    training_args = TrainingArguments(
        output_dir=output_path,
        num_train_epochs=epochs,
        per_device_train_batch_size=4,
        save_steps=100,
        save_total_limit=2,
        logging_steps=10,
        learning_rate=5e-5,
        warmup_steps=50,
        weight_decay=0.01
    )
    
    # Trainer
    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=dataset
    )
    
    # Train
    print("🚀 Starting training...")
    trainer.train()
    
    # Save fine-tuned model
    model.save_pretrained(output_path)
    tokenizer.save_pretrained(output_path)
    
    print(f"✅ Model fine-tuned and saved to {output_path}")


def main():
    """Main retraining function"""
    print("🧠 LitLingua Model Retraining")
    print("=" * 50)
    
    # Load feedback data
    data_by_lang = load_feedback_data()
    
    if not data_by_lang:
        print("⚠️  No feedback data available for retraining")
        return
    
    # Fine-tune each language model
    model_paths = {
        'ne': 'backend/data/offline_models/ne-en',
        'si': 'backend/data/offline_models/si-en'
    }
    
    for lang, data in data_by_lang.items():
        if lang not in model_paths:
            print(f"⚠️  No model path configured for language: {lang}")
            continue
        
        if len(data['source']) < 10:
            print(f"⚠️  Insufficient data for {lang} (need at least 10 samples)")
            continue
        
        model_path = model_paths[lang]
        output_path = f"{model_path}_finetuned"
        
        fine_tune_model(
            model_path=model_path,
            source_texts=data['source'],
            target_texts=data['target'],
            output_path=output_path,
            epochs=3
        )
    
    print("\n✨ Retraining complete!")


if __name__ == "__main__":
    main()
