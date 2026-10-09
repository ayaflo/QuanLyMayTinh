"""Enrollment service for pairing child devices with parent accounts.
Implements secure code generation and device claiming workflow.
"""

import secrets
import string
from datetime import datetime, timedelta, timezone
from typing import Optional, Tuple
from sqlalchemy.orm import Session

try:
    from ..models import Device, PairingCode
    from ..security import create_access_token
except (ImportError, ValueError):
    from server.models import Device, PairingCode
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


# Aliases for specification consistency
generate_pairing_code = create_pairing_code
verify_and_claim_code = claim_device_code

