"""
Feedback Router - Handles user corrections and model retraining
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
import json
from pathlib import Path

from models.retrain_model import RetrainingManager

router = APIRouter()

# Initialize retraining manager
retrain_manager = RetrainingManager()

# Feedback storage
FEEDBACK_FILE = Path("data/user_feedbacks.json")
FEEDBACK_FILE.parent.mkdir(parents=True, exist_ok=True)


class FeedbackSubmission(BaseModel):
    original_text: str
    machine_translation: str
    user_correction: str
    source_language: str
    target_language: str = 'en'
    confidence_score: Optional[float] = None
    notes: Optional[str] = None


class FeedbackResponse(BaseModel):
    feedback_id: str
    status: str
    message: str
    will_retrain: bool


@router.post("/submit", response_model=FeedbackResponse)
async def submit_feedback(feedback: FeedbackSubmission):
    """
    Submit user correction for translation improvement
    
    Args:
        feedback: User's corrected translation
    
    Returns:
        Feedback confirmation and retraining status
    """
    try:
        # Generate feedback ID
        feedback_id = f"fb_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{hash(feedback.original_text) % 10000}"
        
        # Load existing feedbacks
        feedbacks = []
        if FEEDBACK_FILE.exists():
            with open(FEEDBACK_FILE, 'r', encoding='utf-8') as f:
                feedbacks = json.load(f)
        
        # Add new feedback
        feedback_entry = {
            "id": feedback_id,
            "timestamp": datetime.now().isoformat(),
            "original_text": feedback.original_text,
            "machine_translation": feedback.machine_translation,
            "user_correction": feedback.user_correction,
            "source_language": feedback.source_language,
            "target_language": feedback.target_language,
            "confidence_score": feedback.confidence_score,
            "notes": feedback.notes,
            "used_for_training": False
        }
        
        feedbacks.append(feedback_entry)
        
        # Save feedbacks
        with open(FEEDBACK_FILE, 'w', encoding='utf-8') as f:
            json.dump(feedbacks, f, indent=2, ensure_ascii=False)
        
        # Check if we should trigger retraining
        will_retrain = len(feedbacks) >= 100  # Retrain after 100 feedbacks
        
        if will_retrain:
            # Trigger background retraining
            await retrain_manager.schedule_retraining(feedbacks)
        
        return FeedbackResponse(
            feedback_id=feedback_id,
            status="success",
            message="Feedback submitted successfully. Thank you for improving LitLingua!",
            will_retrain=will_retrain
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Feedback submission failed: {str(e)}")


@router.get("/stats")
async def get_feedback_stats():
    """Get feedback statistics"""
    try:
        if not FEEDBACK_FILE.exists():
            return {
                "total_feedbacks": 0,
                "by_language": {},
                "used_for_training": 0,
                "pending_training": 0
            }
        
        with open(FEEDBACK_FILE, 'r', encoding='utf-8') as f:
            feedbacks = json.load(f)
        
        # Calculate statistics
        by_language = {}
        used_for_training = 0
        
        for fb in feedbacks:
            lang = fb.get('source_language', 'unknown')
            by_language[lang] = by_language.get(lang, 0) + 1
            if fb.get('used_for_training', False):
                used_for_training += 1
        
        return {
            "total_feedbacks": len(feedbacks),
            "by_language": by_language,
            "used_for_training": used_for_training,
            "pending_training": len(feedbacks) - used_for_training,
            "next_retrain_at": 100 - (len(feedbacks) % 100)
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Stats retrieval failed: {str(e)}")


@router.get("/recent")
async def get_recent_feedbacks(limit: int = 10):
    """Get recent feedback submissions"""
    try:
        if not FEEDBACK_FILE.exists():
            return {"feedbacks": []}
        
        with open(FEEDBACK_FILE, 'r', encoding='utf-8') as f:
            feedbacks = json.load(f)
        
        # Sort by timestamp and limit
        recent = sorted(
            feedbacks,
            key=lambda x: x.get('timestamp', ''),
            reverse=True
        )[:limit]
        
        return {"feedbacks": recent}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Recent feedbacks retrieval failed: {str(e)}")


@router.post("/retrain")
async def trigger_retraining(
    language: Optional[str] = None,
    min_feedbacks: int = 50
):
    """
    Manually trigger model retraining
    
    Args:
        language: Optional language filter
        min_feedbacks: Minimum number of feedbacks required
    
    Returns:
        Retraining status
    """
    try:
        if not FEEDBACK_FILE.exists():
            raise HTTPException(status_code=400, detail="No feedbacks available for retraining")
        
        with open(FEEDBACK_FILE, 'r', encoding='utf-8') as f:
            feedbacks = json.load(f)
        
        # Filter by language if specified
        if language:
            feedbacks = [fb for fb in feedbacks if fb.get('source_language') == language]
        
        # Filter unused feedbacks
        unused_feedbacks = [fb for fb in feedbacks if not fb.get('used_for_training', False)]
        
        if len(unused_feedbacks) < min_feedbacks:
            return {
                "status": "insufficient_data",
                "message": f"Need at least {min_feedbacks} feedbacks. Currently have {len(unused_feedbacks)}.",
                "available_feedbacks": len(unused_feedbacks)
            }
        
        # Start retraining
        retrain_result = await retrain_manager.retrain_model(
            feedbacks=unused_feedbacks,
            language=language
        )
        
        # Mark feedbacks as used
        for fb in feedbacks:
            if fb['id'] in [f['id'] for f in unused_feedbacks]:
                fb['used_for_training'] = True
                fb['training_date'] = datetime.now().isoformat()
        
        with open(FEEDBACK_FILE, 'w', encoding='utf-8') as f:
            json.dump(feedbacks, f, indent=2, ensure_ascii=False)
        
        return {
            "status": "success",
            "message": "Model retraining initiated",
            "feedbacks_used": len(unused_feedbacks),
            "training_id": retrain_result.get('training_id'),
            "estimated_completion": retrain_result.get('estimated_completion')
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Retraining failed: {str(e)}")


@router.delete("/clear")
async def clear_feedbacks(confirm: bool = False):
    """Clear all feedback data (use with caution)"""
    if not confirm:
        raise HTTPException(
            status_code=400,
            detail="Please confirm deletion by setting confirm=true"
        )
    
    try:
        if FEEDBACK_FILE.exists():
            FEEDBACK_FILE.unlink()
        
        return {
            "status": "success",
            "message": "All feedbacks cleared"
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Clear operation failed: {str(e)}")
