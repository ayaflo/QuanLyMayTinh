"""WebSocket endpoint for Open Guardian Kids real-time channel.
Maintains persistent bidirectional channel with child agents for emergency actions (< 5s).
"""

import json
from datetime import datetime, timezone
from typing import Optional
from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Query, status
from sqlalchemy.orm import Session

try:
    from ..database import SessionLocal
    from ..models import Device, DeviceCommand
    from ..security import decode_access_token
    from ..services.connection_manager import ws_manager
except (ImportError, ValueError):
    from server.database import SessionLocal
    from server.models import Device, DeviceCommand
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

    # 3. Deliver any pending emergency commands immediately
    db = SessionLocal()
    try:
        pending_cmds = db.query(DeviceCommand).filter(
            DeviceCommand.device_id == device_id,
            DeviceCommand.status == "pending"
        ).order_by(DeviceCommand.created_at.asc()).all()

        now = datetime.now(timezone.utc)
        for cmd in pending_cmds:
            payload_dict = json.loads(cmd.payload) if cmd.payload else {}
            ws_msg = {
                "action": cmd.command_type,
                "payload": payload_dict,
                "command_id": cmd.id,
                "timestamp": now.isoformat()
            }
            await websocket.send_text(json.dumps(ws_msg))
            cmd.status = "delivered"
            cmd.delivered_at = now
        if pending_cmds:
            db.commit()
    except Exception as e:
        print(f"[WS] Error delivering pending commands to device #{device_id}: {e}")
    finally:
        db.close()

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
