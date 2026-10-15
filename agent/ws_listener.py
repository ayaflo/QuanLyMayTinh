"""WebSocket listener client for Open Guardian Kids.
Maintains persistent bidirectional connection with server to receive emergency commands (< 5s).
"""

import time
import json
import threading
from typing import Optional, Callable, Dict, Any
import websocket

try:
    from .config import SERVER_URL, DB_PATH
    from .storage import load_credentials
except ImportError:
    from config import SERVER_URL, DB_PATH
    from storage import load_credentials


class WebSocketListener:
    """Listens for real-time push commands from parent dashboard via WebSocket."""

    def __init__(
        self,
        server_url: str = SERVER_URL,
        db_path: str = DB_PATH,
        on_command: Optional[Callable[[str, Dict[str, Any]], None]] = None
    ):
        self.server_url = server_url
        self.db_path = db_path
        self.on_command = on_command

        self.running = False
        self._thread: Optional[threading.Thread] = None
        self._ws: Optional[websocket.WebSocket] = None

    def start(self) -> None:
        """Start WebSocket listener in a background thread."""
        if self.running:
            return
        self.running = True
        self._thread = threading.Thread(target=self._run_loop, daemon=True, name="WSListener")
        self._thread.start()

    def stop(self) -> None:
        """Stop WebSocket listener."""
        self.running = False
        if self._ws:
            try:
                self._ws.close()
            except Exception:
                pass

    def _get_ws_url(self, device_id: int, access_token: str) -> str:
        """Convert HTTP/HTTPS server URL to WS/WSS URL."""
        base = self.server_url
        if base.startswith("https://"):
            ws_base = "wss://" + base[8:]
        elif base.startswith("http://"):
            ws_base = "ws://" + base[7:]
        else:
            ws_base = f"ws://{base}"

        return f"{ws_base}/ws/device/{device_id}?token={access_token}"

    def _run_loop(self) -> None:
        """Continuous connection and command processing loop with auto-reconnect."""
        while self.running:
            creds = load_credentials(self.db_path)
            if not creds:
                time.sleep(5.0)
                continue

            device_id = creds["device_id"]
            access_token = creds["access_token"]
            ws_url = self._get_ws_url(device_id, access_token)

            try:
                print(f"[WS] Connecting to {ws_url}...")
                self._ws = websocket.create_connection(ws_url, timeout=15)
                print("[WS] Connected successfully! Ready for emergency commands (< 5s).")

                while self.running:
                    msg_text = self._ws.recv()
                    if not msg_text:
                        break

                    try:
                        data = json.loads(msg_text)
                        action = data.get("action")
                        payload = data.get("payload", {})
                        print(f"[WS] Received emergency command: {action} (payload={payload})")

                        if self.on_command and action:
                            self.on_command(action, payload)
                    except Exception as err:
                        print(f"[WS] Error processing message: {err}")

            except Exception as e:
                if self.running:
                    print(f"[WS] Connection dropped: {e}. Reconnecting in 5s...")
                    time.sleep(5.0)
            finally:
                if self._ws:
                    try:
                        self._ws.close()
                    except Exception:
                        pass
                    self._ws = None
