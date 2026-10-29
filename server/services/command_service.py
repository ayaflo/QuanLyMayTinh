"""Emergency command dispatch service for Open Guardian Kids.
Handles immediate command creation, WebSocket delivery (< 5s), and audit logging.
"""

import json
from datetime import datetime, timezone
from typing import Optional, Dict, Any
from sqlalchemy.orm import Session

try:
    from ..models import Device, DeviceCommand, AuditLog
    from .connection_manager import ws_manager
except (ImportError, ValueError):
    from server.models import Device, DeviceCommand, AuditLog
    from server.services.connection_manager import ws_manager


def utc_now():
    """Return timezone-aware current UTC time."""
    return datetime.now(timezone.utc)


async def dispatch_command(
    db: Session,
    device_id: int,
    parent_id: Optional[int],
    command_type: str,
    minutes: Optional[int] = 15,
    countdown: Optional[int] = 30,
    ip_address: Optional[str] = None,
    extra_payload: Optional[Dict[str, Any]] = None
) -> DeviceCommand:
    """Create, persist, and dispatch an emergency command via WebSocket (< 5s)."""
    payload_dict: Dict[str, Any] = {}
    if command_type == "add_time":
        payload_dict["minutes"] = minutes or 15
    elif command_type == "lock_now":
        payload_dict["countdown"] = countdown if countdown is not None else 30

    if extra_payload:
        payload_dict.update(extra_payload)

    payload_json = json.dumps(payload_dict) if payload_dict else None

    # 1. Create DB record
    cmd = DeviceCommand(
        device_id=device_id,
        command_type=command_type,
        payload=payload_json,
        status="pending",
        created_at=utc_now()
    )
    db.add(cmd)

    # 2. Record audit log (NT5)
    audit = AuditLog(
        parent_id=parent_id,
        device_id=device_id,
        action=f"command:{command_type}",
        new_value=payload_json or command_type,
        ip_address=ip_address,
        created_at=utc_now()
    )
    db.add(audit)
    db.commit()
    db.refresh(cmd)

    # 3. Dispatch real-time via WebSocket (< 5s)
    ws_msg = {
        "action": command_type,
        "payload": payload_dict,
        "command_id": cmd.id,
        "timestamp": utc_now().isoformat()
    }
    sent = await ws_manager.send_command(device_id, ws_msg)
    if sent:
        cmd.status = "delivered"
        cmd.delivered_at = utc_now()
        db.commit()
        db.refresh(cmd)

    return cmd
