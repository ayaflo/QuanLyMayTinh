"""Emergency command routes for Open Guardian Kids.
Provides endpoints for parents to dispatch real-time commands (< 5s) via WebSocket.
"""

from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Request, Path, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session

try:
    from ..database import get_db
    from ..models import Parent, Device
    from ..schemas import CommandCreateRequest, CommandResponse
    from ..security import decode_access_token
    from ..services.command_service import dispatch_command
except (ImportError, ValueError):
    from server.database import get_db
    from server.models import Parent, Device
    from server.schemas import CommandCreateRequest, CommandResponse
    from server.security import decode_access_token
    from server.services.command_service import dispatch_command

router = APIRouter()
security_scheme = HTTPBearer(auto_error=False)


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


@router.post("/{device_id}/command", response_model=CommandResponse, summary="Gửi lệnh khẩn cấp tới thiết bị (< 5s)")
async def send_emergency_command(
    cmd_req: CommandCreateRequest,
    request: Request,
    device_id: int = Path(..., description="ID thiết bị mục tiêu"),
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security_scheme),
    db: Session = Depends(get_db)
) -> CommandResponse:
    """Dispatch emergency command ('lock_now', 'unlock', 'add_time') to child agent in real-time."""
    parent = _get_parent_from_request(request, credentials, db)
    if not parent:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Yêu cầu đăng nhập tài khoản phụ huynh để gửi lệnh khẩn cấp",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Anti-IDOR check: verify existence and ownership
    device = db.query(Device).filter(Device.id == device_id).first()
    if not device:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Không tìm thấy thiết bị"
        )
    if device.parent_id != parent.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Bạn không có quyền quản lý thiết bị này"
        )

    valid_commands = {"lock_now", "unlock", "add_time"}
    if cmd_req.command_type not in valid_commands:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Lệnh không hợp lệ. Chỉ chấp nhận: {', '.join(valid_commands)}"
        )

    client_ip = request.client.host if request.client else None
    cmd = await dispatch_command(
        db=db,
        device_id=device.id,
        parent_id=parent.id,
        command_type=cmd_req.command_type,
        minutes=cmd_req.minutes,
        ip_address=client_ip
    )

    return cmd
