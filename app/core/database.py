"""Database connection and helper functions."""
import sqlite3
from typing import Optional
from app.config import settings


def init_db():
    """Initialize the database with required tables."""
    conn = sqlite3.connect(settings.database_url)
    c = conn.cursor()
    c.execute(
        "CREATE TABLE IF NOT EXISTS sessions (shop TEXT PRIMARY KEY, token TEXT)"
    )
    conn.commit()
    conn.close()


def save_token(shop: str, token: str):
    """Save or update a shop's access token."""
    conn = sqlite3.connect(settings.database_url)
    c = conn.cursor()
    c.execute(
        "INSERT OR REPLACE INTO sessions (shop, token) VALUES (?, ?)",
        (shop, token)
    )
    conn.commit()
    conn.close()


def get_token(shop: str) -> Optional[str]:
    """Retrieve a shop's access token."""
    conn = sqlite3.connect(settings.database_url)
    c = conn.cursor()
    c.execute("SELECT token FROM sessions WHERE shop=?", (shop,))
    row = c.fetchone()
    conn.close()
    return row[0] if row else None

