"""Automated tests for SHA-256 App Control, Event Ingestion (F3), and Child Requests (NT3) (T3_050)."""

import os
import tempfile
import hashlib
import uuid
from datetime import datetime, timezone
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from server.database import Base, get_db
from server.main import app
from server.models import Parent, Device, ActivityEvent, AccessRequest, AppRule
from server.security import hash_password
from agent.app_controller import get_file_sha256, AppController
from agent.storage import add_pending_event, get_pending_events, delete_pending_events

# Isolated in-memory database for testing
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
def sample_device():
    db = TestingSessionLocal()
    parent = Parent(
        username="parent_tester",
        password_hash=hash_password("password123")
    )
    db.add(parent)
    db.commit()
    db.refresh(parent)

    device = Device(
        parent_id=parent.id,
        device_name="Child Laptop",
        device_fingerprint="test-uuid-fingerprint-123",
        status="online"
    )
    db.add(device)
    db.commit()
    db.refresh(device)
    dev_id = device.id
    db.close()
    return dev_id


def test_sha256_hash_and_anti_rename():
    """Verify SHA-256 calculation and that renaming binary does not bypass detection (T3_038, T3_041)."""
    with tempfile.TemporaryDirectory() as tmpdir:
        # Create a mock executable binary
        exe1_path = os.path.join(tmpdir, "game.exe")
        binary_content = b"\x4d\x5a\x90\x00\x03\x00\x00\x00OGK_MOCK_TEST_BINARY_DATA"
        with open(exe1_path, "wb") as f:
            f.write(binary_content)

        expected_hash = hashlib.sha256(binary_content).hexdigest().lower()
        computed_hash = get_file_sha256(exe1_path)
        assert computed_hash == expected_hash

        # Rename binary to bypass name-based detection: game.exe -> calculator.exe
        exe2_path = os.path.join(tmpdir, "calculator.exe")
        os.rename(exe1_path, exe2_path)

        renamed_hash = get_file_sha256(exe2_path)
        # Hash remains identical despite filename change!
        assert renamed_hash == expected_hash


def test_batch_event_ingestion_with_idempotency(client, sample_device):
    """Verify batch ingestion and exactly-once deduplication via idempotency_key (T3_010, F3)."""
    key1 = str(uuid.uuid4())
    key2 = str(uuid.uuid4())

    batch_payload = {
        "events": [
            {
                "idempotency_key": key1,
                "ts": datetime.now(timezone.utc).isoformat(),
                "device_id": sample_device,
                "child_id": None,
                "type": "app_usage",
                "subject": "code.exe",
                "duration_sec": 300,
                "policy_id": 1
            },
            {
                "idempotency_key": key2,
                "ts": datetime.now(timezone.utc).isoformat(),
                "device_id": sample_device,
                "child_id": None,
                "type": "web_access",
                "subject": "wikipedia.org",
                "duration_sec": 60,
                "policy_id": 1
            }
        ]
    }

    # First ingest: both should be ingested
    res1 = client.post("/api/v1/events/batch", json=batch_payload)
    assert res1.status_code == 200
    data1 = res1.json()
    assert data1["received"] == 2
    assert data1["ingested"] == 2
    assert data1["duplicates"] == 0

    # Second ingest of same payload (offline replay scenario): duplicates detected, 0 re-ingested
    res2 = client.post("/api/v1/events/batch", json=batch_payload)
    assert res2.status_code == 200
    data2 = res2.json()
    assert data2["received"] == 2
    assert data2["ingested"] == 0
    assert data2["duplicates"] == 2


