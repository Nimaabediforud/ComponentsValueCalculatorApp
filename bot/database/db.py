import sqlite3
import os
from datetime import datetime

DB_PATH = os.path.join(os.path.dirname(__file__), 'bot_data.db')

def get_connection():
    """Return a connection to the SQLite database."""
    return sqlite3.connect(DB_PATH)

def init_db():
    """Create tables if they don't exist. Call this once when bot starts."""
    with get_connection() as conn:
        cursor = conn.cursor()
        # Users table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                chat_id INTEGER PRIMARY KEY,
                language TEXT DEFAULT 'en',
                theme TEXT DEFAULT 'light',
                joined_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                last_active TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        # Saved results table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS saved_results (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                chat_id INTEGER,
                component_type TEXT,
                subtype TEXT,
                input_value TEXT,
                output_text TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (chat_id) REFERENCES users(chat_id) ON DELETE CASCADE
            )
        ''')
        conn.commit()

def ensure_user(chat_id):
    """Insert user if not exists, update last_active."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            INSERT OR IGNORE INTO users (chat_id) VALUES (?)
        ''', (chat_id,))
        cursor.execute('''
            UPDATE users SET last_active = CURRENT_TIMESTAMP WHERE chat_id = ?
        ''', (chat_id,))
        conn.commit()

def save_result(chat_id, component_type, subtype, input_value, output_text):
    """Store a calculated result in the user's saved list."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO saved_results (chat_id, component_type, subtype, input_value, output_text)
            VALUES (?, ?, ?, ?, ?)
        ''', (chat_id, component_type, subtype, input_value, output_text))
        conn.commit()

def get_saved_results(chat_id, limit=20):
    """Retrieve saved results for a user, newest first."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            SELECT component_type, subtype, input_value, output_text, created_at
            FROM saved_results
            WHERE chat_id = ?
            ORDER BY created_at DESC
            LIMIT ?
        ''', (chat_id, limit))
        return cursor.fetchall()

def clear_saved_results(chat_id):
    """Delete all saved results for a user."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('DELETE FROM saved_results WHERE chat_id = ?', (chat_id,))
        conn.commit()

def is_result_saved(chat_id, output_text):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            SELECT 1 FROM saved_results 
            WHERE chat_id = ? AND output_text = ? 
            LIMIT 1
        ''', (chat_id, output_text))
        return cursor.fetchone() is not None
    
