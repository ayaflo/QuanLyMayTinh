"""Automated tests for Policy and Time Governance (F1 & F4).
Tests HMAC integrity, policy creation, update, anti-IDOR, and audit logging.
"""

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from server.database import Base, get_db
from server.main import app
from server.models import Parent, Device, Policy, AuditLog
from server.security import (
    hash_password,
    create_access_token,
    calculate_policy_hmac,
    verify_policy_hmac
)
from server.services.policy_service import get_or_create_default_policy

# Test database setup (in-memory SQLite with StaticPool)
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(autouse=True)
def setup_database():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def client():
    """Test client with isolated database dependency override."""
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


def test_hmac_integrity_and_tampering():
    """Verify that calculate_policy_hmac and verify_policy_hmac accurately detect any data tampering."""
    dev_id = 1
    version = 1
    weekday = 90
    weekend = 150
    matrix = "1" * 336

    sig = calculate_policy_hmac(dev_id, version, weekday, weekend, matrix)
    assert len(sig) == 64
    assert verify_policy_hmac(dev_id, version, weekday, weekend, matrix, sig) is True

    # Tamper version
    assert verify_policy_hmac(dev_id, version + 1, weekday, weekend, matrix, sig) is False
    # Tamper quota
    assert verify_policy_hmac(dev_id, version, weekday + 15, weekend, matrix, sig) is False
    # Tamper schedule
    tampered_matrix = "0" + matrix[1:]
    assert verify_policy_hmac(dev_id, version, weekday, weekend, tampered_matrix, sig) is False


def test_get_or_create_default_policy():
    """Verify that default policy is seeded with 90m weekday, 150m weekend, and valid HMAC."""
    db = TestingSessionLocal()
    parent = Parent(username="test_parent", password_hash=hash_password("Password@123"))
    db.add(parent)
    db.commit()

    device = Device(parent_id=parent.id, device_fingerprint="TEST-UUID-001")
    db.add(device)
    db.commit()

    policy = get_or_create_default_policy(db, device.id)
    assert policy.version == 1
    assert policy.weekday_quota_minutes == 90
    assert policy.weekend_quota_minutes == 150
    assert len(policy.schedule_matrix) == 336
    assert verify_policy_hmac(
        device.id,
        policy.version,
        policy.weekday_quota_minutes,
        policy.weekend_quota_minutes,
        policy.schedule_matrix,
        policy.hmac_signature
    ) is True
    db.close()


def test_policy_api_get_and_post_with_audit(client):
    """Verify GET and POST /api/v1/policy API workflow, version increment, and audit log creation."""
    db = TestingSessionLocal()
    parent = Parent(username="parent_1", password_hash=hash_password("Admin@123"))
    db.add(parent)
    db.commit()

    device = Device(parent_id=parent.id, device_fingerprint="DEV-FINGERPRINT-01")
    db.add(device)
    db.commit()
    dev_id = device.id
    parent_id = parent.id
    db.close()

    parent_token = create_access_token({"sub": f"parent:{parent_id}", "parent_id": parent_id})

    # 1. GET policy as parent
    res = client.get(
        f"/api/v1/policy?device_id={dev_id}",
        headers={"Authorization": f"Bearer {parent_token}"}
    )
    assert res.status_code == 200
    data = res.json()
    assert data["version"] == 1
    assert data["weekday_quota_minutes"] == 90

    # 2. POST update policy
    new_matrix = "1" * 336
    update_res = client.post(
        f"/api/v1/policy?device_id={dev_id}",
        headers={"Authorization": f"Bearer {parent_token}"},
        json={
            "weekday_quota_minutes": 120,
            "weekend_quota_minutes": 180,
            "schedule_matrix": new_matrix
        }
    )
    assert update_res.status_code == 200
    updated_data = update_res.json()
    assert updated_data["version"] == 2
    assert updated_data["weekday_quota_minutes"] == 120
    assert updated_data["weekend_quota_minutes"] == 180

    # 3. Verify Audit Log was recorded
    db2 = TestingSessionLocal()
    audit = db2.query(AuditLog).filter(AuditLog.device_id == dev_id).first()
    assert audit is not None
    assert audit.action == "update_policy"
    assert "120" in audit.new_value
    db2.close()


def test_policy_api_anti_idor_protection(client):
    """Verify that a parent cannot update another parent's device policy (Anti-IDOR)."""
    db = TestingSessionLocal()
    p1 = Parent(username="parent_one", password_hash=hash_password("Pass1@123"))
    p2 = Parent(username="parent_two", password_hash=hash_password("Pass2@123"))
    db.add_all([p1, p2])
    db.commit()

    dev_of_p2 = Device(parent_id=p2.id, device_fingerprint="DEV-OF-P2")
    db.add(dev_of_p2)
    db.commit()
    target_dev_id = dev_of_p2.id
    p1_id = p1.id
    db.close()

    p1_token = create_access_token({"sub": f"parent:{p1_id}", "parent_id": p1_id})

    # Parent 1 attempts to update Parent 2's device
    res = client.post(
        f"/api/v1/policy?device_id={target_dev_id}",
        headers={"Authorization": f"Bearer {p1_token}"},
        json={"weekday_quota_minutes": 60}
    )
    assert res.status_code == 403
    assert "quyền" in res.json()["detail"].lower()
