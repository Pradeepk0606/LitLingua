"""
Database Models
"""

from sqlalchemy import Column, Integer, String, Text, Float, DateTime, Boolean
from sqlalchemy.sql import func
from database.db_config import Base


class TranslationHistory(Base):
    """Translation history model"""
    __tablename__ = "translation_history"
    
    id = Column(Integer, primary_key=True, index=True)
    original_text = Column(Text, nullable=False)
    translated_text = Column(Text, nullable=False)
    source_language = Column(String(10), nullable=False)
    target_language = Column(String(10), default='en')
    confidence_score = Column(Float, default=0.0)
    model_used = Column(String(50))
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class User(Base):
    """User model"""
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    is_active = Column(Boolean, default=True)


class Glossary(Base):
    """Glossary model"""
    __tablename__ = "glossary"
    
    id = Column(Integer, primary_key=True, index=True)
    source_text = Column(String(200), nullable=False)
    target_text = Column(String(200), nullable=False)
    source_language = Column(String(10), nullable=False)
    target_language = Column(String(10), default='en')
    category = Column(String(50))
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class Feedback(Base):
    """User feedback model"""
    __tablename__ = "feedback"
    
    id = Column(Integer, primary_key=True, index=True)
    original_text = Column(Text, nullable=False)
    machine_translation = Column(Text, nullable=False)
    user_correction = Column(Text, nullable=False)
    source_language = Column(String(10), nullable=False)
    confidence_score = Column(Float)
    notes = Column(Text)
    used_for_training = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
