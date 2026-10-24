"""Cryptographic utilities for Open Guardian Kids (OGK).
Provides authenticated symmetric encryption (AES-256-GCM) with 12-byte Nonce and 16-byte Tag
for data-at-rest protection and credential security (F5 & OWASP ASVS v4).
"""

import os
import base64
import hashlib
from typing import Optional, Union
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.exceptions import InvalidTag

# Master key derivation: derive a 32-byte (256-bit) AES key from environment or SECRET_KEY
DEFAULT_SECRET = os.getenv("ENCRYPTION_KEY") or os.getenv("SECRET_KEY", "change-this-secret-key-in-production")
MASTER_AES_KEY = hashlib.sha256(DEFAULT_SECRET.encode("utf-8")).digest()


def _get_key(key: Optional[bytes] = None) -> bytes:
    """Ensure key is exactly 32 bytes for AES-256."""
    if key is None:
        return MASTER_AES_KEY
    if len(key) != 32:
        return hashlib.sha256(key).digest()
    return key


def generate_encryption_key() -> str:
    """Generate a random 32-byte AES key encoded as URL-safe base64."""
    raw_key = AESGCM.generate_key(bit_length=256)
    return base64.urlsafe_b64encode(raw_key).decode("utf-8")


def encrypt_data(
    plaintext: Union[str, bytes],
    key: Optional[bytes] = None,
    associated_data: Optional[bytes] = None
) -> str:
    """Encrypt plaintext using AES-256-GCM.

    Format: URL-safe Base64 of [12-byte Nonce + Ciphertext + 16-byte Auth Tag].
    """
    aes_key = _get_key(key)
    aesgcm = AESGCM(aes_key)

    # 12-byte random nonce (standard for GCM)
    nonce = os.urandom(12)

    data_bytes = plaintext.encode("utf-8") if isinstance(plaintext, str) else plaintext

    # AESGCM.encrypt returns ciphertext concatenated with the 16-byte authentication tag
    ciphertext_and_tag = aesgcm.encrypt(nonce, data_bytes, associated_data)

    payload = nonce + ciphertext_and_tag
    return base64.urlsafe_b64encode(payload).decode("utf-8")


def decrypt_data(
    ciphertext_b64: str,
    key: Optional[bytes] = None,
    associated_data: Optional[bytes] = None
) -> str:
    """Decrypt ciphertext produced by encrypt_data using AES-256-GCM.

    Verifies integrity tag before decryption. Raises ValueError if data is invalid or tampered with.
    """
    if not ciphertext_b64:
        raise ValueError("Ciphertext cannot be empty")

    aes_key = _get_key(key)
    aesgcm = AESGCM(aes_key)

    try:
        raw_payload = base64.urlsafe_b64decode(ciphertext_b64.encode("utf-8"))
    except Exception as e:
        raise ValueError(f"Base64 decoding failed: {e}")

    # Must contain at least 12-byte nonce + 16-byte authentication tag
    if len(raw_payload) < 28:
        raise ValueError("Ciphertext payload is too short for AES-256-GCM (minimum 28 bytes required)")

    nonce = raw_payload[:12]
    ciphertext_and_tag = raw_payload[12:]

    try:
        decrypted_bytes = aesgcm.decrypt(nonce, ciphertext_and_tag, associated_data)
        return decrypted_bytes.decode("utf-8")
    except InvalidTag:
        raise ValueError("Decryption failed: data was tampered or invalid auth key (InvalidTag)")
    except UnicodeDecodeError:
        # If payload was originally raw bytes that cannot be decoded to utf-8 string
        return decrypted_bytes.hex()
