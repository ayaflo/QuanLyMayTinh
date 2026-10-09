"""Security utilities for Open Guardian Kids (OGK).
Provides Argon2id password hashing, verification, and HMAC-SHA256 token generation.
"""

import os
import json
import hmac
import hashlib
import base64
from datetime import datetime, timedelta, timezone
from typing import Optional, Dict, Any
from passlib.context import CryptContext

SECRET_KEY = os.getenv("SECRET_KEY", "change-this-secret-key-in-production")
ACCESS_TOKEN_EXPIRE_MINUTES = 15

# Password hashing context configured with Argon2id
pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")


def hash_password(password: str) -> str:
    """Hash a plaintext password using Argon2id."""
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a plaintext password against an Argon2id hash."""
    return pwd_context.verify(plain_password, hashed_password)


def _b64_encode(data: bytes) -> str:
    """Encode bytes to URL-safe base64 string without trailing padding."""
    return base64.urlsafe_b64encode(data).decode("utf-8").rstrip("=")


def _b64_decode(data: str) -> bytes:
    """Decode URL-safe base64 string handling missing padding."""
    padding = 4 - (len(data) % 4)
    if padding != 4:
        data += "=" * padding
    return base64.urlsafe_b64decode(data.encode("utf-8"))


def create_access_token(data: Dict[str, Any], expires_delta: Optional[timedelta] = None) -> str:
    """Create a signed HMAC-SHA256 access token with an expiration timestamp.

    Token contains standard claims:
    - sub: subject identifier
    - iat: issued-at UTC timestamp
    - exp: expiration UTC timestamp (default: 15 minutes)
    """
    to_encode = data.copy()
    now = datetime.now(timezone.utc)
    if expires_delta:
        expire = now + expires_delta
    else:
        expire = now + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode.update({
        "iat": int(now.timestamp()),
        "exp": int(expire.timestamp())
    })

    header = {"alg": "HS256", "typ": "JWT"}
    header_b64 = _b64_encode(json.dumps(header, separators=(",", ":")).encode("utf-8"))
    payload_b64 = _b64_encode(json.dumps(to_encode, separators=(",", ":")).encode("utf-8"))

    signing_input = f"{header_b64}.{payload_b64}".encode("utf-8")
    signature = hmac.new(SECRET_KEY.encode("utf-8"), signing_input, hashlib.sha256).digest()
    signature_b64 = _b64_encode(signature)

    return f"{header_b64}.{payload_b64}.{signature_b64}"


def decode_access_token(token: str) -> Optional[Dict[str, Any]]:
    """Decode and verify a signed token.

    Returns the payload dictionary if the signature is valid and token is not expired,
    or None if verification fails.
    """
    try:
        parts = token.split(".")
        if len(parts) != 3:
            return None

        header_b64, payload_b64, signature_b64 = parts
        signing_input = f"{header_b64}.{payload_b64}".encode("utf-8")
        expected_sig = hmac.new(SECRET_KEY.encode("utf-8"), signing_input, hashlib.sha256).digest()
        provided_sig = _b64_decode(signature_b64)

        if not hmac.compare_digest(expected_sig, provided_sig):
            return None

        payload = json.loads(_b64_decode(payload_b64).decode("utf-8"))

        # Check expiration
        exp = payload.get("exp")
        if exp is not None:
            now_ts = int(datetime.now(timezone.utc).timestamp())
            if now_ts > exp:
                return None

        return payload
    except Exception:
        return None
