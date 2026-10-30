"""Tests for Parent Control Fixes:
1. Lock warning countdown and cancellation
2. Pending command sync (WebSocket connect + Heartbeat fallback)
3. Hosts file synchronization and cleanup
"""

import json
import time
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from datetime import datetime, timezone
from server.database import Base, get_db
from server.main import app
from server.models import Parent, Device, DeviceCommand, AccessRequest, AuditLog
from server.security import hash_password, create_access_token
from server.routes.dashboard import format_local_time
from agent.lock_warning_dialog import LockWarningController
from agent.dns_configurator import sync_hosts_file, restore_hosts_file

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
def client(monkeypatch):
    """Test client with isolated database dependency override."""
    def override_get_db():
        db = TestingSessionLocal()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db
    monkeypatch.setattr("server.routes.ws.SessionLocal", TestingSessionLocal)
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()


def test_lock_warning_countdown_and_cancel():
    """Verify lock warning controller runs countdown and can be cancelled."""
    controller = LockWarningController()
    ticks = []
    locked = []

    controller.start_countdown(
        seconds=2,
        reason="Thử nghiệm khóa máy",
        on_lock_callback=lambda: locked.append(True),
        on_tick_callback=lambda rem: ticks.append(rem),
        show_gui=False
    )

    # Cancel immediately
    controller.cancel()
    time.sleep(0.5)

    assert controller._cancelled is True
    assert len(locked) == 0


def test_lock_warning_countdown_finishes():
    """Verify lock warning controller triggers lock callback when countdown reaches 0."""
    controller = LockWarningController()
    locked = []

    controller.start_countdown(
        seconds=1,
        reason="Hết giờ",
        on_lock_callback=lambda: locked.append(True),
        show_gui=False
    )

    time.sleep(1.3)
    assert len(locked) == 1


def test_pending_commands_delivered_on_websocket_connect(client):
    """Verify pending commands dispatched while device is offline are delivered on connect."""
    db = TestingSessionLocal()
    parent = Parent(username="parent_pending", password_hash=hash_password("Pass@123"))
    db.add(parent)
    db.commit()

    device = Device(parent_id=parent.id, device_fingerprint="DEV-PENDING-001", device_name="Kid PC")
    db.add(device)
    db.commit()
    dev_id = device.id

    # Create a pending add_time command before device connects
    cmd = DeviceCommand(
        device_id=dev_id,
        command_type="add_time",
        payload=json.dumps({"minutes": 15}),
        status="pending"
    )
    db.add(cmd)
    db.commit()
    cmd_id = cmd.id
    db.close()

    dev_token = create_access_token({"sub": f"device:{dev_id}", "device_id": dev_id})

    # Device connects -> Server should flush pending command immediately
    with client.websocket_connect(f"/ws/device/{dev_id}?token={dev_token}") as ws:
        msg_str = ws.receive_text()
        msg = json.loads(msg_str)
        assert msg["action"] == "add_time"
        assert msg["payload"]["minutes"] == 15

    # Check status changed to delivered
    db2 = TestingSessionLocal()
    updated_cmd = db2.query(DeviceCommand).filter(DeviceCommand.id == cmd_id).first()
    assert updated_cmd.status == "delivered"
    assert updated_cmd.delivered_at is not None
    db2.close()


def test_pending_commands_delivered_in_heartbeat(client):
    """Verify pending commands are returned in heartbeat response as fallback."""
    db = TestingSessionLocal()
    parent = Parent(username="parent_hb", password_hash=hash_password("Pass@123"))
    db.add(parent)
    db.commit()

    device = Device(parent_id=parent.id, device_fingerprint="DEV-HB-001", device_name="Kid PC")
    db.add(device)
    db.commit()
    dev_id = device.id

    cmd = DeviceCommand(
        device_id=dev_id,
        command_type="add_time",
        payload=json.dumps({"minutes": 15}),
        status="pending"
    )
    db.add(cmd)
    db.commit()
    cmd_id = cmd.id
    db.close()

    dev_token = create_access_token({"sub": f"device:{dev_id}", "device_id": dev_id})

    # Send heartbeat
    res = client.post(
        "/api/v1/heartbeat",
        headers={"Authorization": f"Bearer {dev_token}"},
        json={"device_fingerprint": "DEV-HB-001"}
    )
    assert res.status_code == 200
    data = res.json()
    assert "pending_commands" in data
    assert len(data["pending_commands"]) == 1
    assert data["pending_commands"][0]["action"] == "add_time"
    assert data["pending_commands"][0]["payload"]["minutes"] == 15

    # Check marked delivered
    db2 = TestingSessionLocal()
    updated_cmd = db2.query(DeviceCommand).filter(DeviceCommand.id == cmd_id).first()
    assert updated_cmd.status == "delivered"
    db2.close()


def test_sync_hosts_file_and_cleanup(tmp_path):
    """Verify hosts file synchronization writes blocked entries and cleans up cleanly."""
    fake_hosts = tmp_path / "hosts"
    initial_content = "127.0.0.1 localhost\n::1 localhost\n"
    fake_hosts.write_text(initial_content, encoding="utf-8")

    blocked = ["facebook.com", "tiktok.com"]
    ok = sync_hosts_file(blocked, hosts_path=str(fake_hosts))
    assert ok is True

    updated_content = fake_hosts.read_text(encoding="utf-8")
    assert "0.0.0.0 facebook.com" in updated_content
    assert "0.0.0.0 www.facebook.com" in updated_content
    assert "0.0.0.0 tiktok.com" in updated_content

    # Restore hosts file
    restore_ok = restore_hosts_file(hosts_path=str(fake_hosts))
    assert restore_ok is True
    cleaned_content = fake_hosts.read_text(encoding="utf-8")
    assert "facebook.com" not in cleaned_content
    assert "tiktok.com" not in cleaned_content
    assert "127.0.0.1 localhost" in cleaned_content


def test_vietnam_local_time_formatting():
    """Verify UTC datetime is correctly converted to Vietnam local time (UTC+7 / ICT)."""
    # 08:16:00 UTC -> 15:16:00 Vietnam time
    utc_naive = datetime(2026, 10, 29, 8, 16, 0)
    assert format_local_time(utc_naive, "%H:%M %d/%m") == "15:16 29/10"
    assert format_local_time(utc_naive, "%H:%M:%S") == "15:16:00"
    assert format_local_time(utc_naive, "%H:%M:%S %d/%m/%Y") == "15:16:00 29/10/2026"

    # With explicit UTC timezone
    utc_aware = datetime(2026, 10, 29, 8, 16, 0, tzinfo=timezone.utc)
    assert format_local_time(utc_aware, "%H:%M %d/%m") == "15:16 29/10"

    # None input handling
    assert format_local_time(None, "%H:%M:%S") == "Chưa có"
    assert format_local_time(None, "%H:%M %d/%m") == ""


def test_dashboard_renders_vietnam_time_for_requests_and_audit(client):
    """Verify web dashboard renders requests and audit logs in Vietnam Local Time (UTC+7)."""
    db = TestingSessionLocal()
    parent = Parent(username="vn_parent", password_hash=hash_password("password123"))
    db.add(parent)
    db.commit()

    # UTC 08:16:00 should display as 15:16:00
    test_utc_dt = datetime(2026, 10, 29, 8, 16, 0, tzinfo=timezone.utc)
    dev = Device(
        parent_id=parent.id,
        device_fingerprint="DEV-TIME-001",
        device_name="Máy Con Học Tập",
        status="online",
        last_seen=test_utc_dt
    )
    db.add(dev)
    db.commit()

    req = AccessRequest(
        device_id=dev.id,
        request_type="add_time",
        target="15",
        reason="Con xin thêm 15p học bài",
        status="pending",
        created_at=test_utc_dt
    )
    db.add(req)

    audit = AuditLog(
        parent_id=parent.id,
        device_id=dev.id,
        action="enroll_device",
        new_value="Ghép đôi thiết bị 'Máy Con Học Tập' thành công",
        created_at=test_utc_dt
    )
    db.add(audit)
    db.commit()
    parent_id = parent.id
    dev_id = dev.id
    db.close()

    # Log in and check /devices
    token = create_access_token({"sub": f"parent:{parent_id}", "parent_id": parent_id, "role": "parent"})
    client.cookies.set("access_token", token)
    res = client.get("/devices")
    assert res.status_code == 200
    html = res.text
    # Device ID must display correctly
    assert f"ID: #{dev_id}" in html

    # Child request must display 'Gửi lúc: 15:16 29/10' (not 08:16 29/10)
    assert "Gửi lúc: 15:16 29/10" in html

    # Audit log must display '15:16:00 29/10/2026' (not 08:16:00)
    assert "15:16:00 29/10/2026" in html


