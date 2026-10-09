"""Tests for heartbeat telemetry and online status tracking (T045).
Verifies heartbeat endpoint, telemetry log storage, and online/offline status detection.
"""

from datetime import datetime, timedelta, timezone
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from server.database import Base, get_db
from server.models import Parent, Device, HeartbeatLog
from server.security import hash_password, create_access_token
from server.main import app

# Isolated in-memory test database
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(autouse=True)
def setup_test_db():
    """Create fresh database with test parent and enrolled device."""
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        parent = Parent(
            id=1,
            username="hb_parent",
            password_hash=hash_password("HbPass#123")
        )
        db.add(parent)
        db.flush()

        device = Device(
            id=1,
            parent_id=parent.id,
            device_name="Test Kid PC",
            device_fingerprint="FINGERPRINT-HB-001",
            status="offline",
            last_seen=None
        )
        db.add(device)
        db.commit()
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)


@pytest.fixture
def client(setup_test_db):
    """FastAPI test client with overridden database dependency."""
    def override_get_db():
        db = TestingSessionLocal()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()


@pytest.fixture
def device_token():
    """Device JWT bearer token."""
    return create_access_token({
        "sub": "device:1",
        "device_id": 1,
        "type": "access"
    })


def test_heartbeat_with_bearer_token(client, device_token):
    """Enrolled device sends heartbeat ping with Bearer token."""
    headers = {"Authorization": f"Bearer {device_token}"}
    payload = {
        "device_fingerprint": "FINGERPRINT-HB-001",
        "status_payload": {
            "agent_status": "running",
            "protocol_version": 1
        }
    }

    response = client.post("/api/v1/heartbeat", json=payload, headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert data["policy_version"] == 1
    assert "server_time" in data

    # Verify device status and log stored in DB
    db = TestingSessionLocal()
    device = db.query(Device).filter(Device.id == 1).first()
    assert device.status == "online"
    assert device.last_seen is not None

    log = db.query(HeartbeatLog).filter(HeartbeatLog.device_id == 1).first()
    assert log is not None
    assert "running" in log.status_payload
    db.close()


def test_heartbeat_with_fingerprint_fallback(client):
    """Device sends heartbeat using hardware fingerprint without token."""
    payload = {
        "device_fingerprint": "FINGERPRINT-HB-001",
        "status_payload": {"agent_status": "running"}
    }
    response = client.post("/api/v1/heartbeat", json=payload)
    assert response.status_code == 200
    assert response.json()["status"] == "ok"

    db = TestingSessionLocal()
    device = db.query(Device).filter(Device.device_fingerprint == "FINGERPRINT-HB-001").first()
    assert device.status == "online"
    db.close()


def test_heartbeat_unknown_device_rejected(client):
    """Heartbeat from unregistered device fingerprint returns 401 Unauthorized."""
    payload = {
        "device_fingerprint": "UNKNOWN-FINGERPRINT",
        "status_payload": {}
    }
    response = client.post("/api/v1/heartbeat", json=payload)
    assert response.status_code == 401
    assert "Thiết bị chưa được đăng ký" in response.json()["detail"]


def test_online_status_threshold_calculation():
    """Verify online status window (within 120 seconds)."""
    now = datetime.now(timezone.utc)
    recent_seen = now - timedelta(seconds=45)
    stale_seen = now - timedelta(seconds=180)

    # 45 seconds ago -> should be considered online
    is_online_recent = (now - recent_seen).total_seconds() <= 120
    assert is_online_recent is True

    # 180 seconds ago (> 2 missed heartbeats) -> should be considered offline
    is_online_stale = (now - stale_seen).total_seconds() <= 120
    assert is_online_stale is False
