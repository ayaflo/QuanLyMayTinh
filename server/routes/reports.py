"""Usage reporting API routes for Open Guardian Kids (F3 & NT5).
Provides transparent usage analytics for both parents and children.
"""

from typing import Optional, List, Dict, Any
from fastapi import APIRouter, Depends, HTTPException, Query, Request, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session

try:
    from ..database import get_db
    from ..models import Parent, Device
    from ..schemas import ReportSummaryResponse
    from ..security import decode_access_token
    from ..services.report_service import get_device_report_summary, get_weekly_usage_stats
except (ImportError, ValueError):
    from server.database import get_db
    from server.models import Parent, Device
    from server.schemas import ReportSummaryResponse
    from server.security import decode_access_token
    from server.services.report_service import get_device_report_summary, get_weekly_usage_stats

router = APIRouter(prefix="/api/v1/reports", tags=["Reports"])
security_scheme = HTTPBearer(auto_error=False)


def _verify_report_access(
    device_id: int,
    request: Request,
    credentials: Optional[HTTPAuthorizationCredentials],
    db: Session
) -> None:
    """Anti-IDOR helper: verifies caller has legitimate ownership or belongs to the target device."""
    token = request.cookies.get("access_token")
    if not token and credentials and credentials.credentials:
        token = credentials.credentials

    if not token:
        return

    payload = decode_access_token(token)
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token không hợp lệ hoặc đã hết hạn",
            headers={"WWW-Authenticate": "Bearer"},
        )

    device = db.query(Device).filter(Device.id == device_id).first()
    if not device:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Không tìm thấy thiết bị")

    # If caller is an enrolled child device
    token_device_id = payload.get("device_id")
    if not token_device_id and "sub" in payload and payload["sub"].startswith("device:"):
        try:
            token_device_id = int(payload["sub"].split(":")[1])
        except (ValueError, IndexError):
            pass

    if token_device_id:
        if token_device_id != device.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Thiết bị không có quyền xem báo cáo của thiết bị khác (Anti-IDOR)"
            )
        return

    # If caller is parent
    parent_id = payload.get("parent_id")
    if not parent_id and "sub" in payload and payload["sub"].startswith("parent:"):
        try:
            parent_id = int(payload["sub"].split(":")[1])
        except (ValueError, IndexError):
            pass

    if parent_id:
        if device.parent_id != parent_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Bạn không có quyền xem báo cáo của thiết bị này (Anti-IDOR)"
            )


@router.get("/summary", response_model=ReportSummaryResponse, summary="Lấy báo cáo tổng hợp sử dụng trong ngày (F3 & NT5)")
def get_report_summary(
    request: Request,
    device_id: int = Query(..., description="ID thiết bị cần xem báo cáo"),
    date: Optional[str] = Query(None, description="Ngày theo định dạng YYYY-MM-DD (mặc định hôm nay)"),
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security_scheme),
    db: Session = Depends(get_db)
) -> ReportSummaryResponse:
    """Retrieve daily usage summary including top apps, top domains, and blocked counts."""
    _verify_report_access(device_id, request, credentials, db)
    return get_device_report_summary(db, device_id=device_id, date_str=date)


@router.get("/weekly", summary="Lấy dữ liệu thống kê 7 ngày gần nhất phục vụ biểu đồ Chart.js")
def get_weekly_stats(
    request: Request,
    device_id: int = Query(..., description="ID thiết bị"),
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security_scheme),
    db: Session = Depends(get_db)
) -> List[Dict[str, Any]]:
    """Retrieve past 7 days daily minutes and blocked counts."""
    _verify_report_access(device_id, request, credentials, db)
    return get_weekly_usage_stats(db, device_id=device_id)
