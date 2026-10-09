"""Tests for device enrollment logic and endpoints (T044).
Verifies 8-character pairing code generation, 10-minute expiration, and device claim flow.
"""

from datetime import datetime, timedelta, timezone
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from server.database import Base, get_db
from server.models import Parent, Device, PairingCode
from server.security import hash_password, create_access_token
from server.services.enrollment_service import generate_code, SAFE_CHARS
from server.main import app

# Setup isolated in-memory test database
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(autouse=True)
def setup_test_db():
    """Create fresh tables for every test."""
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        test_parent = Parent(
            id=1,
            username="enroll_parent",
            password_hash=hash_password("EnrollPass#123")
        )
        db.add(test_parent)
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
def parent_token():
    """Generate a valid parent JWT bearer token."""
    return create_access_token({
        "sub": "parent:1",
        "parent_id": 1,
        "username": "enroll_parent",
        "role": "parent"
    })


def test_generate_code_format():
    """Verify code is 8 characters and free from ambiguous letters."""
    for _ in range(50):
        code = generate_code(8)
        assert len(code) == 8
        for ch in code:
            assert ch in SAFE_CHARS
            assert ch not in ["0", "O", "1", "I", "L"]


def test_create_code_endpoint_unauthorized(client):
    """Calling POST /api/v1/enroll/create-code without auth must return 401."""
    response = client.post("/api/v1/enroll/create-code")
    assert response.status_code == 401


def test_create_code_endpoint_success(client, parent_token):
    """Parent creates 8-char pairing code valid for 10 minutes."""
    headers = {"Authorization": f"Bearer {parent_token}"}
    response = client.post("/api/v1/enroll/create-code", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert "code" in data
    assert len(data["code"]) == 8
    assert "expires_at" in data

    # Verify code exists in DB and is unused
    db = TestingSessionLocal()
    saved_code = db.query(PairingCode).filter(PairingCode.code == data["code"]).first()
    assert saved_code is not None
    assert saved_code.is_used is False
    assert saved_code.parent_id == 1
    db.close()


def test_claim_device_endpoint_success(client, parent_token):
    """Child agent pairs successfully with valid code and hardware fingerprint."""
    # 1. Parent creates code
    create_resp = client.post(
        "/api/v1/enroll/create-code",
        headers={"Authorization": f"Bearer {parent_token}"}
    )
    pairing_code = create_resp.json()["code"]

    # 2. Agent claims code
    claim_resp = client.post(
        "/api/v1/enroll/claim",
        json={
            "code": pairing_code,
            "device_fingerprint": "WIN-UUID-TEST-001",
            "device_name": "Laptop Em Be"
        }
    )
    assert claim_resp.status_code == 200
    claim_data = claim_resp.json()
    assert "device_id" in claim_data
    assert "access_token" in claim_data
    assert "refresh_token" in claim_data
    assert claim_data["token_type"] == "bearer"

    # 3. Check DB state
    db = TestingSessionLocal()
    code_record = db.query(PairingCode).filter(PairingCode.code == pairing_code).first()
    assert code_record.is_used is True

    device = db.query(Device).filter(Device.device_fingerprint == "WIN-UUID-TEST-001").first()
    assert device is not None
    assert device.parent_id == 1
    assert device.device_name == "Laptop Em Be"
    assert device.status == "online"
    db.close()


def test_claim_device_reuse_code_rejected(client, parent_token):
    """Attempting to use an already-used pairing code returns 400 Bad Request."""
    create_resp = client.post(
        "/api/v1/enroll/create-code",
        headers={"Authorization": f"Bearer {parent_token}"}
    )
    pairing_code = create_resp.json()["code"]

    # First claim succeeds
    client.post(
        "/api/v1/enroll/claim",
        json={"code": pairing_code, "device_fingerprint": "WIN-UUID-001"}
    )

    # Second claim fails
    reuse_resp = client.post(
        "/api/v1/enroll/claim",
        json={"code": pairing_code, "device_fingerprint": "WIN-UUID-002"}
    )
    assert reuse_resp.status_code == 400
    assert "Mã ghép đôi không tồn tại hoặc đã được sử dụng" in reuse_resp.json()["detail"]


def test_claim_device_expired_code_rejected(client):
    """Attempting to claim an expired code (> 10 mins) returns 400 Bad Request."""
    db = TestingSessionLocal()
    expired_code = PairingCode(
        parent_id=1,
        code="EXPIRED8",
        expires_at=datetime.now(timezone.utc) - timedelta(minutes=5),
        is_used=False
    )
    db.add(expired_code)
    db.commit()
    db.close()

    response = client.post(
        "/api/v1/enroll/claim",
        json={"code": "EXPIRED8", "device_fingerprint": "WIN-UUID-EXPIRED"}
    )
    assert response.status_code == 400
    assert "Mã ghép đôi đã hết hạn" in response.json()["detail"]
