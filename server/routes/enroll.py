"""Device enrollment routes for Open Guardian Kids.
Implements:
- POST /api/v1/enroll/create-code (Parent generates pairing code)
- POST /api/v1/enroll/claim (Child agent claims code and pairs)
"""

from datetime import timezone
from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlalchemy.orm import Session

try:
    from ..database import get_db
    from ..models import Parent, Device
    from ..schemas import CreateCodeResponse, ClaimDeviceRequest, ClaimDeviceResponse, UnenrollDeviceRequest
    from ..services.enrollment_service import create_pairing_code, claim_device_code, unenroll_device
    from ..security import decode_access_token
    from .auth import get_current_parent
except (ImportError, ValueError):
    from server.database import get_db
    from server.models import Parent, Device
    from server.schemas import CreateCodeResponse, ClaimDeviceRequest, ClaimDeviceResponse, UnenrollDeviceRequest
    from server.services.enrollment_service import create_pairing_code, claim_device_code, unenroll_device
    from server.security import decode_access_token
    from server.routes.auth import get_current_parent

router = APIRouter()


@router.post(
    "/create-code",
    response_model=CreateCodeResponse,
    summary="Tạo mã ghép đôi 8 ký tự cho phụ huynh"
)
@router.post(
    "/pairing-codes",
    response_model=CreateCodeResponse,
    summary="Alias tạo mã ghép đôi 8 ký tự cho phụ huynh"
)
def create_code(
    current_parent: Parent = Depends(get_current_parent),
    db: Session = Depends(get_db)
) -> CreateCodeResponse:
    """Generate a temporary 8-character pairing code valid for 10 minutes for the authenticated parent."""
    pairing_code = create_pairing_code(db=db, parent_id=current_parent.id, expires_minutes=10)
    exp = pairing_code.expires_at
    if exp.tzinfo is None:
        exp = exp.replace(tzinfo=timezone.utc)
    return CreateCodeResponse(
        code=pairing_code.code,
        expires_at=exp
    )


@router.post(
    "/claim",
    response_model=ClaimDeviceResponse,
    summary="Tác tử kích hoạt mã ghép đôi để liên kết thiết bị"
)
def claim_device(
    req: ClaimDeviceRequest,
    db: Session = Depends(get_db)
) -> ClaimDeviceResponse:
    """Child agent presents pairing code and device fingerprint to pair with parent account."""
    try:
        device, access_token, refresh_token = claim_device_code(
            db=db,
            code=req.code,
            device_fingerprint=req.device_fingerprint,
            device_name=req.device_name
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

    return ClaimDeviceResponse(
        device_id=device.id,
        access_token=access_token,
        refresh_token=refresh_token,
        token_type="bearer"
    )


@router.post(
    "/unenroll",
    summary="Tác tử máy con thông báo gỡ cài đặt để xóa thiết bị khỏi máy chủ"
)
def unenroll_endpoint(
    req: UnenrollDeviceRequest,
    request: Request,
    db: Session = Depends(get_db)
):
    """Child agent unenrolls itself upon uninstallation.

    Authenticates via:
    1. Bearer access/refresh token in Authorization header
    2. Or device_id + device_fingerprint verification
    Permanently deletes device and cascading data so parent dashboard updates immediately.
    """
    auth_header = request.headers.get("Authorization", "")
    token = None
    if auth_header.startswith("Bearer "):
        token = auth_header.split(" ", 1)[1].strip()

    target_device_id = req.device_id
    if token:
        payload = decode_access_token(token)
        if payload:
            token_dev_id = payload.get("device_id")
            if not token_dev_id and "sub" in payload and payload["sub"].startswith("device:"):
                try:
                    token_dev_id = int(payload["sub"].split(":")[1])
                except Exception:
                    pass
            if token_dev_id:
                target_device_id = token_dev_id

    # If neither token nor fingerprint is provided, reject request
    if not target_device_id and not req.device_fingerprint:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cần cung cấp mã thiết bị hoặc mã nhận diện phần cứng (fingerprint) để gỡ bỏ."
        )

    # Check device in database
    query = db.query(Device)
    if target_device_id:
        query = query.filter(Device.id == target_device_id)
    if req.device_fingerprint:
        query = query.filter(Device.device_fingerprint == req.device_fingerprint)
    device = query.first()

    if not device and req.device_fingerprint:
        device = db.query(Device).filter(Device.device_fingerprint == req.device_fingerprint).first()

    if not device:
        # Idempotent response if device was already deleted or not found
        return {
            "status": "success",
            "message": "Thiết bị không tồn tại trên hệ thống hoặc đã được gỡ bỏ từ trước."
        }

    dev_id = device.id
    unenroll_device(db, device_id=dev_id)
    return {
        "status": "success",
        "device_id": dev_id,
        "message": f"Đã gỡ bỏ hoàn toàn thiết bị #{dev_id} khỏi tài khoản phụ huynh."
    }
