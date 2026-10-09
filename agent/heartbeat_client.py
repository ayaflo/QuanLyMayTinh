"""Heartbeat client for sending periodic telemetry pings to the server.
Complies with Principle NT2 (Data Minimisation): only sends minimal telemetry (status, timestamp).
"""

import time
import threading
from typing import Optional, Dict, Any, Tuple
import requests

try:
    from .config import SERVER_URL, HEARTBEAT_INTERVAL
    from .fingerprint import get_device_fingerprint
    from .storage import load_credentials
except ImportError:
    from config import SERVER_URL, HEARTBEAT_INTERVAL
    from fingerprint import get_device_fingerprint
    from storage import load_credentials


def send_heartbeat(
    access_token: str,
    device_fingerprint: Optional[str] = None,
    server_url: str = SERVER_URL,
    custom_payload: Optional[Dict[str, Any]] = None
) -> Tuple[bool, Optional[Dict[str, Any]]]:
    """Send a single heartbeat telemetry ping to server.

    Args:
        access_token: Bearer JWT access token.
        device_fingerprint: Hardware fingerprint.
        server_url: Base server URL.
        custom_payload: Optional minimal telemetry.

    Returns:
        (success: bool, response_data: Optional[Dict])
    """
    endpoint = f"{server_url}/api/v1/heartbeat"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }

    # Data Minimisation (NT2): Minimal telemetry only (no private URLs or sensitive titles)
    payload = {
        "device_fingerprint": device_fingerprint or get_device_fingerprint(),
        "status_payload": custom_payload or {
            "agent_status": "running",
            "protocol_version": 1
        }
    }

    try:
        response = requests.post(
            endpoint,
            json=payload,
            headers=headers,
            timeout=10
        )
        if response.status_code == 200:
            return True, response.json()
        return False, None
    except requests.exceptions.RequestException:
        return False, None


def run_heartbeat_loop(
    stop_event: Optional[threading.Event] = None,
    interval_seconds: int = HEARTBEAT_INTERVAL,
    server_url: str = SERVER_URL
) -> None:
    """Run continuous heartbeat loop every `interval_seconds` until `stop_event` is set.

    Runs in a dedicated background worker thread.
    """
    if stop_event is None:
        stop_event = threading.Event()

    print(f" [*] Đã khởi động luồng nhịp tim Agent (chu kỳ {interval_seconds}s)...")

    while not stop_event.is_set():
        creds = load_credentials()
        if not creds:
            print(" [!] Chưa có thông tin xác thực. Tạm dừng gửi nhịp tim...")
            # Wait 5 seconds before checking again
            if stop_event.wait(5):
                break
            continue

        token = creds.get("access_token", "")
        success, result = send_heartbeat(access_token=token, server_url=server_url)

        if success:
            policy_ver = result.get("policy_version", 1) if result else 1
            print(f" [♥] Nhịp tim thành công -> Máy chủ xác nhận (Policy v{policy_ver})")
        else:
            print(" [!] Gửi nhịp tim không thành công (máy chủ tạm thời không phản hồi)")

        # Wait for next cycle or exit signal
        if stop_event.wait(interval_seconds):
            break

    print(" [*] Luồng nhịp tim đã dừng an toàn.")


def start_heartbeat_thread(
    interval_seconds: int = HEARTBEAT_INTERVAL,
    server_url: str = SERVER_URL
) -> Tuple[threading.Thread, threading.Event]:
    """Start the heartbeat loop in a background daemon thread."""
    stop_event = threading.Event()
    thread = threading.Thread(
        target=run_heartbeat_loop,
        args=(stop_event, interval_seconds, server_url),
        daemon=True,
        name="OGK-HeartbeatThread"
    )
    thread.start()
    return thread, stop_event
