"""Data retention & Right to Erasure services for Open Guardian Kids (OGK).
Compliant with Vietnam Decree 13/2023/ND-CP (Article 20 - Protection of Children's Personal Data)
and the 2016 Children Law:
- Auto-purge activity telemetry and heartbeat logs older than 90 days.
- Synchronous Right to Erasure ("Xóa toàn bộ dữ liệu của con tôi") on Server & Client Agent.
"""

import logging
from datetime import datetime, timedelta, timezone
from typing import Dict, Any, Optional
from sqlalchemy.orm import Session

try:
    from ..models import ActivityEvent, HeartbeatLog, AccessRequest, AuditLog, Device
    from .connection_manager import ws_manager
except (ImportError, ValueError):
    from server.models import ActivityEvent, HeartbeatLog, AccessRequest, AuditLog, Device
    from server.services.connection_manager import ws_manager

logger = logging.getLogger("OGK_RetentionService")


def purge_expired_activity_data(db: Session, days: int = 90) -> Dict[str, int]:
    """Auto-purge activity events and heartbeat logs older than specified retention days (default: 90).

    Mandated by Decree 13/2023/ND-CP Article 20 on data minimization and limited storage.
    """
    cutoff = datetime.now(timezone.utc) - timedelta(days=days)

    try:
        events_deleted = (
            db.query(ActivityEvent)
            .filter(ActivityEvent.ts < cutoff)
            .delete(synchronize_session=False)
        )

        heartbeats_deleted = (
            db.query(HeartbeatLog)
            .filter(HeartbeatLog.timestamp < cutoff)
            .delete(synchronize_session=False)
        )

        db.commit()

        if events_deleted > 0 or heartbeats_deleted > 0:
            logger.info(
                f"[Retention] Đã tự động dọn dẹp dữ liệu cũ hơn {days} ngày: "
                f"{events_deleted} sự kiện, {heartbeats_deleted} bản ghi nhịp tim."
            )

        return {
            "events_purged": events_deleted,
            "heartbeats_purged": heartbeats_deleted
        }
    except Exception as e:
        db.rollback()
        logger.error(f"[Retention] Lỗi dọn dẹp dữ liệu quá hạn 90 ngày: {e}")
        raise


async def erase_device_data(
    db: Session,
    device_id: int,
    parent_id: int,
    ip_address: Optional[str] = None
) -> Dict[str, Any]:
    """Execute 'Right to Erasure' (Quyền được xóa dữ liệu của trẻ) under Decree 13/2023/ND-CP.

    Permanently deletes all activity events, heartbeat telemetry, and access requests
    associated with the device, and triggers an immediate local buffer purge on the Agent.
    """
    device = db.query(Device).filter(Device.id == device_id, Device.parent_id == parent_id).first()
    if not device:
        raise ValueError("Thiết bị không tồn tại hoặc không thuộc quyền quản lý của bạn")

    try:
        ev_count = db.query(ActivityEvent).filter(ActivityEvent.device_id == device_id).delete(synchronize_session=False)
        hb_count = db.query(HeartbeatLog).filter(HeartbeatLog.device_id == device_id).delete(synchronize_session=False)
        req_count = db.query(AccessRequest).filter(AccessRequest.device_id == device_id).delete(synchronize_session=False)
        audit_count = db.query(AuditLog).filter(AuditLog.device_id == device_id).delete(synchronize_session=False)

        # Log compliance audit record for legal transparency
        compliance_log = AuditLog(
            parent_id=parent_id,
            device_id=device_id,
            action="retention:right_to_erasure",
            new_value=f"Đã xóa toàn bộ dữ liệu ({ev_count} sự kiện, {hb_count} nhịp tim) theo Nghị định 13/2023",
            ip_address=ip_address
        )
        db.add(compliance_log)
        db.commit()

        # Send real-time command via WebSocket to purge Agent local SQLite buffer
        await ws_manager.send_command(device_id, {
            "action": "purge_local_data",
            "timestamp": datetime.now(timezone.utc).isoformat()
        })

        logger.info(
            f"[Retention] Phụ huynh #{parent_id} đã thực hiện quyền xóa dữ liệu trên thiết bị #{device_id}: "
            f"{ev_count} sự kiện, {hb_count} nhịp tim, {req_count} yêu cầu."
        )

        return {
            "status": "success",
            "device_id": device_id,
            "events_deleted": ev_count,
            "heartbeats_deleted": hb_count,
            "requests_deleted": req_count,
            "message": "Đã xóa toàn bộ dữ liệu lịch sử hoạt động của thiết bị thành công."
        }
    except Exception as e:
        db.rollback()
        logger.error(f"[Retention] Lỗi thực hiện quyền xóa dữ liệu: {e}")
        raise
