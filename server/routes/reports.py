"""Usage reporting API routes for Open Guardian Kids (F3 & NT5).
Provides transparent usage analytics for both parents and children.
"""

from typing import Optional, List, Dict, Any
from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

try:
    from ..database import get_db
    from ..schemas import ReportSummaryResponse
    from ..services.report_service import get_device_report_summary, get_weekly_usage_stats
except (ImportError, ValueError):
    from server.database import get_db
    from server.schemas import ReportSummaryResponse
    from server.services.report_service import get_device_report_summary, get_weekly_usage_stats

router = APIRouter(prefix="/api/v1/reports", tags=["Reports"])


@router.get("/summary", response_model=ReportSummaryResponse, summary="Lấy báo cáo tổng hợp sử dụng trong ngày (F3 & NT5)")
def get_report_summary(
    device_id: int = Query(..., description="ID thiết bị cần xem báo cáo"),
    date: Optional[str] = Query(None, description="Ngày theo định dạng YYYY-MM-DD (mặc định hôm nay)"),
    db: Session = Depends(get_db)
) -> ReportSummaryResponse:
    """Retrieve daily usage summary including top apps, top domains, and blocked counts."""
    return get_device_report_summary(db, device_id=device_id, date_str=date)


@router.get("/weekly", summary="Lấy dữ liệu thống kê 7 ngày gần nhất phục vụ biểu đồ Chart.js")
def get_weekly_stats(
    device_id: int = Query(..., description="ID thiết bị"),
    db: Session = Depends(get_db)
) -> List[Dict[str, Any]]:
    """Retrieve past 7 days daily minutes and blocked counts."""
    return get_weekly_usage_stats(db, device_id=device_id)
