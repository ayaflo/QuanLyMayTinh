"""Automated tests for WebSocket real-time channel and emergency commands (< 5s).
"""

import json
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from server.database import Base, get_db
from server.main import app
from server.models import Parent, Device, AuditLog
from server.security import hash_password, create_access_token

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


def test_websocket_connection_and_emergency_command(client):
    """Verify WebSocket connection, command dispatch, and real-time delivery."""
    db = TestingSessionLocal()
    parent = Parent(username="parent_ws", password_hash=hash_password("Pass@123"))
    db.add(parent)
    db.commit()

    device = Device(parent_id=parent.id, device_fingerprint="DEV-WS-001", device_name="Con PC")
    db.add(device)
    db.commit()
    dev_id = device.id
    parent_id = parent.id
    db.close()

    dev_token = create_access_token({"sub": f"device:{dev_id}", "device_id": dev_id})
    parent_token = create_access_token({"sub": f"parent:{parent_id}", "parent_id": parent_id})

    # Connect WebSocket client simulating child agent
    with client.websocket_connect(f"/ws/device/{dev_id}?token={dev_token}") as ws:
        # Dispatch emergency command from parent API
        res = client.post(
            f"/api/v1/devices/{dev_id}/command",
            headers={"Authorization": f"Bearer {parent_token}"},
            json={"command_type": "lock_now"}
        )
        assert res.status_code == 200
        cmd_data = res.json()
        assert cmd_data["command_type"] == "lock_now"

        # Receive real-time command on WebSocket client (< 5s)
        msg_str = ws.receive_text()
        msg = json.loads(msg_str)
        assert msg["action"] == "lock_now"
        assert "timestamp" in msg

    # Verify AuditLog created
    db2 = TestingSessionLocal()
    audit = db2.query(AuditLog).filter(AuditLog.device_id == dev_id).first()
    assert audit is not None
    assert "command:lock_now" in audit.action
    db2.close()
