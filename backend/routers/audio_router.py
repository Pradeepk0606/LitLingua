"""
Audio Router - Handles text-to-speech and speech-to-text
"""

from fastapi import APIRouter, UploadFile, File, HTTPException, Form
from fastapi.responses import FileResponse
from typing import Optional
from pathlib import Path
import uuid

from models.tts_model import TTSModel

router = APIRouter()

# Initialize TTS model
tts_model = TTSModel()


@router.post("/text-to-speech")
async def text_to_speech(
    text: str = Form(...),
    language: str = Form('en'),
    speed: float = Form(1.0)
):
    """
    Convert text to speech audio file
    
    Args:
        text: Text to convert to speech
        language: Language code ('en', 'ne', 'si')
        speed: Speech speed (0.5 to 2.0)
    
    Returns:
        Audio file (MP3)
    """
    try:
        # Generate unique filename
        audio_id = str(uuid.uuid4())
        audio_dir = Path("static/audio")
        audio_dir.mkdir(parents=True, exist_ok=True)
        audio_path = audio_dir / f"{audio_id}.mp3"
        
        # Generate speech
        await tts_model.generate_speech(
            text=text,
            output_path=str(audio_path),
            language=language,
            speed=speed
        )
        
        return FileResponse(
            path=audio_path,
            media_type="audio/mpeg",
            filename=f"speech_{audio_id}.mp3",
            headers={
                "X-Audio-ID": audio_id,
                "X-Text-Length": str(len(text))
            }
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"TTS generation failed: {str(e)}")


@router.post("/speech-to-text")
async def speech_to_text(
    audio_file: UploadFile = File(...),
    language: Optional[str] = Form(None)
):
    """
    Convert speech audio to text
    
    Args:
        audio_file: Audio file (MP3, WAV, OGG)
        language: Optional language hint
    
    Returns:
        Transcribed text
    """
    try:
        # Validate file type
        allowed_extensions = {'.mp3', '.wav', '.ogg', '.m4a'}
        file_ext = Path(audio_file.filename).suffix.lower()
        
        if file_ext not in allowed_extensions:
            raise HTTPException(
                status_code=400,
                detail=f"Unsupported audio format. Allowed: {', '.join(allowed_extensions)}"
            )
        
        # Save uploaded audio temporarily
        audio_dir = Path("static/audio")
        audio_dir.mkdir(parents=True, exist_ok=True)
        
        audio_id = str(uuid.uuid4())
        temp_audio_path = audio_dir / f"{audio_id}{file_ext}"
        
        with open(temp_audio_path, "wb") as buffer:
            content = await audio_file.read()
            buffer.write(content)
        
        # Transcribe audio
        transcription = await tts_model.transcribe_audio(
            audio_path=str(temp_audio_path),
            language=language
        )
        
        # Clean up temporary file
        temp_audio_path.unlink()
        
        return {
            "success": True,
            "text": transcription['text'],
            "language": transcription.get('detected_language'),
            "confidence": transcription.get('confidence', 0.0),
            "duration": transcription.get('duration', 0.0)
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Speech-to-text failed: {str(e)}")


@router.get("/voices")
async def get_available_voices():
    """Get list of available TTS voices"""
    return {
        "voices": [
            {
                "language": "en",
                "name": "English (US)",
                "code": "en-US",
                "gender": "neutral"
            },
            {
                "language": "en",
                "name": "English (UK)",
                "code": "en-GB",
                "gender": "neutral"
            },
            {
                "language": "ne",
                "name": "Nepali",
                "code": "ne-NP",
                "gender": "neutral"
            },
            {
                "language": "si",
                "name": "Sinhalese",
                "code": "si-LK",
                "gender": "neutral"
            }
        ]
    }


@router.delete("/audio/{audio_id}")
async def delete_audio(audio_id: str):
    """Delete generated audio file"""
    try:
        audio_dir = Path("static/audio")
        audio_path = audio_dir / f"{audio_id}.mp3"
        
        if audio_path.exists():
            audio_path.unlink()
            return {"success": True, "message": "Audio file deleted"}
        else:
            raise HTTPException(status_code=404, detail="Audio file not found")
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Audio deletion failed: {str(e)}")
