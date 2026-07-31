# LitLingua API Reference

## Base URL
```
http://localhost:8000/api
```

## Authentication
Currently, the API does not require authentication. This may change in future versions.

---

## OCR Endpoints

### Extract Text from Image/PDF
**POST** `/ocr/extract`

Extract text from uploaded image or PDF file.

**Request:**
- Content-Type: `multipart/form-data`
- Body:
  - `file`: Image or PDF file (required)
  - `language`: Language code ('ne', 'si') (optional)
  - `detect_language`: Boolean (optional, default: true)

**Response:**
```json
{
  "success": true,
  "file_id": "uuid",
  "filename": "document.pdf",
  "text": "Extracted text content",
  "detected_language": "ne",
  "language_confidence": 0.95,
  "word_count": 150,
  "character_count": 750,
  "pages": 1,
  "page_texts": ["Page 1 text"],
  "word_confidences": [
    {
      "word": "word",
      "confidence": 0.98,
      "bbox": {"x": 10, "y": 20, "width": 50, "height": 20}
    }
  ]
}
```

---

## Translation Endpoints

### Translate Text
**POST** `/translate/translate`

Translate text from Nepali/Sinhalese to English.

**Request:**
```json
{
  "text": "Text to translate",
  "source_language": "ne",
  "target_language": "en",
  "use_glossary": true,
  "preserve_formatting": true
}
```

**Response:**
```json
{
  "original_text": "Original text",
  "translated_text": "Translated text",
  "source_language": "ne",
  "target_language": "en",
  "confidence_score": 0.92,
  "word_alignments": [],
  "confidence_heatmap": [
    {
      "word": "word",
      "position": 0,
      "confidence": 0.95,
      "level": "high",
      "color": "#4ade80"
    }
  ],
  "translation_time": 0.5,
  "model_used": "MarianMT-ne-en"
}
```

### Improve Translation
**POST** `/translate/improve`

Improve translation quality using advanced techniques.

**Request:**
```json
{
  "original_text": "Original text",
  "current_translation": "Current translation",
  "source_language": "ne"
}
```

### Explain Translation
**POST** `/translate/explain`

Get explanation of translation decisions.

**Request:**
```json
{
  "original_text": "Original text",
  "translated_text": "Translated text",
  "source_language": "ne"
}
```

---

## Audio Endpoints

### Text-to-Speech
**POST** `/audio/text-to-speech`

Convert text to speech audio.

**Request:**
- Content-Type: `multipart/form-data`
- Body:
  - `text`: Text to convert (required)
  - `language`: Language code (optional, default: 'en')
  - `speed`: Speech speed 0.5-2.0 (optional, default: 1.0)

**Response:**
- Audio file (MP3)

### Speech-to-Text
**POST** `/audio/speech-to-text`

Transcribe audio to text.

**Request:**
- Content-Type: `multipart/form-data`
- Body:
  - `audio_file`: Audio file (required)
  - `language`: Language hint (optional)

**Response:**
```json
{
  "success": true,
  "text": "Transcribed text",
  "language": "en",
  "confidence": 0.88,
  "duration": 5.2
}
```

---

## File Endpoints

### Export to PDF
**POST** `/files/export-pdf`

Export translation to formatted PDF.

**Request:**
- Content-Type: `multipart/form-data`
- Body:
  - `original_text`: Original text (required)
  - `translated_text`: Translated text (required)
  - `source_language`: Source language code (required)
  - `title`: Document title (optional)
  - `include_original`: Boolean (optional, default: true)
  - `layout`: 'side-by-side' or 'sequential' (optional)

**Response:**
- PDF file

---

## Feedback Endpoints

### Submit Feedback
**POST** `/feedback/submit`

Submit user correction for translation improvement.

**Request:**
```json
{
  "original_text": "Original text",
  "machine_translation": "Machine translation",
  "user_correction": "Corrected translation",
  "source_language": "ne",
  "target_language": "en",
  "confidence_score": 0.85,
  "notes": "Optional notes"
}
```

**Response:**
```json
{
  "feedback_id": "fb_20250107_123456_1234",
  "status": "success",
  "message": "Feedback submitted successfully",
  "will_retrain": false
}
```

### Get Feedback Statistics
**GET** `/feedback/stats`

Get feedback statistics.

**Response:**
```json
{
  "total_feedbacks": 50,
  "by_language": {
    "ne": 30,
    "si": 20
  },
  "used_for_training": 0,
  "pending_training": 50,
  "next_retrain_at": 50
}
```

---

## Error Responses

All endpoints may return error responses in the following format:

```json
{
  "error": "Error message",
  "status_code": 400,
  "detail": "Detailed error information"
}
```

### Common Status Codes
- `200`: Success
- `400`: Bad Request
- `404`: Not Found
- `500`: Internal Server Error

---

## Rate Limiting
Currently, there are no rate limits. This may change in production deployments.

## Versioning
API Version: 1.0.0

For more information, visit the interactive API documentation at:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc
