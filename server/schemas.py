"""Pydantic schemas for data validation and API request/response serialization.
Includes authentication, device enrollment, and heartbeat schemas.
"""

from datetime import datetime, timezone
from typing import Optional, Dict, Any
from pydantic import BaseModel, Field, ConfigDict


def utc_now():
    """Return timezone-aware current UTC time."""
    return datetime.now(timezone.utc)


# ============================================================================
# Phase 2 / T010: Authentication Schemas
# ============================================================================

class LoginRequest(BaseModel):
    """Schema for parent login requests."""
    username: str = Field(..., min_length=3, max_length=50, description="Parent account username")
    password: str = Field(..., min_length=6, description="Parent account password")


class TokenResponse(BaseModel):
    """Schema for JWT / session token response upon successful login."""
    access_token: str
    token_type: str = "bearer"
    expires_in: int = 900  # 15 minutes default


# ============================================================================
# Phase 2 / T011: Enrollment Schemas
# ============================================================================

class CreateCodeResponse(BaseModel):
    """Schema for newly generated 8-character pairing code."""
    code: str = Field(..., min_length=8, max_length=8, description="8-character pairing code")
    expires_at: datetime = Field(..., description="Expiration timestamp (typically 10 minutes)")


class ClaimDeviceRequest(BaseModel):
    """Schema sent by Agent to claim a pairing code and link device to parent."""
    code: str = Field(..., min_length=8, max_length=8, description="8-character pairing code")
    device_fingerprint: str = Field(..., description="Unique hardware UUID / fingerprint")
    device_name: Optional[str] = Field("Windows PC", description="Friendly device name")


class ClaimDeviceResponse(BaseModel):
    """Schema returned to Agent upon successful pairing."""
    device_id: int
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


# ============================================================================
# Phase 2 / T012: Heartbeat Schemas
# ============================================================================

class HeartbeatRequest(BaseModel):
    """Schema for periodic heartbeat ping sent from Agent (every 60s)."""
    device_fingerprint: Optional[str] = Field(None, description="Optional fingerprint check")
    status_payload: Optional[Dict[str, Any]] = Field(default=None, description="Telemetry data (CPU, RAM, active app, etc.)")


class HeartbeatResponse(BaseModel):
    """Schema returned to Agent with current policy version and server timestamp."""
    status: str = "ok"
    policy_version: int = Field(default=1, description="Latest policy version for synchronization")
    server_time: datetime = Field(default_factory=utc_now, description="Server UTC time for monotonic drift check")

    model_config = ConfigDict(from_attributes=True)