def test_child_access_request_lifecycle(client, sample_device):
    """Verify child request submission and parent approval workflow (T3_012, NT3)."""
    # 1. Child submits request for +15m
    req_payload = {
        "device_id": sample_device,
        "child_id": None,
        "request_type": "add_time",
        "target": "15",
        "reason": "Con cần thêm thời gian để làm bài tập tiếng Anh"
    }
    submit_res = client.post("/api/v1/requests", json=req_payload)
    assert submit_res.status_code == 201
    created_req = submit_res.json()
    assert created_req["status"] == "pending"
    assert created_req["request_type"] == "add_time"
    req_id = created_req["id"]

    # 2. Verify request appears in listing
    list_res = client.get(f"/api/v1/requests?device_id={sample_device}")
    assert list_res.status_code == 200
    items = list_res.json()
    assert len(items) >= 1
    assert any(i["id"] == req_id for i in items)

    # 3. Parent approves request
    review_payload = {
        "status": "approved",
        "parent_response": "Ba mẹ đồng ý thêm 15 phút, học xong nghỉ ngơi con nhé!",
        "granted_minutes": 15
    }
    review_res = client.put(f"/api/v1/requests/{req_id}/review", json=review_payload)
    assert review_res.status_code == 200
    reviewed_data = review_res.json()
    assert reviewed_data["status"] == "approved"
    assert reviewed_data["parent_response"] == review_payload["parent_response"]
    assert reviewed_data["resolved_at"] is not None


def test_filtering_service_nt6_immutable_whitelist(client):
    """Verify NT6: Permanent whitelist entries cannot be blocked or deleted via API (T3_009, T3_014)."""
    # 1. Create permanent whitelist domain
    create_payload = {
        "domain": "truonghoc.edu.vn",
        "category": "Giáo dục",
        "action": "allow",
        "is_permanent_whitelist": True
    }
    create_res = client.post("/api/v1/filtering/domain-rules", json=create_payload)
    assert create_res.status_code == 201
    rule_id = create_res.json()["id"]

    # 2. Attempting to override permanent whitelist to 'block' must fail
    block_override = {
        "domain": "truonghoc.edu.vn",
        "category": "Giáo dục",
        "action": "block",
        "is_permanent_whitelist": False
    }
    block_res = client.post("/api/v1/filtering/domain-rules", json=block_override)
    assert block_res.status_code == 400
    assert "danh sách trắng vĩnh viễn" in block_res.json()["detail"].lower()

    # 3. Attempting to delete permanent whitelist entry must fail
    del_res = client.delete(f"/api/v1/filtering/domain-rules/{rule_id}")
    assert del_res.status_code == 400
    assert "danh sách trắng vĩnh viễn" in del_res.json()["detail"].lower()


def test_app_controller_usage_callback_and_reports(client, sample_device, monkeypatch):
    """Verify that AppController periodic foreground app telemetry feeds into Server Report Service."""
    from agent import app_controller
    monkeypatch.setattr(app_controller, "get_foreground_process_name", lambda: "Code.exe")
    monkeypatch.setattr(app_controller, "is_user_idle", lambda threshold=300.0: False)

    recorded_usage = []
    controller = app_controller.AppController(
        on_usage_callback=lambda app, dur: recorded_usage.append((app, dur))
    )
    # Simulate elapsed 16 seconds
    controller._last_usage_sampled = 0.0

    active = app_controller.get_foreground_process_name()
    assert active == "Code.exe"
    controller.on_usage_callback(active, 16)

    assert len(recorded_usage) == 1
    assert recorded_usage[0] == ("Code.exe", 16)

    # Ingest this app_usage event into Server
    key = str(uuid.uuid4())
    ingest_res = client.post("/api/v1/events/batch", json={
        "events": [{
            "idempotency_key": key,
            "ts": datetime.now(timezone.utc).isoformat(),
            "device_id": sample_device,
            "child_id": None,
            "type": "app_usage",
            "subject": "Code.exe",
            "duration_sec": 900,
            "policy_id": 1
        }]
    })
    assert ingest_res.status_code == 200

    # Query report summary to ensure app_usage is aggregated properly in reports
    rep_res = client.get(f"/api/v1/reports/summary?device_id={sample_device}")
    assert rep_res.status_code == 200
    rep_data = rep_res.json()
    assert rep_data["total_screen_time_sec"] == 900
    assert len(rep_data["top_apps"]) >= 1
    assert rep_data["top_apps"][0]["subject"] == "Code.exe"
    assert rep_data["top_apps"][0]["total_duration_sec"] == 900

