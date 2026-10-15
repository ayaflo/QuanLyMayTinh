"""WebSocket Connection Manager for Open Guardian Kids.
Maintains active real-time connections to child agents for emergency command dispatch (< 5s).
"""

import json
from typing import Dict, Optional, Any
from fastapi import WebSocket


class ConnectionManager:
    """Manages active WebSocket connections for enrolled child devices."""

    def __init__(self):
        # Maps device_id -> active WebSocket connection
        self.active_connections: Dict[int, WebSocket] = {}

    async def connect(self, device_id: int, websocket: WebSocket) -> None:
        """Accept incoming WebSocket connection and register device."""
        await websocket.accept()
        self.active_connections[device_id] = websocket

    def disconnect(self, device_id: int) -> None:
        """Unregister a disconnected device."""
        if device_id in self.active_connections:
            del self.active_connections[device_id]

    def is_connected(self, device_id: int) -> bool:
        """Check if device is currently connected via WebSocket."""
        return device_id in self.active_connections

    async def send_command(self, device_id: int, message: Dict[str, Any]) -> bool:
        """Send emergency command JSON payload to device in real-time (< 5s).
        
        Returns True if successfully sent, False if device is not connected.
        """
        websocket = self.active_connections.get(device_id)
        if not websocket:
            return False

        try:
            await websocket.send_text(json.dumps(message))
            return True
        except Exception:
            self.disconnect(device_id)
            return False


# Global singleton instance
ws_manager = ConnectionManager()
