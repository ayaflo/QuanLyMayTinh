"""Usage report aggregation service for Open Guardian Kids (F3 & NT5).
Aggregates screen time, top applications, top web domains, and safety blocks.
"""

from typing import List, Dict, Any, Optional
from datetime import datetime, timezone, timedelta
from sqlalchemy.orm import Session
from sqlalchemy import func, desc

try:
    from ..models import ActivityEvent
    from ..schemas import ReportSummaryResponse, UsageSummaryItem
except (ImportError, ValueError):
    from server.models import ActivityEvent
    from server.schemas import ReportSummaryResponse, UsageSummaryItem


def utc_now():
    return datetime.now(timezone.utc)


def get_device_report_summary(
    db: Session,
    device_id: int,
    date_str: Optional[str] = None
) -> ReportSummaryResponse:
    """Aggregate daily usage summary for a specific device (F3 & NT5).
    Shared symmetrically between Parent Dashboard and Child View.
    """
    if not date_str:
        target_date = utc_now().date()
        date_str = target_date.isoformat()
    else:
        try:
            target_date = datetime.strptime(date_str, "%Y-%m-%d").date()
        except ValueError:
            target_date = utc_now().date()
            date_str = target_date.isoformat()

    start_dt = datetime.combine(target_date, datetime.min.time(), tzinfo=timezone.utc)
    end_dt = datetime.combine(target_date, datetime.max.time(), tzinfo=timezone.utc)

    base_query = db.query(ActivityEvent).filter(
        ActivityEvent.device_id == device_id,
        ActivityEvent.ts >= start_dt,
        ActivityEvent.ts <= end_dt
    )

    # 1. Total screen time seconds (from app_usage or screen_time events)
    total_screen_time = db.query(func.coalesce(func.sum(ActivityEvent.duration_sec), 0)).filter(
        ActivityEvent.device_id == device_id,
        ActivityEvent.ts >= start_dt,
        ActivityEvent.ts <= end_dt,
        ActivityEvent.type.in_(["app_usage", "screen_time"])
    ).scalar() or 0

    # 2. Top apps
    top_apps_raw = db.query(
        ActivityEvent.subject,
        func.sum(ActivityEvent.duration_sec).label("total_sec"),
        func.count(ActivityEvent.id).label("cnt")
    ).filter(
        ActivityEvent.device_id == device_id,
        ActivityEvent.ts >= start_dt,
        ActivityEvent.ts <= end_dt,
        ActivityEvent.type == "app_usage"
    ).group_by(ActivityEvent.subject).order_by(desc("total_sec")).limit(10).all()

    top_apps = [
        UsageSummaryItem(subject=item[0], total_duration_sec=item[1] or 0, count=item[2] or 0)
        for item in top_apps_raw
    ]

    # 3. Top domains (NT2: strictly FQDN/domain)
    top_domains_raw = db.query(
        ActivityEvent.subject,
        func.sum(ActivityEvent.duration_sec).label("total_sec"),
        func.count(ActivityEvent.id).label("cnt")
    ).filter(
        ActivityEvent.device_id == device_id,
        ActivityEvent.ts >= start_dt,
        ActivityEvent.ts <= end_dt,
        ActivityEvent.type == "web_access"
    ).group_by(ActivityEvent.subject).order_by(desc("cnt")).limit(10).all()

    top_domains = [
        UsageSummaryItem(subject=item[0], total_duration_sec=item[1] or 0, count=item[2] or 0)
        for item in top_domains_raw
    ]

    # 4. Blocked attempts count
    blocked_count = db.query(func.count(ActivityEvent.id)).filter(
        ActivityEvent.device_id == device_id,
        ActivityEvent.ts >= start_dt,
        ActivityEvent.ts <= end_dt,
        ActivityEvent.type.in_(["blocked_app", "blocked_domain"])
    ).scalar() or 0

    return ReportSummaryResponse(
        device_id=device_id,
        date=date_str,
        total_screen_time_sec=int(total_screen_time),
        top_apps=top_apps,
        top_domains=top_domains,
        blocked_attempts_count=int(blocked_count)
    )


def get_weekly_usage_stats(db: Session, device_id: int) -> List[Dict[str, Any]]:
    """Return past 7 days daily usage data for Chart.js rendering."""
    today = utc_now().date()
    stats = []
    for i in range(6, -1, -1):
        day = today - timedelta(days=i)
        start_dt = datetime.combine(day, datetime.min.time(), tzinfo=timezone.utc)
        end_dt = datetime.combine(day, datetime.max.time(), tzinfo=timezone.utc)

        duration = db.query(func.coalesce(func.sum(ActivityEvent.duration_sec), 0)).filter(
            ActivityEvent.device_id == device_id,
            ActivityEvent.ts >= start_dt,
            ActivityEvent.ts <= end_dt,
            ActivityEvent.type.in_(["app_usage", "screen_time"])
        ).scalar() or 0

        blocked = db.query(func.count(ActivityEvent.id)).filter(
            ActivityEvent.device_id == device_id,
            ActivityEvent.ts >= start_dt,
            ActivityEvent.ts <= end_dt,
            ActivityEvent.type.in_(["blocked_app", "blocked_domain"])
        ).scalar() or 0

        stats.append({
            "date": day.strftime("%d/%m"),
            "minutes": round(duration / 60, 1),
            "blocked_count": blocked
        })
    return stats
