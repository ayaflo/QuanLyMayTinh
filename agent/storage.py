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
        conn.execute("""
            CREATE TABLE IF NOT EXISTS policy_cache (
                id INTEGER PRIMARY KEY CHECK (id = 1),
                version INTEGER NOT NULL,
                weekday_quota_minutes INTEGER NOT NULL,
                weekend_quota_minutes INTEGER NOT NULL,
                schedule_matrix TEXT NOT NULL,
                hmac_signature TEXT NOT NULL,
                updated_at TEXT NOT NULL
            );
        """)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS daily_usage (
                usage_date TEXT PRIMARY KEY,
                used_seconds INTEGER NOT NULL DEFAULT 0,
                bonus_minutes INTEGER NOT NULL DEFAULT 0,
                is_locked INTEGER NOT NULL DEFAULT 0,
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


# ============================================================================
# Week 2 (Version 0.2): Policy Cache & Daily Usage Persistence
# ============================================================================

def save_policy_cache(policy_data: Dict[str, Any], db_path: str = DB_PATH) -> None:
    """Save or update local cached policy with HMAC signature."""
    conn = _get_connection(db_path)
    now_str = datetime.now(timezone.utc).isoformat()
    with conn:
        conn.execute("""
            INSERT OR REPLACE INTO policy_cache (
                id, version, weekday_quota_minutes, weekend_quota_minutes,
                schedule_matrix, hmac_signature, updated_at
            ) VALUES (1, ?, ?, ?, ?, ?, ?);
        """, (
            policy_data["version"],
            policy_data["weekday_quota_minutes"],
            policy_data["weekend_quota_minutes"],
            policy_data["schedule_matrix"],
            policy_data["hmac_signature"],
            now_str
        ))
    conn.close()


def load_policy_cache(db_path: str = DB_PATH) -> Optional[Dict[str, Any]]:
    """Load cached policy from local database, or return None if not cached yet."""
    conn = _get_connection(db_path)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT version, weekday_quota_minutes, weekend_quota_minutes, schedule_matrix, hmac_signature, updated_at
        FROM policy_cache WHERE id = 1;
    """)
    row = cursor.fetchone()
    conn.close()

    if not row:
        return None

    return {
        "version": row["version"],
        "weekday_quota_minutes": row["weekday_quota_minutes"],
        "weekend_quota_minutes": row["weekend_quota_minutes"],
        "schedule_matrix": row["schedule_matrix"],
        "hmac_signature": row["hmac_signature"],
        "updated_at": row["updated_at"]
    }


def get_daily_usage(date_str: str, db_path: str = DB_PATH) -> Dict[str, Any]:
    """Get screen time usage record for given date (YYYY-MM-DD)."""
    conn = _get_connection(db_path)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT usage_date, used_seconds, bonus_minutes, is_locked, updated_at
        FROM daily_usage WHERE usage_date = ?;
    """, (date_str,))
    row = cursor.fetchone()
    conn.close()

    if not row:
        return {
            "usage_date": date_str,
            "used_seconds": 0,
            "bonus_minutes": 0,
            "is_locked": 0,
            "updated_at": datetime.now(timezone.utc).isoformat()
        }

    return {
        "usage_date": row["usage_date"],
        "used_seconds": row["used_seconds"],
        "bonus_minutes": row["bonus_minutes"],
        "is_locked": row["is_locked"],
        "updated_at": row["updated_at"]
    }


def update_daily_usage(
    date_str: str,
    used_seconds: int,
    bonus_minutes: int = 0,
    is_locked: int = 0,
    db_path: str = DB_PATH
) -> None:
    """Update or insert daily usage record in local SQLite database."""
    conn = _get_connection(db_path)
    now_str = datetime.now(timezone.utc).isoformat()
    with conn:
        conn.execute("""
            INSERT INTO daily_usage (usage_date, used_seconds, bonus_minutes, is_locked, updated_at)
            VALUES (?, ?, ?, ?, ?)
            ON CONFLICT(usage_date) DO UPDATE SET
                used_seconds = excluded.used_seconds,
                bonus_minutes = excluded.bonus_minutes,
                is_locked = excluded.is_locked,
                updated_at = excluded.updated_at;
        """, (date_str, used_seconds, bonus_minutes, is_locked, now_str))
    conn.close()
