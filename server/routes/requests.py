"""Child access requests API routes for Open Guardian Kids (NT3).
Enables two-way communication where children can request more screen time or report false positives.
"""

from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, Request, status
from sqlalchemy.orm import Session

try:
    from ..database import get_db
    from ..schemas import AccessRequestCreate, AccessRequestReview, AccessRequestResponse
    from ..services.request_service import create_child_request, get_requests, review_request
except (ImportError, ValueError):
    from server.database import get_db
    from server.schemas import AccessRequestCreate, AccessRequestReview, AccessRequestResponse
    from server.services.request_service import create_child_request, get_requests, review_request

router = APIRouter(prefix="/api/v1/requests", tags=["AccessRequests"])


@router.post("", response_model=AccessRequestResponse, status_code=status.HTTP_201_CREATED, summary="Trẻ gửi yêu cầu xin thêm giờ hoặc báo chặn nhầm (NT3)")
def submit_child_request(
    request_in: AccessRequestCreate,
    db: Session = Depends(get_db)
) -> AccessRequestResponse:
    """Submit a child request for review by parents."""
    try:
        req = create_child_request(db, request_in)
        return AccessRequestResponse.model_validate(req)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get("", response_model=List[AccessRequestResponse], summary="Lấy danh sách yêu cầu của trẻ")
def list_child_requests(
    device_id: Optional[int] = Query(None, description="Lọc theo ID thiết bị"),
    req_status: Optional[str] = Query(None, alias="status", description="Lọc theo trạng thái ('pending', 'approved', 'rejected')"),
    db: Session = Depends(get_db)
) -> List[AccessRequestResponse]:
    """Retrieve child requests."""
    items = get_requests(db, device_id=device_id, status=req_status)
    return [AccessRequestResponse.model_validate(item) for item in items]


@router.put("/{request_id}/review", response_model=AccessRequestResponse, summary="Phụ huynh duyệt hoặc từ chối yêu cầu của trẻ")
async def review_child_request(
    request_id: int,
    review_in: AccessRequestReview,
    request: Request,
    db: Session = Depends(get_db)
) -> AccessRequestResponse:
    """Resolve child request. If approved for 'add_time', immediately issues WebSocket command (< 5s)."""
    client_ip = request.client.host if request.client else None
    try:
        req = await review_request(
            db=db,
            request_id=request_id,
            review_in=review_in,
            parent_id=None,
            ip_address=client_ip
        )
        return AccessRequestResponse.model_validate(req)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
