"""Local SQLite storage for persisting client credentials.
Manages device_id, access_token, and refresh_token in agent_cache.db.
"""

import sqlite3
from datetime import datetime, timezone
from typing import Optional, Dict, Any

try:
    from .config import DB_PATH
except ImportError:
    from config import DB_PATH


def _get_connection(db_path: str = DB_PATH) -> sqlite3.Connection:
    """Initialize connection and credentials table if not exists."""
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    with conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS credentials (
                id INTEGER PRIMARY KEY CHECK (id = 1),
                device_id INTEGER NOT NULL,
                access_token TEXT NOT NULL,
                refresh_token TEXT NOT NULL,
                device_name TEXT,
                updated_at TEXT NOT NULL
            );
        """)
    return conn


def save_credentials(
    device_id: int,
    access_token: str,
    refresh_token: str,
    device_name: Optional[str] = "Windows PC",
    db_path: str = DB_PATH
) -> None:
    """Save or replace paired device credentials in local SQLite database."""
    conn = _get_connection(db_path)
    now_str = datetime.now(timezone.utc).isoformat()
    with conn:
        conn.execute("""
            INSERT OR REPLACE INTO credentials (id, device_id, access_token, refresh_token, device_name, updated_at)
            VALUES (1, ?, ?, ?, ?, ?);
        """, (device_id, access_token, refresh_token, device_name, now_str))
    conn.close()


def load_credentials(db_path: str = DB_PATH) -> Optional[Dict[str, Any]]:
    """Load credentials from local database, or return None if device has not paired."""
    conn = _get_connection(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT device_id, access_token, refresh_token, device_name, updated_at FROM credentials WHERE id = 1;")
    row = cursor.fetchone()
    conn.close()

    if not row:
        return None

    return {
        "device_id": row["device_id"],
        "access_token": row["access_token"],
        "refresh_token": row["refresh_token"],
        "device_name": row["device_name"],
        "updated_at": row["updated_at"]
    }


def clear_credentials(db_path: str = DB_PATH) -> None:
    """Clear credentials table (used for reset or unpairing)."""
    conn = _get_connection(db_path)
    with conn:
        conn.execute("DELETE FROM credentials WHERE id = 1;")
    conn.close()
