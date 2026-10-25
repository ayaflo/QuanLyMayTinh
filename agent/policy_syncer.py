"""Policy synchronization client for Open Guardian Kids.
Pulls latest policy from server, validates HMAC-SHA256 signature, and updates local cache.
"""

import os
import hmac
import hashlib
from typing import Optional, Dict, Any
import requests

try:
    from .config import SERVER_URL, DB_PATH, REQUEST_TIMEOUT
    from .storage import load_credentials, save_policy_cache, load_policy_cache
except ImportError:
    from config import SERVER_URL, DB_PATH, REQUEST_TIMEOUT
    from storage import load_credentials, save_policy_cache, load_policy_cache

SECRET_KEY = os.getenv("SECRET_KEY", "change-this-secret-key-in-production")


def verify_hmac(
    device_id: int,
    version: int,
    weekday_quota: int,
    weekend_quota: int,
    schedule_matrix: str,
    signature: str
) -> bool:
    """Verify policy HMAC-SHA256 signature locally on Agent."""
    canonical_str = f"{device_id}:{version}:{weekday_quota}:{weekend_quota}:{schedule_matrix}"
    expected = hmac.new(
        SECRET_KEY.encode("utf-8"),
        canonical_str.encode("utf-8"),
        hashlib.sha256
    ).hexdigest()
    return hmac.compare_digest(expected, signature)


def sync_policy_from_server(server_url: str = SERVER_URL, db_path: str = DB_PATH) -> Optional[Dict[str, Any]]:
    """Fetch policy from GET /api/v1/policy, verify integrity, and update local cache."""
    creds = load_credentials(db_path)
    if not creds:
        return None

    device_id = creds["device_id"]
    access_token = creds["access_token"]

    url = f"{server_url}/api/v1/policy"
    headers = {"Authorization": f"Bearer {access_token}"}

    try:
        response = requests.get(url, headers=headers, timeout=REQUEST_TIMEOUT)
        if response.status_code != 200:
            print(f"[POLICY] Failed to fetch policy: HTTP {response.status_code}")
            return None

        policy_data = response.json()

        # Validate HMAC signature (F4 Anti-Tamper)
        is_valid = verify_hmac(
            device_id=device_id,
            version=policy_data["version"],
            weekday_quota=policy_data["weekday_quota_minutes"],
            weekend_quota=policy_data["weekend_quota_minutes"],
            schedule_matrix=policy_data["schedule_matrix"],
            signature=policy_data["hmac_signature"]
        )

        if not is_valid:
            print("[POLICY] WARNING: HMAC signature verification failed! Rejecting corrupted policy.")
            return None

        # Save to local cache
        save_policy_cache(policy_data, db_path)
        print(f"[POLICY] Synced policy v{policy_data['version']} successfully (HMAC Verified).")
        return policy_data
    except Exception as e:
        print(f"[POLICY] Error syncing policy: {e}")
        return None
