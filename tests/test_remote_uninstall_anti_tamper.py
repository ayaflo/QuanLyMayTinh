"""Tests for Remote Encrypted Uninstall and System Tray Anti-Tamper Protection."""

import os
import sys
import pytest
from unittest.mock import patch
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from server.database import Base, get_db
from server.models import Parent
from server.security import hash_password, create_access_token
from server.main import app

from agent.uninstall import (
    verify_uninstall_authorization,
    ensure_encrypted_vault,
    ENCRYPTED_VAULT_FILE
)
from agent.tray import init_tray_icon

# Isolated in-memory DB
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture
def setup_test_db():
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        p = Parent(id=1, username="parent_test", password_hash=hash_password("Pass#12345"))
        db.add(p)
        db.commit()
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)


@pytest.fixture
def client(setup_test_db):
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
    return create_access_token(data={"sub": "parent:1", "parent_id": 1, "username": "parent_test"})


def test_anti_tamper_blocks_unauthorized_uninstall(monkeypatch):
    """Verify that verify_uninstall_authorization rejects empty credentials when not in test mode."""
    monkeypatch.delenv("OGK_TEST_MODE", raising=False)
    assert verify_uninstall_authorization(token=None, unlock_key=None) is False
    assert verify_uninstall_authorization(token="", unlock_key="") is False


def test_anti_tamper_accepts_valid_unlock_key(monkeypatch):
    """Verify that the valid UNINSTALL_MASTER_KEY passes and invalid keys are rejected."""
    monkeypatch.delenv("OGK_TEST_MODE", raising=False)
    ensure_encrypted_vault()
    assert os.path.exists(ENCRYPTED_VAULT_FILE)
    # Master key matches vault encryption -> True
    assert verify_uninstall_authorization(unlock_key="OGK_STATIC_MASTER_UNINSTALL_KEY_2026") is True
    # Wrong fake key fails to decrypt vault -> False
    assert verify_uninstall_authorization(unlock_key="wrong_fake_key_12345") is False


def test_tray_locks_autostart_permanently():
    """Verify system tray menu item for autostart is locked and informative."""
    icon = init_tray_icon()
    menu_titles = [item.text for item in icon.menu]
    assert any("Khởi động cùng Windows (Bắt buộc)" in t for t in menu_titles)
    assert any("Thoát" in t for t in menu_titles)


def test_parent_delete_device_dispatches_uninstall_ws_command(client, parent_token):
    """Verify DELETE /api/v1/devices/{device_id} generates cryptographic unlock key and sends uninstall WS command."""
    # 1. Enroll device
    code_res = client.post(
        "/api/v1/enroll/create-code",
        headers={"Authorization": f"Bearer {parent_token}"}
    )
    assert code_res.status_code == 200
    pairing_code = code_res.json()["code"]

    claim_res = client.post(
        "/api/v1/enroll/claim",
        json={
            "code": pairing_code,
            "device_fingerprint": "mock_hw_fingerprint_123",
            "device_name": "Child-PC"
        }
    )
    assert claim_res.status_code == 200
    dev_id = claim_res.json()["device_id"]

    # 2. Mock ws_manager to capture outgoing command
    sent_commands = []

    async def mock_send_command(target_dev_id, message):
        sent_commands.append({"device_id": target_dev_id, "message": message})
        return True

    with patch("server.services.connection_manager.ws_manager.send_command", side_effect=mock_send_command):
        del_res = client.delete(
            f"/api/v1/devices/{dev_id}",
            headers={"Authorization": f"Bearer {parent_token}"}
        )
        assert del_res.status_code == 200
        assert del_res.json()["status"] == "success"

        # Check commands dispatched in order: 1. purge_local_data -> 2. uninstall
        assert len(sent_commands) == 2
        assert sent_commands[0]["device_id"] == dev_id
        assert sent_commands[0]["message"]["action"] == "purge_local_data"

        cmd = sent_commands[1]
        assert cmd["device_id"] == dev_id
        assert cmd["message"]["action"] == "uninstall"
        payload = cmd["message"]["payload"]
        assert "unlock_key" in payload
        assert "token" in payload
        assert payload["reason"] == "uninstalled_by_parent"
