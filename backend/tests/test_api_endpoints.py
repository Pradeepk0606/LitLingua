"""
Tests for API endpoints
"""

import pytest
from fastapi.testclient import TestClient
from app import app


client = TestClient(app)


def test_root_endpoint():
    """Test root endpoint"""
    response = client.get("/")
    assert response.status_code == 200
    assert "message" in response.json()
    assert response.json()["status"] == "online"


def test_health_check():
    """Test health check endpoint"""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_get_supported_languages():
    """Test supported languages endpoint"""
    response = client.get("/api/languages")
    assert response.status_code == 200
    data = response.json()
    assert "source_languages" in data
    assert "target_languages" in data
    assert len(data["source_languages"]) >= 2


def test_get_ocr_languages():
    """Test OCR languages endpoint"""
    response = client.get("/api/ocr/languages")
    assert response.status_code == 200
    data = response.json()
    assert "supported_languages" in data


def test_get_translation_models():
    """Test translation models endpoint"""
    response = client.get("/api/translate/models")
    assert response.status_code == 200
    data = response.json()
    assert "models" in data
    assert len(data["models"]) >= 2


def test_feedback_stats():
    """Test feedback statistics endpoint"""
    response = client.get("/api/feedback/stats")
    assert response.status_code == 200
    data = response.json()
    assert "total_feedbacks" in data
