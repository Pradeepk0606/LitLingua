"""
Glossary Manager - Custom dictionary support
"""

import sqlite3
from typing import List, Dict, Optional
from pathlib import Path


class GlossaryManager:
    """Manage custom translation glossary"""
    
    def __init__(self, db_path: str = "data/glossary.db"):
        self.db_path = db_path
        Path(db_path).parent.mkdir(parents=True, exist_ok=True)
        self._init_database()
    
    def _init_database(self):
        """Initialize glossary database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS glossary (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                source_text TEXT NOT NULL,
                target_text TEXT NOT NULL,
                source_language TEXT NOT NULL,
                target_language TEXT DEFAULT 'en',
                category TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                UNIQUE(source_text, source_language, target_language)
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def add_entry(
        self,
        source_text: str,
        target_text: str,
        source_language: str,
        target_language: str = 'en',
        category: Optional[str] = None
    ) -> bool:
        """Add entry to glossary"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT OR REPLACE INTO glossary 
                (source_text, target_text, source_language, target_language, category)
                VALUES (?, ?, ?, ?, ?)
            ''', (source_text, target_text, source_language, target_language, category))
            
            conn.commit()
            conn.close()
            
            return True
            
        except Exception as e:
            return False
    
    def get_entries(
        self,
        source_language: str,
        target_language: str = 'en',
        category: Optional[str] = None
    ) -> List[Dict]:
        """Get glossary entries"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        if category:
            cursor.execute('''
                SELECT source_text, target_text, category, created_at
                FROM glossary
                WHERE source_language = ? AND target_language = ? AND category = ?
            ''', (source_language, target_language, category))
        else:
            cursor.execute('''
                SELECT source_text, target_text, category, created_at
                FROM glossary
                WHERE source_language = ? AND target_language = ?
            ''', (source_language, target_language))
        
        entries = []
        for row in cursor.fetchall():
            entries.append({
                'source_text': row[0],
                'target_text': row[1],
                'category': row[2],
                'created_at': row[3]
            })
        
        conn.close()
        return entries
    
    def apply_glossary(self, text: str, source_language: str) -> str:
        """Apply glossary replacements to text"""
        entries = self.get_entries(source_language)
        
        for entry in entries:
            text = text.replace(entry['source_text'], entry['target_text'])
        
        return text
    
    def delete_entry(self, source_text: str, source_language: str) -> bool:
        """Delete glossary entry"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                DELETE FROM glossary
                WHERE source_text = ? AND source_language = ?
            ''', (source_text, source_language))
            
            conn.commit()
            conn.close()
            
            return True
            
        except Exception as e:
            return False
