"""Audit log routes for Open Guardian Kids.
Provides endpoints for parents and children to inspect policy change history (NT5).
"""

from typing import Optional
from fastapi import APIRouter, Depends, Query, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session

try:
    from ..database import get_db
    from ..models import AuditLog, Device, Parent
    from ..schemas import AuditLogResponse, AuditLogItem
    from ..security import decode_access_token
except (ImportError, ValueError):
    from server.database import get_db
    from server.models import AuditLog, Device, Parent
    from server.schemas import AuditLogResponse, AuditLogItem
    from server.security import decode_access_token

router = APIRouter()
security_scheme = HTTPBearer(auto_error=False)


def _get_identity(request: Request, credentials: Optional[HTTPAuthorizationCredentials]):
    """Extract authenticated identity (parent_id or device_id)."""
    token = request.cookies.get("access_token")
    if not token and credentials and credentials.credentials:
        token = credentials.credentials
    if not token:
        return None, None

    payload = decode_access_token(token)
    if not payload:
        return None, None

    parent_id = payload.get("parent_id")
    device_id = payload.get("device_id")
    if "sub" in payload:
        sub: str = payload["sub"]
        if sub.startswith("parent:"):
            try:
                parent_id = int(sub.split(":")[1])
            except (ValueError, IndexError):
                pass
        elif sub.startswith("device:"):
            try:
                device_id = int(sub.split(":")[1])
            except (ValueError, IndexError):
                pass

    return parent_id, device_id


@router.get("", response_model=AuditLogResponse, summary="Xem nhật ký kiểm toán thay đổi chính sách (NT5)")
def get_audit_logs(
    request: Request,
    device_id: Optional[int] = Query(None, description="Lọc theo ID thiết bị"),
    limit: int = Query(50, ge=1, le=200),
    offset: int = Query(0, ge=0),
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security_scheme),
    db: Session = Depends(get_db)
) -> AuditLogResponse:
    """Return audit log entries. Both parents and child agents can view history for transparency (NT5)."""
    parent_id, agent_dev_id = _get_identity(request, credentials)

    query = db.query(AuditLog)

    if agent_dev_id:
        # Child agent is viewing its own audit log (NT5)
        query = query.filter(AuditLog.device_id == agent_dev_id)
    elif device_id:
        query = query.filter(AuditLog.device_id == device_id)
    elif parent_id:
        # Parent viewing: filter to devices belonging to parent
        dev_ids = [d.id for d in db.query(Device.id).filter(Device.parent_id == parent_id).all()]
        query = query.filter(AuditLog.device_id.in_(dev_ids))

    total = query.count()
    items = query.order_by(AuditLog.id.desc()).offset(offset).limit(limit).all()

    return AuditLogResponse(
        total=total,
        items=[AuditLogItem.model_validate(it) for it in items]
    )
