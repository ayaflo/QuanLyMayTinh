"""Device enrollment routes for Open Guardian Kids.
Implements:
- POST /api/v1/enroll/create-code (Parent generates pairing code)
- POST /api/v1/enroll/claim (Child agent claims code and pairs)
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

try:
    from ..database import get_db
    from ..models import Parent
    from ..schemas import CreateCodeResponse, ClaimDeviceRequest, ClaimDeviceResponse
    from ..services.enrollment_service import create_pairing_code, claim_device_code
    from .auth import get_current_parent
except (ImportError, ValueError):
    from server.database import get_db
    from server.models import Parent
    from server.schemas import CreateCodeResponse, ClaimDeviceRequest, ClaimDeviceResponse
    from server.services.enrollment_service import create_pairing_code, claim_device_code
    from server.routes.auth import get_current_parent

router = APIRouter()


@router.post(
    "/create-code",
    response_model=CreateCodeResponse,
    summary="Tạo mã ghép đôi 8 ký tự cho phụ huynh"
)
def create_code(
    current_parent: Parent = Depends(get_current_parent),
    db: Session = Depends(get_db)
) -> CreateCodeResponse:
    """Generate a temporary 8-character pairing code valid for 10 minutes for the authenticated parent."""
    pairing_code = create_pairing_code(db=db, parent_id=current_parent.id, expires_minutes=10)
    return CreateCodeResponse(
        code=pairing_code.code,
        expires_at=pairing_code.expires_at
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
