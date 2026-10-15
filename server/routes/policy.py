"""Policy routes for Open Guardian Kids.
Provides endpoints for retrieving and updating screen-time policies (F1 & F4).
"""

from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Request, Query, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session

try:
    from ..database import get_db
    from ..models import Parent, Device, Policy
    from ..schemas import PolicyUpdate, PolicyResponse
    from ..security import decode_access_token
    from ..services.policy_service import get_or_create_default_policy, update_policy_and_log_audit
    from ..services.connection_manager import ws_manager
except (ImportError, ValueError):
    from server.database import get_db
    from server.models import Parent, Device, Policy
    from server.schemas import PolicyUpdate, PolicyResponse
    from server.security import decode_access_token
    from server.services.policy_service import get_or_create_default_policy, update_policy_and_log_audit
    from server.services.connection_manager import ws_manager

router = APIRouter()
security_scheme = HTTPBearer(auto_error=False)


def _get_device_from_token(credentials: Optional[HTTPAuthorizationCredentials], db: Session) -> Optional[Device]:
    """Helper to extract device from Authorization Bearer token."""
    if not credentials or not credentials.credentials:
        return None
    payload = decode_access_token(credentials.credentials)
    if not payload:
        return None
    device_id = payload.get("device_id")
    if not device_id and "sub" in payload and payload["sub"].startswith("device:"):
        try:
            device_id = int(payload["sub"].split(":")[1])
        except (ValueError, IndexError):
            return None
    if device_id:
        return db.query(Device).filter(Device.id == device_id).first()
    return None


def _get_parent_from_request(request: Request, credentials: Optional[HTTPAuthorizationCredentials], db: Session) -> Optional[Parent]:
    """Helper to extract authenticated parent from Cookie or Bearer token."""
    token = request.cookies.get("access_token")
    if not token and credentials and credentials.credentials:
        token = credentials.credentials
    if not token:
        return None

    payload = decode_access_token(token)
    if not payload:
        return None
    parent_id = payload.get("parent_id")
    if not parent_id and "sub" in payload and payload["sub"].startswith("parent:"):
        try:
            parent_id = int(payload["sub"].split(":")[1])
        except (ValueError, IndexError):
            return None
    if parent_id:
        return db.query(Parent).filter(Parent.id == parent_id).first()
    return None


@router.get("", response_model=PolicyResponse, summary="Lấy chính sách thời gian mới nhất (Agent hoặc Parent)")
def get_policy(
    request: Request,
    device_id: Optional[int] = Query(None, description="ID thiết bị (nếu phụ huynh gọi)"),
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security_scheme),
    db: Session = Depends(get_db)
) -> PolicyResponse:
    """Retrieve policy for a device. Devices authenticate via token; parents pass device_id."""
    target_device_id = device_id

    # If called by Agent
    agent_device = _get_device_from_token(credentials, db)
    if agent_device:
        target_device_id = agent_device.id
    elif not target_device_id:
        # Fallback to parent check
        parent = _get_parent_from_request(request, credentials, db)
        if not parent:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Yêu cầu xác thực tài khoản phụ huynh hoặc thiết bị",
                headers={"WWW-Authenticate": "Bearer"},
            )
        # If parent didn't specify device_id, pick their first device if any
        first_dev = db.query(Device).filter(Device.parent_id == parent.id).first()
        if not first_dev:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Chưa có thiết bị nào được ghép đôi")
        target_device_id = first_dev.id

    device = db.query(Device).filter(Device.id == target_device_id).first()
    if not device:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Không tìm thấy thiết bị")

    policy = get_or_create_default_policy(db, device.id)
    return policy


@router.post("", response_model=PolicyResponse, summary="Cập nhật chính sách thời gian (Phụ huynh)")
async def update_policy(
    update_data: PolicyUpdate,
    request: Request,
    device_id: int = Query(..., description="ID thiết bị cần áp dụng chính sách"),
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security_scheme),
    db: Session = Depends(get_db)
) -> PolicyResponse:
    """Update device policy, increment version, recalculate HMAC, and notify Agent via WebSocket."""
    parent = _get_parent_from_request(request, credentials, db)
    if not parent:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Chỉ phụ huynh mới có quyền cập nhật chính sách",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Anti-IDOR check: verify device ownership
    device = db.query(Device).filter(Device.id == device_id, Device.parent_id == parent.id).first()
    if not device:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Bạn không có quyền chỉnh sửa thiết bị này"
        )

    client_ip = request.client.host if request.client else None
    updated_policy = update_policy_and_log_audit(
        db=db,
        device_id=device.id,
        parent_id=parent.id,
        update_data=update_data,
        ip_address=client_ip
    )

    # Notify Agent in real-time via WebSocket if connected
    await ws_manager.send_command(device.id, {
        "action": "policy_updated",
        "version": updated_policy.version,
        "payload": {
            "weekday_quota_minutes": updated_policy.weekday_quota_minutes,
            "weekend_quota_minutes": updated_policy.weekend_quota_minutes
        }
    })

    return updated_policy