def test_pairing_code_timezone_and_audit_log(client):
    """Verify pairing code returns timezone-aware expires_at and pairing creates AuditLog."""
    db = TestingSessionLocal()
    parent = Parent(username="enroll_parent", password_hash=hash_password("password123"))
    db.add(parent)
    db.commit()
    parent_id = parent.id
    db.close()

    token = create_access_token({"sub": f"parent:{parent_id}", "parent_id": parent_id, "role": "parent"})

    # 1. Parent generates pairing code
    create_res = client.post(
        "/api/v1/enroll/create-code",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert create_res.status_code == 200
    code_data = create_res.json()
    assert "code" in code_data
    assert "expires_at" in code_data
    assert code_data["expires_at"].endswith("Z") or "+00:00" in code_data["expires_at"]
    pair_code = code_data["code"]

    # 2. Child agent claims code
    claim_res = client.post(
        "/api/v1/enroll/claim",
        json={
            "code": pair_code,
            "device_fingerprint": "DEV-FINGERPRINT-NEW",
            "device_name": "Máy Con Windows"
        }
    )
    assert claim_res.status_code == 200

    # 3. Verify audit log entry was created for enroll_device
    db2 = TestingSessionLocal()
    enroll_log = db2.query(AuditLog).filter(
        AuditLog.parent_id == parent_id,
        AuditLog.action == "enroll_device"
    ).first()
    assert enroll_log is not None
    assert "Ghép đôi thiết bị 'Máy Con Windows' thành công" in enroll_log.new_value
    db2.close()


def test_clean_10_domains_and_notepad_blocking(client, monkeypatch):
    """Verify clean 10-domain seed list and Notepad app blocking (F2)."""
    from server.seed_domains import seed_domain_rules, SEED_DOMAINS_DATA, SEED_APP_RULES_DATA
    from server.models import DomainRule, AppRule
    from agent.app_controller import AppController

    db = TestingSessionLocal()
    # 1. Verify representative domains
    assert len(SEED_DOMAINS_DATA) == 9
    seed_domain_rules(db)
    domains = db.query(DomainRule).all()
    assert len(domains) == 9

    # 2. Verify notepad.exe in default app rules
    app_names = [a["app_name"] for a in SEED_APP_RULES_DATA]
    assert "notepad.exe" in app_names
    db.close()

    # 3. Test API allows adding app rule without SHA-256 hash (auto-generates)
    res = client.post("/api/v1/filtering/app-rules", json={
        "app_name": "notepad",
        "action": "block",
        "description": "Thử nghiệm khóa Notepad"
    })
    assert res.status_code == 201
    rule_data = res.json()
    assert rule_data["app_name"] == "notepad.exe"
    assert len(rule_data["sha256_hash"]) == 64

    # 4. Test AppController terminates notepad process
    terminated = []

    class FakeProc:
        def __init__(self, pid, name, exe):
            self.info = {'pid': pid, 'name': name, 'exe': exe}
            self.killed = False

        def terminate(self):
            self.killed = True

        def kill(self):
            self.killed = True

    proc_notepad = FakeProc(9999, "Notepad.exe", r"C:\Windows\System32\notepad.exe")

    import psutil
    monkeypatch.setattr(psutil, "process_iter", lambda attrs: [proc_notepad])

    rules_map = {
        rule_data["sha256_hash"]: {
            "name": "notepad.exe",
            "action": "block",
            "description": "Thử nghiệm khóa Notepad"
        }
    }
    controller = AppController(rules_provider=lambda: rules_map)
    killed_list = controller.scan_and_enforce()

    assert len(killed_list) == 1
    assert killed_list[0]["app_name"] == "Notepad.exe"
    assert proc_notepad.killed is True


def test_child_request_reviewed_dispatches_notification_and_web_clean(client):
    """Verify:
    1. Web template does not render parent_response text bubble.
    2. Reviewing request as 'rejected' dispatches 'request_reviewed' command to agent.
    3. Reviewing request as 'approved' for unblocking dispatches 'request_reviewed' command.
    """
    import os
    # 1. Template check
    template_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "dashboard", "templates", "devices.html")
    with open(template_path, "r", encoding="utf-8") as f:
        content = f.read()
    assert "💬 Phản hồi:" not in content

    # 2. Setup DB data
    db = TestingSessionLocal()
    parent = Parent(username="parent_req_test", password_hash=hash_password("Pass@123"))
    db.add(parent)
    db.commit()

    device = Device(parent_id=parent.id, device_fingerprint="DEV-REQ-001", device_name="Kid PC")
    db.add(device)
    db.commit()

    req_reject = AccessRequest(
        device_id=device.id,
        request_type="unblock_domain",
        target="roblox.com",
        reason="Em muốn chơi game một chút",
        status="pending"
    )
    req_approve = AccessRequest(
        device_id=device.id,
        request_type="unblock_domain",
        target="scratch.mit.edu",
        reason="Em học lập trình Scratch",
        status="pending"
    )
    db.add_all([req_reject, req_approve])
    db.commit()
    req_reject_id = req_reject.id
    req_approve_id = req_approve.id
    dev_id = device.id
    db.close()

    # 3. Parent rejects unblock request
    token = create_access_token({"sub": "parent_req_test", "role": "parent"})
    res = client.put(
        f"/api/v1/requests/{req_reject_id}/review",
        json={
            "status": "rejected",
            "parent_response": "Chưa học xong bài tập con nhé"
        },
        headers={"Authorization": f"Bearer {token}"}
    )
    assert res.status_code == 200

    # Verify DeviceCommand was created for rejection
    db = TestingSessionLocal()
    reject_cmd = db.query(DeviceCommand).filter(
        DeviceCommand.device_id == dev_id,
        DeviceCommand.command_type == "request_reviewed"
    ).order_by(DeviceCommand.id.desc()).first()
    assert reject_cmd is not None
    payload = json.loads(reject_cmd.payload)
    assert payload["status"] == "rejected"
    assert payload["request_type"] == "unblock_domain"
    assert payload["target"] == "roblox.com"

    # 4. Parent approves unblock request
    res2 = client.put(
        f"/api/v1/requests/{req_approve_id}/review",
        json={
            "status": "approved",
            "parent_response": "Đồng ý để con học"
        },
        headers={"Authorization": f"Bearer {token}"}
    )
    assert res2.status_code == 200

    approve_cmd = db.query(DeviceCommand).filter(
        DeviceCommand.device_id == dev_id,
        DeviceCommand.command_type == "request_reviewed"
    ).order_by(DeviceCommand.id.desc()).first()
    assert approve_cmd is not None
    payload2 = json.loads(approve_cmd.payload)
    assert payload2["status"] == "approved"
    assert payload2["request_type"] == "unblock_domain"
    assert payload2["target"] == "scratch.mit.edu"
    db.close()


