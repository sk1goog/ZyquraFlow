"""SQLite database for metadata index."""
import sqlite3
from contextlib import contextmanager
from pathlib import Path

from backend.config import DB_PATH


def get_conn():
    return sqlite3.connect(DB_PATH)


def init_db():
    conn = get_conn()
    try:
        conn.executescript("""
            CREATE TABLE IF NOT EXISTS config (
                key TEXT PRIMARY KEY,
                value TEXT
            );
            CREATE TABLE IF NOT EXISTS cases (
                case_id TEXT PRIMARY KEY,
                alias TEXT NOT NULL,
                created_at TEXT NOT NULL
            );
            CREATE TABLE IF NOT EXISTS sessions (
                session_id TEXT PRIMARY KEY,
                case_id TEXT,
                created_at TEXT NOT NULL,
                audio_path TEXT,
                summary_path TEXT,
                file_size INTEGER DEFAULT 0,
                duration REAL,
                status TEXT DEFAULT 'draft',
                transcript TEXT,
                FOREIGN KEY (case_id) REFERENCES cases(case_id)
            );
            INSERT OR IGNORE INTO config (key, value) VALUES
                ('provider', 'ollama'),
                ('model', 'llama3.2:3b'),
                ('debug', 'false');
        """)
        conn.commit()
    finally:
        conn.close()


def row_to_dict(row) -> dict:
    if row is None:
        return {}
    return dict(zip(row.keys(), row)) if hasattr(row, "keys") else dict(row)


@contextmanager
def db_cursor():
    conn = get_conn()
    conn.row_factory = sqlite3.Row
    try:
        yield conn.cursor()
        conn.commit()
    finally:
        conn.close()
