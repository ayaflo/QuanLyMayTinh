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


# ============================================================================
# Week 2 (Version 0.2): Policy, Audit Logs & Emergency Commands Schemas
# ============================================================================

class PolicyUpdate(BaseModel):
    """Schema for updating device screen time policy from Parent Dashboard."""
    weekday_quota_minutes: Optional[int] = Field(None, ge=1, le=1440, description="Daily limit in minutes for Mon-Fri")
    weekend_quota_minutes: Optional[int] = Field(None, ge=1, le=1440, description="Daily limit in minutes for Sat-Sun")
    schedule_matrix: Optional[str] = Field(None, min_length=336, max_length=336, description="336-character 0/1 weekly schedule matrix")


class PolicyResponse(BaseModel):
    """Schema for policy payload sent to Agent and Dashboard."""
    device_id: int
    version: int
    weekday_quota_minutes: int
    weekend_quota_minutes: int
    schedule_matrix: str
    hmac_signature: str
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class AuditLogItem(BaseModel):
    """Schema for single audit log entry (NT5)."""
    id: int
    parent_id: Optional[int] = None
    device_id: int
    action: str
    old_value: Optional[str] = None
    new_value: Optional[str] = None
    ip_address: Optional[str] = None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class AuditLogResponse(BaseModel):
    """Schema for list of audit log items."""
    total: int
    items: list[AuditLogItem]


class CommandCreateRequest(BaseModel):
    """Schema for creating an emergency command from Dashboard."""
    command_type: str = Field(..., description="Action: 'lock_now', 'unlock', 'add_time'")
    minutes: Optional[int] = Field(15, ge=1, le=180, description="Additional minutes if command_type is 'add_time'")


class CommandResponse(BaseModel):
    """Schema for command dispatch status."""
    id: int
    device_id: int
    command_type: str
    status: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class WSCommandMessage(BaseModel):
    """Schema for JSON message dispatched over WebSocket to child agent."""
    action: str = Field(..., description="Command action: 'lock_now', 'unlock', 'add_time', 'policy_updated'")
    payload: Optional[Dict[str, Any]] = None
    timestamp: datetime = Field(default_factory=utc_now)
