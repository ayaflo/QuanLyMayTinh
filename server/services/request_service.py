"""Child access request management service for Open Guardian Kids (NT3).
Handles two-way communication: child requests extra time or reports false positives,
and parents approve/reject with instant WebSocket dispatch (< 5s).
"""

from typing import List, Optional
from datetime import datetime, timezone
from sqlalchemy.orm import Session

try:
    from ..models import AccessRequest, DomainRule, AppRule, Device
    from ..schemas import AccessRequestCreate, AccessRequestReview
    from .command_service import dispatch_command
except (ImportError, ValueError):
    from server.models import AccessRequest, DomainRule, AppRule, Device
    from server.schemas import AccessRequestCreate, AccessRequestReview
    from server.services.command_service import dispatch_command


def utc_now():
    return datetime.now(timezone.utc)


def create_child_request(db: Session, req_in: AccessRequestCreate) -> AccessRequest:
    """Submit a new request from the child agent (NT3)."""
    device = db.query(Device).filter(Device.id == req_in.device_id).first()
    if not device:
        raise ValueError(f"Thiết bị #{req_in.device_id} không tồn tại.")

    new_req = AccessRequest(
        device_id=req_in.device_id,
        child_id=req_in.child_id,
        request_type=req_in.request_type,
        target=req_in.target,
        reason=req_in.reason,
        status="pending",
        created_at=utc_now()
    )
    db.add(new_req)
    db.commit()
    db.refresh(new_req)
    return new_req


def get_requests(
    db: Session,
    device_id: Optional[int] = None,
    status: Optional[str] = None
) -> List[AccessRequest]:
    """Retrieve access requests, optionally filtered by device or status."""
    query = db.query(AccessRequest)
    if device_id is not None:
        query = query.filter(AccessRequest.device_id == device_id)
    if status is not None:
        query = query.filter(AccessRequest.status == status)
    return query.order_by(AccessRequest.created_at.desc()).all()


async def review_request(
    db: Session,
    request_id: int,
    review_in: AccessRequestReview,
    parent_id: Optional[int] = None,
    ip_address: Optional[str] = None
) -> AccessRequest:
    """Review and resolve a child request.
    If approved for 'add_time', dispatches WebSocket add_time command to agent (< 5s).
    If approved for unblocking domain/app, modifies the corresponding rule.
    """
    req = db.query(AccessRequest).filter(AccessRequest.id == request_id).first()
    if not req:
        raise ValueError(f"Yêu cầu #{request_id} không tồn tại.")

    req.status = review_in.status
    req.parent_response = review_in.parent_response
    req.resolved_at = utc_now()
    db.commit()
    db.refresh(req)

    # If approved, perform required action
    if review_in.status == "approved":
        if req.request_type == "add_time":
            minutes = review_in.granted_minutes or 15
            await dispatch_command(
                db=db,
                device_id=req.device_id,
                parent_id=parent_id,
                command_type="add_time",
                minutes=minutes,
                ip_address=ip_address,
                extra_payload={
                    "request_id": req.id,
                    "request_type": "add_time",
                    "status": "approved",
                    "minutes": minutes,
                    "parent_response": review_in.parent_response or ""
                }
            )
        elif req.request_type == "unblock_domain" and req.target:
            target_domain = req.target.strip().lower()
            rule = db.query(DomainRule).filter(DomainRule.domain == target_domain).first()
            if rule:
                rule.action = "allow"
                db.commit()
            await dispatch_command(
                db=db,
                device_id=req.device_id,
                parent_id=parent_id,
                command_type="request_reviewed",
                ip_address=ip_address,
                extra_payload={
                    "request_id": req.id,
                    "request_type": "unblock_domain",
                    "status": "approved",
                    "target": req.target,
                    "parent_response": review_in.parent_response or ""
                }
            )
        elif req.request_type == "unblock_app" and req.target:
            rule = db.query(AppRule).filter(
                (AppRule.app_name == req.target) | (AppRule.sha256_hash == req.target.lower())
            ).first()
            if rule:
                rule.action = "allow"
                db.commit()
            await dispatch_command(
                db=db,
                device_id=req.device_id,
                parent_id=parent_id,
                command_type="request_reviewed",
                ip_address=ip_address,
                extra_payload={
                    "request_id": req.id,
                    "request_type": "unblock_app",
                    "status": "approved",
                    "target": req.target,
                    "parent_response": review_in.parent_response or ""
                }
            )
    elif review_in.status == "rejected":
        # Dispatch rejection notification to child agent
        await dispatch_command(
            db=db,
            device_id=req.device_id,
            parent_id=parent_id,
            command_type="request_reviewed",
            ip_address=ip_address,
            extra_payload={
                "request_id": req.id,
                "request_type": req.request_type,
                "status": "rejected",
                "target": req.target,
                "parent_response": review_in.parent_response or ""
            }
        )

    return req