def test_browser_incognito_policy_and_bypass_browser_blocking(monkeypatch):
    """Verify:
    1. SEED_APP_RULES_DATA includes bypass browsers (tor, opera, opera_gx, epic, ur).
    2. AppController terminates bypass browsers like opera.exe and tor.exe.
    3. disable_browser_doh executes without error.
    """
    from server.seed_domains import SEED_APP_RULES_DATA
    from agent.app_controller import AppController
    app_names = {r["app_name"].lower() for r in SEED_APP_RULES_DATA}
    assert "tor.exe" in app_names
    assert "tor-browser.exe" in app_names
    assert "opera.exe" in app_names
    assert "opera_gx.exe" in app_names
    assert "epic.exe" in app_names
    assert "ur.exe" in app_names

    # Test AppController terminates Opera and Tor
    class FakeProc:
        def __init__(self, pid, name, exe):
            self.info = {'pid': pid, 'name': name, 'exe': exe}
            self.killed = False

        def terminate(self):
            self.killed = True

        def kill(self):
            self.killed = True

    proc_opera = FakeProc(1234, "opera.exe", r"C:\Users\User\AppData\Local\Programs\Opera\opera.exe")
    proc_tor = FakeProc(5678, "tor.exe", r"C:\Tor Browser\Browser\TorBrowser\Tor\tor.exe")

    import psutil
    monkeypatch.setattr(psutil, "process_iter", lambda attrs: [proc_opera, proc_tor])

    rules_map = {
        "hash_opera": {"name": "opera.exe", "action": "block"},
        "hash_tor": {"name": "tor.exe", "action": "block"},
    }
    controller = AppController(rules_provider=lambda: rules_map)
    killed = controller.scan_and_enforce()

    assert len(killed) == 2
    assert proc_opera.killed is True
    assert proc_tor.killed is True

    # Test disable_browser_doh and restore_browser_doh
    from agent.dns_configurator import disable_browser_doh, restore_browser_doh, reset_browser_connections
    assert disable_browser_doh() is True
    assert restore_browser_doh() is True

    # Test reset_browser_connections with mock Chromium NetworkService
    class MockChromiumProc:
        def __init__(self, pid, name, cmdline):
            self.pid = pid
            self.info = {'pid': pid, 'name': name}
            self._cmdline = cmdline
            self.killed = False

        def cmdline(self):
            return self._cmdline

        def kill(self):
            self.killed = True

    mock_chrome_net = MockChromiumProc(
        8888, "chrome.exe", ["chrome.exe", "--type=utility", "--utility-sub-type=network.mojom.NetworkService"]
    )
    mock_chrome_render = MockChromiumProc(
        8889, "chrome.exe", ["chrome.exe", "--type=renderer"]
    )
    monkeypatch.setattr(psutil, "process_iter", lambda attrs: [mock_chrome_net, mock_chrome_render])
    monkeypatch.setattr(psutil, "net_connections", lambda kind: [])

    reset_count = reset_browser_connections()
    assert mock_chrome_net.killed is True
    assert mock_chrome_render.killed is False
    assert reset_count >= 1


