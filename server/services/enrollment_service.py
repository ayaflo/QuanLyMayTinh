"""Enrollment service for pairing child devices with parent accounts.
Implements secure code generation and device claiming workflow.
"""

import secrets
import string
from datetime import datetime, timedelta, timezone
from typing import Optional, Tuple
from sqlalchemy.orm import Session

try:
    from ..models import Device, PairingCode, AuditLog
    from ..security import create_access_token
except (ImportError, ValueError):
    from server.models import Device, PairingCode, AuditLog
    from server.security import create_access_token

# Unambiguous characters avoiding 0/O, 1/I/L to make manual typing painless
SAFE_CHARS = "23456789ABCDEFGHJKMNPQRSTUVWXYZ"
CODE_VALIDITY_MINUTES = 10


def generate_code(length: int = 8) -> str:
    """Generate a cryptographically secure random code avoiding ambiguous characters.

    Omits characters such as '0', 'O', '1', 'I', 'L'.
    """
    return "".join(secrets.choice(SAFE_CHARS) for _ in range(length))


def create_pairing_code(db: Session, parent_id: int, expires_minutes: int = CODE_VALIDITY_MINUTES) -> PairingCode:
    """Create a temporary pairing code valid for expires_minutes for a parent."""
    code = generate_code(8)
    expires_at = datetime.now(timezone.utc) + timedelta(minutes=expires_minutes)

    pairing_code = PairingCode(
        parent_id=parent_id,
        code=code,
        expires_at=expires_at,
        is_used=False
    )
    db.add(pairing_code)
    db.commit()
    db.refresh(pairing_code)
    return pairing_code


def claim_device_code(
    db: Session,
    code: str,
    device_fingerprint: str,
    device_name: Optional[str] = "Windows PC"
) -> Tuple[Device, str, str]:
    """Validate a pairing code and link the child device to the parent account.

    Checks:
    - Code exists and is not used.
    - Code is within validity duration (<= 10 minutes).

    Updates/creates device record, marks code as used, and issues access/refresh tokens.
    Returns:
        (device, access_token, refresh_token)
    """
    cleaned_code = code.strip().upper()
    now = datetime.now(timezone.utc)

    pairing = (
        db.query(PairingCode)
        .filter(PairingCode.code == cleaned_code, PairingCode.is_used == False)
        .first()
    )

    if not pairing:
        raise ValueError("Mã ghép đôi không tồn tại hoặc đã được sử dụng")

    expires_at = pairing.expires_at
    if expires_at.tzinfo is None:
        expires_at = expires_at.replace(tzinfo=timezone.utc)

    if expires_at < now:
        raise ValueError("Mã ghép đôi đã hết hạn")

    # Link or register device
    device = (
        db.query(Device)
        .filter(Device.device_fingerprint == device_fingerprint)
        .first()
    )

    if device:
        device.parent_id = pairing.parent_id
        if device_name:
            device.device_name = device_name
        device.status = "online"
        device.last_seen = now
    else:
        device = Device(
            parent_id=pairing.parent_id,
            device_fingerprint=device_fingerprint,
            device_name=device_name or "Windows PC",
            status="online",
            last_seen=now
        )
        db.add(device)

    # Invalidate code
    pairing.is_used = True
    db.flush()

    # Record pairing in AuditLog (NT5)
    audit = AuditLog(
        parent_id=pairing.parent_id,
        device_id=device.id,
        action="enroll_device",
        new_value=f"Ghép đôi thiết bị '{device.device_name}' thành công",
        ip_address="127.0.0.1",
        created_at=now
    )
    db.add(audit)

    db.commit()
    db.refresh(device)

    # Issue tokens for device
    access_token = create_access_token(
        {"sub": f"device:{device.id}", "device_id": device.id, "type": "access"},
        expires_delta=timedelta(minutes=15)
    )
    refresh_token = create_access_token(
        {"sub": f"device:{device.id}", "device_id": device.id, "type": "refresh"},
        expires_delta=timedelta(days=30)
    )

    return device, access_token, refresh_token


def unenroll_device(
    db: Session,
    device_id: int,
    device_fingerprint: Optional[str] = None
) -> bool:
    """Permanently delete a device from parent account and wipe all associated records.

    Ensures the device completely disappears from the parent's dashboard upon uninstall.
    """
    query = db.query(Device).filter(Device.id == device_id)
    if device_fingerprint:
        query = query.filter(Device.device_fingerprint == device_fingerprint)
    device = query.first()

    if not device and device_fingerprint:
        # Fallback search by unique fingerprint only
        device = db.query(Device).filter(Device.device_fingerprint == device_fingerprint).first()

    if not device:
        return False

    dev_id = device.id

    # Cascade delete records for consistency across all database engines
    try:
        from server.models import (
            AuditLog, HeartbeatLog, ActivityEvent,
            AccessRequest, DeviceCommand, Policy, AppRule
        )
        db.query(AuditLog).filter(AuditLog.device_id == dev_id).delete(synchronize_session=False)
        db.query(HeartbeatLog).filter(HeartbeatLog.device_id == dev_id).delete(synchronize_session=False)
        db.query(ActivityEvent).filter(ActivityEvent.device_id == dev_id).delete(synchronize_session=False)
        db.query(AccessRequest).filter(AccessRequest.device_id == dev_id).delete(synchronize_session=False)
        db.query(DeviceCommand).filter(DeviceCommand.device_id == dev_id).delete(synchronize_session=False)
        db.query(Policy).filter(Policy.device_id == dev_id).delete(synchronize_session=False)
        db.query(AppRule).filter(AppRule.device_id == dev_id).delete(synchronize_session=False)
    except Exception:
        pass

    db.delete(device)
    db.commit()

    # Disconnect any active real-time WebSocket connection
    try:
        from server.services.connection_manager import ws_manager
        ws_manager.disconnect(dev_id)
    except Exception:
        pass

    return True


# Aliases for specification consistency
generate_pairing_code = create_pairing_code
verify_and_claim_code = claim_device_code
delete_enrolled_device = unenroll_device

