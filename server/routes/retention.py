"""Data Retention & Right to Erasure API routes (Decree 13/2023/ND-CP).
Allows parents to invoke their statutory Right to Erasure ("Xóa toàn bộ dữ liệu của con tôi").
"""

from typing import Optional, Dict, Any
from fastapi import APIRouter, Depends, HTTPException, Request, Path, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session

try:
    from ..database import get_db
    from ..models import Parent, Device
    from ..schemas import EraseDeviceDataRequest
    from ..security import decode_access_token, verify_password
    from ..services.retention_service import erase_device_data
except (ImportError, ValueError):
    from server.database import get_db
    from server.models import Parent, Device
    from server.schemas import EraseDeviceDataRequest
    from server.security import decode_access_token, verify_password
    from server.services.retention_service import erase_device_data

router = APIRouter(prefix="/api/v1/devices", tags=["Retention"])
security_scheme = HTTPBearer(auto_error=False)


def _get_parent_from_request(
    request: Request,
    credentials: Optional[HTTPAuthorizationCredentials],
    db: Session
) -> Optional[Parent]:
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


@router.delete("/{device_id}/data", summary="Thực hiện Quyền được xóa dữ liệu của trẻ (Nghị định 13/2023/NĐ-CP)")
async def erase_child_data(
    req_in: EraseDeviceDataRequest,
    request: Request,
    device_id: int = Path(..., description="ID thiết bị cần xóa toàn bộ dữ liệu"),
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security_scheme),
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """Permanently delete all historical events, telemetry, and requests of a child device.

    Requires parent password confirmation and verifies device ownership.
    Dispatches a real-time command via WebSocket to purge Agent local storage.
    """
    parent = _get_parent_from_request(request, credentials, db)
    if not parent:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Yêu cầu đăng nhập tài khoản phụ huynh để thực hiện quyền xóa dữ liệu",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # 1. Verify parent password
    if not verify_password(req_in.password, parent.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Mật khẩu xác nhận không chính xác. Yêu cầu xóa dữ liệu bị từ chối."
        )

    # 2. Verify device existence and anti-IDOR ownership
    device = db.query(Device).filter(Device.id == device_id).first()
    if not device:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Không tìm thấy thiết bị"
        )
    if device.parent_id != parent.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Bạn không có quyền xóa dữ liệu của thiết bị này"
        )

    client_ip = request.client.host if request.client else None
    try:
        result = await erase_device_data(
            db=db,
            device_id=device.id,
            parent_id=parent.id,
            ip_address=client_ip
        )
        return result
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