def test_download_ogk_agent_zip_and_ui():
    """Verify downloading OGK.zip works and the top header displays the download button instead of realtime monitor."""
    from fastapi.testclient import TestClient
    from server.main import app

    client = TestClient(app)
    res_zip = client.get("/download/OGK.zip")
    assert res_zip.status_code == 200
    assert "application/zip" in res_zip.headers.get("content-type", "")
    assert 'filename="OGK.zip"' in res_zip.headers.get("content-disposition", "")

    res_agent = client.get("/download/agent")
    assert res_agent.status_code == 200
    assert "application/zip" in res_agent.headers.get("content-type", "")

    # Check UI replacement
    res_login = client.get("/login")
    assert res_login.status_code == 200
    assert "Giám Sát Thời Gian Thực" not in res_login.text
    assert "/download/OGK.zip" in res_login.text
    assert "Tải Agent" in res_login.text


def test_app_rule_with_custom_sha256_hash(client):
    """Verify creating app rule with valid custom SHA-256 hash succeeds and is stored."""
    valid_hash = "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
    payload = {
        "app_name": "malicious_game.exe",
        "action": "block",
        "description": "Block harmful game by exact binary hash",
        "sha256_hash": valid_hash.upper()  # Test normalization to lowercase
    }
    res = client.post("/api/v1/filtering/app-rules", json=payload)
    assert res.status_code == 201
    data = res.json()
    assert data["app_name"] == "malicious_game.exe"
    assert data["sha256_hash"] == valid_hash.lower()


def test_app_rule_with_invalid_sha256_hash(client):
    """Verify creating app rule with invalid SHA-256 hash returns 400 Bad Request."""
    # Test short hash
    res_short = client.post("/api/v1/filtering/app-rules", json={
        "app_name": "game.exe",
        "sha256_hash": "123456"
    })
    assert res_short.status_code == 400
    assert "64 ký tự" in res_short.json()["detail"]

    # Test non-hex characters
    res_invalid_hex = client.post("/api/v1/filtering/app-rules", json={
        "app_name": "game.exe",
        "sha256_hash": "g" * 64
    })
    assert res_invalid_hex.status_code == 400
    assert "64 ký tự" in res_invalid_hex.json()["detail"]


def test_app_rule_auto_hash_when_omitted(client):
    """Verify creating app rule without sha256_hash generates a deterministic hash."""
    import hashlib
    res = client.post("/api/v1/filtering/app-rules", json={
        "app_name": "notepad.exe",
        "action": "block"
    })
    assert res.status_code == 201
    data = res.json()
    expected_hash = hashlib.sha256("notepad.exe".encode()).hexdigest()
    assert data["sha256_hash"] == expected_hash








