"""WebSocket endpoint for Open Guardian Kids real-time channel.
Maintains persistent bidirectional channel with child agents for emergency actions (< 5s).
"""

from typing import Optional
from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Query, status
from sqlalchemy.orm import Session

try:
    from ..database import SessionLocal
    from ..models import Device
    from ..security import decode_access_token
    from ..services.connection_manager import ws_manager
except (ImportError, ValueError):
    from server.database import SessionLocal
    from server.models import Device
    from server.security import decode_access_token
    from server.services.connection_manager import ws_manager

router = APIRouter()


@router.websocket("/device/{device_id}")
async def websocket_device_endpoint(
    websocket: WebSocket,
    device_id: int,
    token: Optional[str] = Query(None, description="Device access token")
):
    """Maintain real-time WebSocket connection with child agent."""
    # 1. Authenticate connection
    db: Session = SessionLocal()
    authenticated = False
    try:
        if token:
            payload = decode_access_token(token)
            if payload:
                token_dev_id = payload.get("device_id")
                if not token_dev_id and "sub" in payload and payload["sub"].startswith("device:"):
                    try:
                        token_dev_id = int(payload["sub"].split(":")[1])
                    except (ValueError, IndexError):
                        token_dev_id = None
                if token_dev_id == device_id:
                    authenticated = True

        if not authenticated:
            # Check if device exists in DB
            dev = db.query(Device).filter(Device.id == device_id).first()
            if not dev:
                await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
                return
    finally:
        db.close()

    # 2. Register connection
    await ws_manager.connect(device_id, websocket)

    try:
        while True:
            # Keep listening for client keep-alive pings / command receipts
            data = await websocket.receive_text()
            if data == "ping":
                await websocket.send_text("pong")
    except WebSocketDisconnect:
        ws_manager.disconnect(device_id)
    except Exception:
        ws_manager.disconnect(device_id)
