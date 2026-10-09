"""Heartbeat telemetry routes for Open Guardian Kids.
Implements POST /api/v1/heartbeat for periodic client ping every 60s.
"""

import json
from datetime import datetime, timezone
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Request, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session

try:
    from ..database import get_db
    from ..models import Device, HeartbeatLog
    from ..schemas import HeartbeatRequest, HeartbeatResponse
    from ..security import decode_access_token
except (ImportError, ValueError):
    from server.database import get_db
    from server.models import Device, HeartbeatLog
    from server.schemas import HeartbeatRequest, HeartbeatResponse
    from server.security import decode_access_token

router = APIRouter()
security_scheme = HTTPBearer(auto_error=False)


@router.post("", response_model=HeartbeatResponse, summary="Ghi nhận nhịp tim định kỳ từ Agent")
def receive_heartbeat(
    req: HeartbeatRequest,
    request: Request,
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security_scheme),
    db: Session = Depends(get_db)
) -> HeartbeatResponse:
    """Receive periodic telemetry ping from child agent, update online status and record heartbeat log."""
    device: Optional[Device] = None

    # Method 1: Identify via Bearer Token
    if credentials and credentials.credentials:
        payload = decode_access_token(credentials.credentials)
        if payload:
            device_id = payload.get("device_id")
            if not device_id and "sub" in payload and payload["sub"].startswith("device:"):
                try:
                    device_id = int(payload["sub"].split(":")[1])
                except (ValueError, IndexError):
                    device_id = None

            if device_id:
                device = db.query(Device).filter(Device.id == device_id).first()

    # Method 2: Fallback to device_fingerprint in request body
    if not device and req.device_fingerprint:
        device = db.query(Device).filter(Device.device_fingerprint == req.device_fingerprint).first()

    if not device:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Thiết bị chưa được đăng ký hoặc token không hợp lệ",
            headers={"WWW-Authenticate": "Bearer"},
        )

    now = datetime.now(timezone.utc)

    # Update device online state and last seen
    device.status = "online"
    device.last_seen = now

    # Store telemetry log
    status_str: Optional[str] = None
    if req.status_payload is not None:
        try:
            status_str = json.dumps(req.status_payload)
        except Exception:
            status_str = str(req.status_payload)

    heartbeat_log = HeartbeatLog(
        device_id=device.id,
        timestamp=now,
        status_payload=status_str
    )
    db.add(heartbeat_log)
    db.commit()

    return HeartbeatResponse(
        status="ok",
        policy_version=1,
        server_time=now
    )
