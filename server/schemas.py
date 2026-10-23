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


# ============================================================================
# Week 3 (Version 0.3): Domain & App Rules Schemas (T3_005)
# ============================================================================

class DomainRuleCreate(BaseModel):
    """Schema for creating a domain filtering rule."""
    category: str = Field(..., description="Giáo dục, Giải trí, Mạng xã hội, Game, Không phù hợp, DoH")
    domain: str = Field(..., min_length=3, max_length=255, description="FQDN domain or *.domain pattern")
    action: str = Field("block", description="'allow' or 'block'")
    is_permanent_whitelist: bool = Field(False, description="NT6 permanent whitelist flag")


class DomainRuleResponse(BaseModel):
    """Schema for returning domain rule details."""
    id: int
    category: str
    domain: str
    action: str
    is_permanent_whitelist: bool
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class DomainCategorySummary(BaseModel):
    """Summary of domain rules count by category."""
    category: str
    total_domains: int
    blocked_domains: int
    allowed_domains: int


class AppRuleCreate(BaseModel):
    """Schema for adding an app SHA-256 control rule."""
    device_id: Optional[int] = Field(None, description="Device ID or None for global rule")
    app_name: str = Field(..., min_length=1, max_length=100)
    sha256_hash: str = Field(..., min_length=64, max_length=64, description="64-hex char SHA-256 hash")
    action: str = Field("block", description="'allow' or 'block'")
    description: Optional[str] = None


class AppRuleResponse(BaseModel):
    """Schema for returning app rule details."""
    id: int
    device_id: Optional[int] = None
    app_name: str
    sha256_hash: str
    action: str
    description: Optional[str] = None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class FilteringRulesSyncResponse(BaseModel):
    """Consolidated rules payload downloaded by Client Agent for offline caching."""
    version: int = 1
    blocked_domains: list[str] = []
    allowed_domains: list[str] = []
    permanent_whitelist: list[str] = []
    app_blocklist: list[Dict[str, str]] = []  # [{"name": "...", "sha256": "..."}]


# ============================================================================
# Week 3 (Version 0.3): Event Ingestion Schemas (T3_006 - F3 & NT2)
# ============================================================================

class EventItemSchema(BaseModel):
    """Single telemetry event strictly conforming to F3 and NT2 minimal schema."""
    idempotency_key: str = Field(..., min_length=1, max_length=64, description="UUID v4 from agent buffer")
    ts: datetime = Field(..., description="Event timestamp in UTC")
    device_id: int = Field(..., description="Reporting device ID")
    child_id: Optional[int] = Field(None, description="Child profile ID if configured")
    type: str = Field(..., description="'app_usage', 'web_access', 'blocked_app', 'blocked_domain', 'screen_time'")
    subject: str = Field(..., min_length=1, max_length=255, description="FQDN domain or app executable ONLY")
    duration_sec: int = Field(0, ge=0, description="Duration in seconds if applicable")
    policy_id: Optional[int] = Field(None, description="Active policy version at event time")


class BatchEventIngestRequest(BaseModel):
    """Batch ingestion request payload sent from agent offline buffer."""
    events: list[EventItemSchema] = Field(..., max_length=500, description="Batch of up to 500 events")


class BatchEventIngestResponse(BaseModel):
    """Response after processing event batch."""
    received: int
    ingested: int
    duplicates: int
    status: str = "success"


# ============================================================================
# Week 3 (Version 0.3): Access Requests & Reports Schemas (T3_007 - NT3 & NT5)
# ============================================================================

class AccessRequestCreate(BaseModel):
    """Schema sent by child agent when child requests time or reports false positive (NT3)."""
    device_id: int
    child_id: Optional[int] = None
    request_type: str = Field(..., description="'add_time', 'unblock_domain', 'unblock_app'")
    target: Optional[str] = Field(None, max_length=255, description="Target domain, app name, or requested minutes")
    reason: Optional[str] = Field(None, max_length=500, description="Child's stated reason")


class AccessRequestReview(BaseModel):
    """Schema sent by parent to approve or reject an access request."""
    status: str = Field(..., description="'approved' or 'rejected'")
    parent_response: Optional[str] = Field(None, max_length=500, description="Message to the child")
    granted_minutes: Optional[int] = Field(15, ge=1, le=180, description="Minutes to add if request_type is 'add_time'")


class AccessRequestResponse(BaseModel):
    """Schema for returning access request details."""
    id: int
    device_id: int
    child_id: Optional[int] = None
    request_type: str
    target: Optional[str] = None
    reason: Optional[str] = None
    status: str
    parent_response: Optional[str] = None
    created_at: datetime
    resolved_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)


class UsageSummaryItem(BaseModel):
    """Item aggregation in usage reports."""
    subject: str
    total_duration_sec: int = 0
    count: int = 0


class ReportSummaryResponse(BaseModel):
    """Aggregated usage and safety report for Dashboard and Child View (NT5)."""
    device_id: int
    date: str
    total_screen_time_sec: int = 0
    top_apps: list[UsageSummaryItem] = []
    top_domains: list[UsageSummaryItem] = []
    blocked_attempts_count: int = 0

