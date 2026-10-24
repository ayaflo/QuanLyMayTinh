"""Child access requests API routes for Open Guardian Kids (NT3).
Enables two-way communication where children can request more screen time or report false positives.
"""

from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, Request, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session

try:
    from ..database import get_db
    from ..models import Parent, Device, AccessRequest
    from ..schemas import AccessRequestCreate, AccessRequestReview, AccessRequestResponse
    from ..security import decode_access_token
    from ..services.request_service import create_child_request, get_requests, review_request
except (ImportError, ValueError):
    from server.database import get_db
    from server.models import Parent, Device, AccessRequest
    from server.schemas import AccessRequestCreate, AccessRequestReview, AccessRequestResponse
    from server.security import decode_access_token
    from server.services.request_service import create_child_request, get_requests, review_request

router = APIRouter(prefix="/api/v1/requests", tags=["AccessRequests"])
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


@router.post("", response_model=AccessRequestResponse, status_code=status.HTTP_201_CREATED, summary="Trẻ gửi yêu cầu xin thêm giờ hoặc báo chặn nhầm (NT3)")
def submit_child_request(
    request_in: AccessRequestCreate,
    db: Session = Depends(get_db)
) -> AccessRequestResponse:
    """Submit a child request for review by parents."""
    device = db.query(Device).filter(Device.id == request_in.device_id).first()
    if not device:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Không tìm thấy thiết bị")

    try:
        req = create_child_request(db, request_in)
        return AccessRequestResponse.model_validate(req)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get("", response_model=List[AccessRequestResponse], summary="Lấy danh sách yêu cầu của trẻ")
def list_child_requests(
    request: Request,
    device_id: Optional[int] = Query(None, description="Lọc theo ID thiết bị"),
    req_status: Optional[str] = Query(None, alias="status", description="Lọc theo trạng thái ('pending', 'approved', 'rejected')"),
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security_scheme),
    db: Session = Depends(get_db)
) -> List[AccessRequestResponse]:
    """Retrieve child requests with anti-IDOR isolation across parents."""
    parent = _get_parent_from_request(request, credentials, db)
    if parent:
        if device_id is not None:
            device = db.query(Device).filter(Device.id == device_id).first()
            if not device:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Không tìm thấy thiết bị")
            if device.parent_id != parent.id:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Bạn không có quyền xem yêu cầu của thiết bị này (Anti-IDOR)"
                )
            items = get_requests(db, device_id=device_id, status=req_status)
        else:
            parent_dev_ids = [d.id for d in db.query(Device.id).filter(Device.parent_id == parent.id).all()]
            items = [r for r in get_requests(db, status=req_status) if r.device_id in parent_dev_ids]
    else:
        items = get_requests(db, device_id=device_id, status=req_status)

    return [AccessRequestResponse.model_validate(item) for item in items]


@router.put("/{request_id}/review", response_model=AccessRequestResponse, summary="Phụ huynh duyệt hoặc từ chối yêu cầu của trẻ")
async def review_child_request(
    request_id: int,
    review_in: AccessRequestReview,
    request: Request,
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security_scheme),
    db: Session = Depends(get_db)
) -> AccessRequestResponse:
    """Resolve child request with anti-IDOR parent verification. Issues WebSocket command if approved."""
    req_obj = db.query(AccessRequest).filter(AccessRequest.id == request_id).first()
    if not req_obj:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Không tìm thấy yêu cầu")

    parent = _get_parent_from_request(request, credentials, db)
    if parent:
        device = db.query(Device).filter(Device.id == req_obj.device_id).first()
        if device and device.parent_id != parent.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Bạn không có quyền duyệt yêu cầu của thiết bị này (Anti-IDOR)"
            )

    client_ip = request.client.host if request.client else None
    try:
        req = await review_request(
            db=db,
            request_id=request_id,
            review_in=review_in,
            parent_id=parent.id if parent else None,
            ip_address=client_ip
        )
        return AccessRequestResponse.model_validate(req)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
