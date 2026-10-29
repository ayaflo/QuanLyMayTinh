"""Local SQLite storage for persisting client credentials.
Manages device_id, access_token, and refresh_token in agent_cache.db.
"""

import os
import sqlite3
from datetime import datetime, timezone
from typing import Optional, Dict, Any

try:
    from .config import DB_PATH
except ImportError:
    from config import DB_PATH


def _get_connection(db_path: str = DB_PATH) -> sqlite3.Connection:
    """Initialize connection and credentials table if not exists."""
    db_dir = os.path.dirname(os.path.abspath(db_path))
    if db_dir:
        os.makedirs(db_dir, exist_ok=True)
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
        conn.execute("""
            CREATE TABLE IF NOT EXISTS dns_rules_cache (
                domain TEXT PRIMARY KEY,
                action TEXT NOT NULL,
                is_permanent_whitelist INTEGER NOT NULL DEFAULT 0,
                category TEXT
            );
        """)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS app_rules_cache (
                sha256_hash TEXT PRIMARY KEY,
                app_name TEXT NOT NULL,
                action TEXT NOT NULL,
                description TEXT
            );
        """)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS pending_events (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                idempotency_key TEXT UNIQUE NOT NULL,
                ts TEXT NOT NULL,
                device_id INTEGER NOT NULL,
                child_id INTEGER,
                type TEXT NOT NULL,
                subject TEXT NOT NULL,
                duration_sec INTEGER NOT NULL DEFAULT 0,
                policy_id INTEGER
            );
        """)
    return conn


def init_db(db_path: str = DB_PATH) -> None:
    """Explicitly initialize local SQLite schema if needed."""
    conn = _get_connection(db_path)
    conn.close()


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


# ============================================================================
# Week 3 (Version 0.3): DNS Rules, App Rules & Offline Event Buffer (T3_028, T3_042)
# ============================================================================

def save_dns_rules_cache(rules: list[Dict[str, Any]], db_path: str = DB_PATH) -> None:
    """Persist domain rules into local SQLite cache for offline DNS resolution."""
    conn = _get_connection(db_path)
    with conn:
        conn.execute("DELETE FROM dns_rules_cache;")
        conn.executemany("""
            INSERT OR REPLACE INTO dns_rules_cache (domain, action, is_permanent_whitelist, category)
            VALUES (?, ?, ?, ?);
        """, [
            (
                r["domain"].lower().strip(),
                r.get("action", "block"),
                1 if r.get("is_permanent_whitelist") else 0,
                r.get("category", "")
            )
            for r in rules
        ])
    conn.close()


def load_dns_rules_cache(db_path: str = DB_PATH) -> Dict[str, Any]:
    """Load cached domain rules for rapid lookup by the DNS proxy."""
    conn = _get_connection(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT domain, action, is_permanent_whitelist FROM dns_rules_cache;")
    rows = cursor.fetchall()
    conn.close()

    blocked = set()
    allowed = set()
    whitelist = set()

    for r in rows:
        dom = r["domain"]
        if r["is_permanent_whitelist"] == 1:
            whitelist.add(dom)
            allowed.add(dom)
        elif r["action"] == "block":
            blocked.add(dom)
        else:
            allowed.add(dom)

    return {
        "blocked_domains": blocked,
        "allowed_domains": allowed,
        "permanent_whitelist": whitelist
    }


def save_app_rules_cache(rules: list[Dict[str, Any]], db_path: str = DB_PATH) -> None:
    """Persist SHA-256 app control rules into local SQLite cache."""
    conn = _get_connection(db_path)
    with conn:
        conn.execute("DELETE FROM app_rules_cache;")
        conn.executemany("""
            INSERT OR REPLACE INTO app_rules_cache (sha256_hash, app_name, action, description)
            VALUES (?, ?, ?, ?);
        """, [
            (
                r["sha256"].lower().strip(),
                r.get("name", ""),
                r.get("action", "block"),
                r.get("description", "")
            )
            for r in rules
        ])
    conn.close()


def load_app_rules_cache(db_path: str = DB_PATH) -> Dict[str, Dict[str, str]]:
    """Load cached SHA-256 app rules map: {sha256_hash: {name, action, description}}."""
    conn = _get_connection(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT sha256_hash, app_name, action, description FROM app_rules_cache;")
    rows = cursor.fetchall()
    conn.close()

    return {
        r["sha256_hash"]: {
            "name": r["app_name"],
            "action": r["action"],
            "description": r["description"] or ""
        }
        for r in rows
    }


def add_pending_event(event: Dict[str, Any], db_path: str = DB_PATH) -> None:
    """Buffer an activity event in offline storage until pushed to server (T3_042)."""
    conn = _get_connection(db_path)
    with conn:
        conn.execute("""
            INSERT OR IGNORE INTO pending_events (
                idempotency_key, ts, device_id, child_id, type, subject, duration_sec, policy_id
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?);
        """, (
            event["idempotency_key"],
            event["ts"],
            event["device_id"],
            event.get("child_id"),
            event["type"],
            event["subject"],
            event.get("duration_sec", 0),
            event.get("policy_id")
        ))
    conn.close()


def get_pending_events(limit: int = 200, db_path: str = DB_PATH) -> list[Dict[str, Any]]:
    """Retrieve buffered events to send in batch."""
    conn = _get_connection(db_path)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT idempotency_key, ts, device_id, child_id, type, subject, duration_sec, policy_id
        FROM pending_events ORDER BY id ASC LIMIT ?;
    """, (limit,))
    rows = cursor.fetchall()
    conn.close()

    return [
        {
            "idempotency_key": r["idempotency_key"],
            "ts": r["ts"],
            "device_id": r["device_id"],
            "child_id": r["child_id"],
            "type": r["type"],
            "subject": r["subject"],
            "duration_sec": r["duration_sec"],
            "policy_id": r["policy_id"]
        }
        for r in rows
    ]


def delete_pending_events(keys: list[str], db_path: str = DB_PATH) -> None:
    """Remove successfully ingested events from local buffer."""
    if not keys:
        return
    conn = _get_connection(db_path)
    with conn:
        placeholders = ",".join("?" for _ in keys)
        conn.execute(f"DELETE FROM pending_events WHERE idempotency_key IN ({placeholders});", keys)
    conn.close()


def purge_local_data(db_path: str = DB_PATH) -> Dict[str, int]:
    """Wipe all cached activity events, daily usage, and local rule caches (Right to Erasure / Decree 13/2023)."""
    conn = _get_connection(db_path)
    with conn:
        c1 = conn.execute("DELETE FROM pending_events;").rowcount
        c2 = conn.execute("DELETE FROM daily_usage;").rowcount
        c3 = conn.execute("DELETE FROM dns_rules_cache;").rowcount
        c4 = conn.execute("DELETE FROM app_rules_cache;").rowcount
    conn.close()
    return {
        "pending_events_deleted": c1,
        "daily_usage_deleted": c2,
        "dns_rules_deleted": c3,
        "app_rules_deleted": c4
    }


