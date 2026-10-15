"""Policy and time governance service for Open Guardian Kids.
Handles retrieval, default initialization, HMAC calculation, and audit logging (NT5).
"""

import json
from typing import Optional
from sqlalchemy.orm import Session

try:
    from ..models import Policy, AuditLog, DEFAULT_SCHEDULE_MATRIX
    from ..schemas import PolicyUpdate
    from ..security import calculate_policy_hmac
except (ImportError, ValueError):
    from server.models import Policy, AuditLog, DEFAULT_SCHEDULE_MATRIX
    from server.schemas import PolicyUpdate
    from server.security import calculate_policy_hmac


def get_or_create_default_policy(db: Session, device_id: int) -> Policy:
    """Retrieve current policy for a device or create default policy (v1) if none exists."""
    policy = db.query(Policy).filter(Policy.device_id == device_id).first()
    if policy:
        return policy

    # Initialize default policy (v1)
    version = 1
    weekday_quota = 90   # 90 minutes
    weekend_quota = 150  # 150 minutes
    matrix = DEFAULT_SCHEDULE_MATRIX

    hmac_sig = calculate_policy_hmac(
        device_id=device_id,
        version=version,
        weekday_quota_minutes=weekday_quota,
        weekend_quota_minutes=weekend_quota,
        schedule_matrix=matrix
    )

    policy = Policy(
        device_id=device_id,
        version=version,
        weekday_quota_minutes=weekday_quota,
        weekend_quota_minutes=weekend_quota,
        schedule_matrix=matrix,
        hmac_signature=hmac_sig
    )
    db.add(policy)
    db.commit()
    db.refresh(policy)
    return policy


def update_policy_and_log_audit(
    db: Session,
    device_id: int,
    parent_id: Optional[int],
    update_data: PolicyUpdate,
    ip_address: Optional[str] = None
) -> Policy:
    """Update device policy, increment version, recalculate HMAC, and record audit log (NT5)."""
    policy = get_or_create_default_policy(db, device_id)

    old_record = {
        "version": policy.version,
        "weekday_quota_minutes": policy.weekday_quota_minutes,
        "weekend_quota_minutes": policy.weekend_quota_minutes,
        "schedule_matrix": policy.schedule_matrix
    }

    # Apply changes
    if update_data.weekday_quota_minutes is not None:
        policy.weekday_quota_minutes = update_data.weekday_quota_minutes
    if update_data.weekend_quota_minutes is not None:
        policy.weekend_quota_minutes = update_data.weekend_quota_minutes
    if update_data.schedule_matrix is not None:
        policy.schedule_matrix = update_data.schedule_matrix

    policy.version += 1
    policy.hmac_signature = calculate_policy_hmac(
        device_id=device_id,
        version=policy.version,
        weekday_quota_minutes=policy.weekday_quota_minutes,
        weekend_quota_minutes=policy.weekend_quota_minutes,
        schedule_matrix=policy.schedule_matrix
    )

    new_record = {
        "version": policy.version,
        "weekday_quota_minutes": policy.weekday_quota_minutes,
        "weekend_quota_minutes": policy.weekend_quota_minutes,
        "schedule_matrix": policy.schedule_matrix
    }

    # Record Audit Log for transparency (NT5)
    audit = AuditLog(
        parent_id=parent_id,
        device_id=device_id,
        action="update_policy",
        old_value=json.dumps(old_record),
        new_value=json.dumps(new_record),
        ip_address=ip_address
    )
    db.add(audit)

    db.commit()
    db.refresh(policy)
    return policy
