"""Offline Event Buffer & Telemetry Collector for Open Guardian Kids (F3 & NT2).
Buffers minimal activity events locally with UUID v4 idempotency keys,
and pushes them in batches to the Central Server when network connectivity is available.
"""

import time
import uuid
import threading
import logging
import requests
from datetime import datetime, timezone
from typing import Optional, Callable, Dict, Any

try:
    from .storage import add_pending_event, get_pending_events, delete_pending_events, load_credentials
    from .config import SERVER_URL, REQUEST_TIMEOUT
except ImportError:
    from storage import add_pending_event, get_pending_events, delete_pending_events, load_credentials
    from config import SERVER_URL, REQUEST_TIMEOUT

logger = logging.getLogger("OGK_EventCollector")


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


class EventCollector:
    """Manages local event buffering and asynchronous batch upload to Server (F3)."""

    def __init__(
        self,
        server_url: str = SERVER_URL,
        device_id_provider: Optional[Callable[[], Optional[int]]] = None,
        token_provider: Optional[Callable[[], Optional[str]]] = None,
        sync_interval_sec: float = 15.0,
        batch_size: int = 100
    ):
        self.server_url = server_url.rstrip("/")
        self.device_id_provider = device_id_provider
        self.token_provider = token_provider
        self.sync_interval_sec = sync_interval_sec
        self.batch_size = batch_size

        self._running = False
        self._thread: Optional[threading.Thread] = None

    def record_event(
        self,
        event_type: str,
        subject: str,
        duration_sec: int = 0,
        policy_id: Optional[int] = None
    ) -> str:
        """Buffer a minimal telemetry event into local SQLite (NT2 & F3).
        Enforces minimal disclosure: subject is strictly FQDN domain or app executable name.
        """
        device_id = self.device_id_provider() if self.device_id_provider else None
        if not device_id:
            creds = load_credentials()
            device_id = creds["device_id"] if creds else 1

        clean_subject = subject.split("/")[0].strip() if "/" in subject else subject.strip()
        idem_key = str(uuid.uuid4())

        event_payload = {
            "idempotency_key": idem_key,
            "ts": utc_now_iso(),
            "device_id": device_id,
            "child_id": None,
            "type": event_type,
            "subject": clean_subject,
            "duration_sec": max(0, int(duration_sec)),
            "policy_id": policy_id
        }

        try:
            add_pending_event(event_payload)
            logger.debug(f"[EVENT BUFFERED] {event_type} - {clean_subject} ({idem_key[:8]})")
        except Exception as e:
            logger.error(f"Failed to buffer event: {e}")

        return idem_key

    def flush_batch(self) -> int:
        """Attempt to upload a batch of pending events to the Server (T3_043).
        Returns count of successfully uploaded events.
        """
        events = get_pending_events(limit=self.batch_size)
        if not events:
            return 0

        token = self.token_provider() if self.token_provider else None
        if not token:
            creds = load_credentials()
            token = creds["access_token"] if creds else None

        headers = {"Content-Type": "application/json"}
        if token:
            headers["Authorization"] = f"Bearer {token}"

        target_url = f"{self.server_url}/api/v1/events/batch"
        try:
            resp = requests.post(target_url, json={"events": events}, headers=headers, timeout=REQUEST_TIMEOUT)
            if resp.status_code == 200:
                keys = [ev["idempotency_key"] for ev in events]
                delete_pending_events(keys)
                logger.info(f"[BATCH SYNC] Successfully uploaded {len(events)} events to server.")
                return len(events)
            else:
                logger.warning(f"[BATCH SYNC] Server returned status {resp.status_code}: {resp.text[:100]}")
        except Exception as e:
            logger.debug(f"[BATCH SYNC] Server unreachable (offline buffer active): {e}")

        return 0

    def _sync_loop(self):
        """Periodic background sync loop."""
        while self._running:
            try:
                self.flush_batch()
            except Exception as e:
                logger.error(f"Error in EventCollector sync loop: {e}")
            time.sleep(self.sync_interval_sec)

    def start(self):
        """Start background event sync thread."""
        if self._running:
            return
        self._running = True
        self._thread = threading.Thread(target=self._sync_loop, daemon=True, name="OGK_EventCollector")
        self._thread.start()
        logger.info("[*] EventCollector background sync thread started.")

    def stop(self):
        """Stop background event sync thread and attempt final flush."""
        self._running = False
        try:
            self.flush_batch()
        except Exception:
            pass
        if self._thread and self._thread.is_alive():
            self._thread.join(timeout=1.5)
        logger.info("[*] EventCollector stopped.")
