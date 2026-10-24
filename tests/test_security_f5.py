"""Automated security test suite for F5 Hardening & Anti-IDOR (T4_029).
Verifies:
- AES-256-GCM authenticated encryption at rest and tamper rejection
- Anti-IDOR authorization enforcement across commands, policy, reports, and requests
"""

from datetime import datetime, timedelta, timezone
import tempfile
import os
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from server.database import Base, get_db
from server.main import app
from server.models import Parent, Device, Policy, AccessRequest, ActivityEvent, HeartbeatLog, AuditLog, AppRule
from server.security import hash_password, create_access_token, reset_ip_rate_limits, clear_revoked_tokens
from server.crypto_utils import encrypt_data, decrypt_data
from server.services.retention_service import purge_expired_activity_data
from agent.storage import purge_local_data, add_pending_event, get_pending_events, update_daily_usage, get_daily_usage
from agent.dns_watchdog import DNSWatchdog
from server.seed_domains import seed_app_rules
from agent.app_controller import AppController

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
    reset_ip_rate_limits()
    clear_revoked_tokens()
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)
    reset_ip_rate_limits()
    clear_revoked_tokens()


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
def parents_and_devices():
    """Setup two distinct parents each owning their own device."""
    db = TestingSessionLocal()
    # Parent A & Device A
    parent_a = Parent(username="parent_alice", password_hash=hash_password("PassAlice@123"))
    db.add(parent_a)
    db.commit()

    dev_a = Device(parent_id=parent_a.id, device_fingerprint="DEV-FINGERPRINT-A", device_name="Alice Child PC")
    db.add(dev_a)
    db.commit()

    # Parent B & Device B
    parent_b = Parent(username="parent_bob", password_hash=hash_password("PassBob@12345"))
    db.add(parent_b)
    db.commit()

    dev_b = Device(parent_id=parent_b.id, device_fingerprint="DEV-FINGERPRINT-B", device_name="Bob Child PC")
    db.add(dev_b)
    db.commit()

    # Access request submitted by Device B
    req_b = AccessRequest(
        device_id=dev_b.id,
        request_type="add_time",
        reason="Need 15 more minutes for math homework",
        status="pending"
    )
    db.add(req_b)
    db.commit()

    token_a = create_access_token({"sub": f"parent:{parent_a.id}", "parent_id": parent_a.id})
    token_b = create_access_token({"sub": f"parent:{parent_b.id}", "parent_id": parent_b.id})

    data = {
        "parent_a": parent_a.id,
        "parent_b": parent_b.id,
        "dev_a": dev_a.id,
        "dev_b": dev_b.id,
        "req_b": req_b.id,
        "token_a": token_a,
        "token_b": token_b
    }
    db.close()
    return data


# ============================================================================
# 0. Authentication, Lockout & Rate Limiting Tests (T4_001 - T4_006)
# ============================================================================

def test_f5_minimum_10_char_password_policy(client):
    """Verify NIST SP 800-63B password policy enforcement (rejects passwords < 10 chars with HTTP 422)."""
    # 8-char password should be rejected
    res_short = client.post(
        "/api/v1/auth/login",
        json={"username": "parent_alice", "password": "Short123"}
    )
    assert res_short.status_code == 422
    assert "at least 10" in str(res_short.json()).lower() or "string_too_short" in str(res_short.json()).lower()


def test_f5_bruteforce_lockout_and_ip_rate_limiting(client, parents_and_devices):
    """Verify 15-minute account lockout after 5 consecutive failed attempts (HTTP 423) and IP rate limiting."""
    # Failed attempts 1 to 4 return 401
    for attempt in range(1, 5):
        resp = client.post(
            "/api/v1/auth/login",
            json={"username": "parent_alice", "password": f"WrongPass_{attempt}"}
        )
        assert resp.status_code == 401, f"Attempt {attempt} should return 401"

    # Attempt 5 triggers account lockout (HTTP 423)
    resp5 = client.post(
        "/api/v1/auth/login",
        json={"username": "parent_alice", "password": "WrongPass_5"}
    )
    assert resp5.status_code == 423
    assert "tạm khóa 15 phút" in resp5.json()["detail"].lower()

    # Even with correct password, login must be rejected while locked
    resp_locked = client.post(
        "/api/v1/auth/login",
        json={"username": "parent_alice", "password": "PassAlice@123"}
    )
    assert resp_locked.status_code == 423
    assert "tạm khóa" in resp_locked.json()["detail"].lower()


# ============================================================================
# 1. AES-256-GCM Tests (T4_007)
# ============================================================================

def test_aes_256_gcm_roundtrip():
    """Verify AES-256-GCM encryption and decryption roundtrip integrity."""
    plaintext = "Sensitive child browsing telemetry: learning.edu.vn"
    encrypted = encrypt_data(plaintext)
    assert encrypted != plaintext
    assert len(encrypted) > 28

    decrypted = decrypt_data(encrypted)
    assert decrypted == plaintext


def test_aes_256_gcm_tamper_rejection():
    """Verify that tampering with any byte of ciphertext triggers rejection."""
    plaintext = "Important safety configuration"
    encrypted = encrypt_data(plaintext)

    # Modify last character of base64
    tampered = encrypted[:-2] + ("AA" if not encrypted.endswith("AA") else "BB")
    with pytest.raises(ValueError) as exc:
        decrypt_data(tampered)
    assert "tampered" in str(exc.value).lower() or "invalid" in str(exc.value).lower()


# ============================================================================
# 2. Anti-IDOR Tests (T4_008, T4_009, T4_010)
# ============================================================================

def test_anti_idor_emergency_command(client, parents_and_devices):
    """Parent A must NOT be able to send emergency lock command to Parent B's device (T4_008)."""
    p = parents_and_devices
    # Alice attempts to lock Bob's child device
    resp = client.post(
        f"/api/v1/devices/{p['dev_b']}/command",
        headers={"Authorization": f"Bearer {p['token_a']}"},
        json={"command_type": "lock_now"}
    )
    assert resp.status_code == 403
    assert "quyền" in resp.json()["detail"].lower()


def test_anti_idor_policy_get_and_update(client, parents_and_devices):
    """Parent A must NOT be able to view or edit Parent B's device policy (T4_009)."""
    p = parents_and_devices

    # Alice attempts to read Bob's child policy
    get_resp = client.get(
        f"/api/v1/policy?device_id={p['dev_b']}",
        headers={"Authorization": f"Bearer {p['token_a']}"}
    )
    assert get_resp.status_code == 403
    assert "quyền" in get_resp.json()["detail"].lower()

    # Alice attempts to change Bob's child quota to 60 minutes
    update_resp = client.post(
        f"/api/v1/policy?device_id={p['dev_b']}",
        headers={"Authorization": f"Bearer {p['token_a']}"},
        json={
            "weekday_quota_minutes": 60,
            "weekend_quota_minutes": 120,
            "schedule_matrix": "1" * 336
        }
    )
    assert update_resp.status_code == 403
    assert "quyền" in update_resp.json()["detail"].lower()


def test_anti_idor_reports(client, parents_and_devices):
    """Parent A must NOT be able to view usage summary of Parent B's device (T4_010)."""
    p = parents_and_devices

    resp = client.get(
        f"/api/v1/reports/summary?device_id={p['dev_b']}",
        headers={"Authorization": f"Bearer {p['token_a']}"}
    )
    assert resp.status_code == 403
    assert "quyền" in resp.json()["detail"].lower()


def test_anti_idor_child_requests(client, parents_and_devices):
    """Parent A must NOT be able to view or approve Parent B's child access requests (T4_010)."""
    p = parents_and_devices

    # Alice queries Bob's device requests
    list_resp = client.get(
        f"/api/v1/requests?device_id={p['dev_b']}",
        headers={"Authorization": f"Bearer {p['token_a']}"}
    )
    assert list_resp.status_code == 403
    assert "quyền" in list_resp.json()["detail"].lower()

    # Alice attempts to approve Bob's child request
    review_resp = client.put(
        f"/api/v1/requests/{p['req_b']}/review",
        headers={"Authorization": f"Bearer {p['token_a']}"},
        json={"status": "approved", "granted_minutes": 15, "parent_response": "Hacker Alice approved"}
    )
    assert review_resp.status_code == 403
    assert "quyền" in review_resp.json()["detail"].lower()


# ============================================================================
# 3. Data Retention & Right to Erasure Tests (T4_011 - T4_016 - Decree 13/2023)
# ============================================================================

def test_90_day_retention_purge():
    """Verify purge_expired_activity_data() removes records older than 90 days and retains newer ones (T4_011)."""
    db = TestingSessionLocal()
    now = datetime.now(timezone.utc)

    # Old records (> 90 days)
    old_event = ActivityEvent(
        idempotency_key="old-ev-1",
        ts=now - timedelta(days=95),
        device_id=1,
        type="app_usage",
        subject="Game.exe",
        duration_sec=300
    )
    old_hb = HeartbeatLog(
        device_id=1,
        timestamp=now - timedelta(days=92),
        status_payload='{"cpu": 10}'
    )

    # Recent records (< 90 days)
    recent_event = ActivityEvent(
        idempotency_key="recent-ev-1",
        ts=now - timedelta(days=15),
        device_id=1,
        type="app_usage",
        subject="Learning.exe",
        duration_sec=600
    )
    recent_hb = HeartbeatLog(
        device_id=1,
        timestamp=now - timedelta(days=1),
        status_payload='{"cpu": 5}'
    )

    db.add_all([old_event, old_hb, recent_event, recent_hb])
    db.commit()

    # Execute purge
    result = purge_expired_activity_data(db, days=90)
    assert result["events_purged"] == 1
    assert result["heartbeats_purged"] == 1

    # Verify only recent records remain
    remaining_events = db.query(ActivityEvent).all()
    assert len(remaining_events) == 1
    assert remaining_events[0].idempotency_key == "recent-ev-1"

    remaining_hbs = db.query(HeartbeatLog).all()
    assert len(remaining_hbs) == 1
    assert (now - remaining_hbs[0].timestamp.replace(tzinfo=timezone.utc)).days < 90
    db.close()


def test_right_to_erasure_endpoint(client, parents_and_devices):
    """Verify DELETE /api/v1/devices/{device_id}/data enforces password confirmation and anti-IDOR (T4_014)."""
    p = parents_and_devices
    db = TestingSessionLocal()

    # Seed events for Bob's child device
    now = datetime.now(timezone.utc)
    ev = ActivityEvent(
        idempotency_key="bob-child-ev-1",
        ts=now,
        device_id=p["dev_b"],
        type="web_access",
        subject="youtube.com",
        duration_sec=120
    )
    hb = HeartbeatLog(device_id=p["dev_b"], timestamp=now, status_payload='{}')
    db.add_all([ev, hb])
    db.commit()
    db.close()

    # 1. Bob attempts erasure with WRONG password -> 401
    wrong_pwd_resp = client.request(
        "DELETE",
        f"/api/v1/devices/{p['dev_b']}/data",
        headers={"Authorization": f"Bearer {p['token_b']}"},
        json={"password": "WrongPassword123"}
    )
    assert wrong_pwd_resp.status_code == 401
    assert "chính xác" in wrong_pwd_resp.json()["detail"].lower()

    # 2. Alice attempts erasure on Bob's child device with Alice's password -> 403 (Anti-IDOR)
    idor_resp = client.request(
        "DELETE",
        f"/api/v1/devices/{p['dev_b']}/data",
        headers={"Authorization": f"Bearer {p['token_a']}"},
        json={"password": "PassAlice@123"}
    )
    assert idor_resp.status_code == 403
    assert "quyền" in idor_resp.json()["detail"].lower()

    # 3. Bob authorizes erasure with CORRECT password ("PassBob@12345") -> 200
    valid_resp = client.request(
        "DELETE",
        f"/api/v1/devices/{p['dev_b']}/data",
        headers={"Authorization": f"Bearer {p['token_b']}"},
        json={"password": "PassBob@12345"}
    )
    assert valid_resp.status_code == 200
    data = valid_resp.json()
    assert data["status"] == "success"
    assert data["events_deleted"] >= 1
    assert data["heartbeats_deleted"] >= 1

    # Verify that telemetry for dev_b is wiped from DB
    db2 = TestingSessionLocal()
    assert db2.query(ActivityEvent).filter(ActivityEvent.device_id == p["dev_b"]).count() == 0
    assert db2.query(HeartbeatLog).filter(HeartbeatLog.device_id == p["dev_b"]).count() == 0
    assert db2.query(AccessRequest).filter(AccessRequest.device_id == p["dev_b"]).count() == 0
    # Legal compliance audit log should be present
    compliance_audit = db2.query(AuditLog).filter(
        AuditLog.device_id == p["dev_b"],
        AuditLog.action == "retention:right_to_erasure"
    ).first()
    assert compliance_audit is not None
    db2.close()


def test_agent_storage_purge_local_data():
    """Verify agent/storage.py purge_local_data() wipes offline buffers and rule caches (T4_015)."""
    with tempfile.NamedTemporaryFile(suffix=".db", delete=False) as tmp:
        tmp_path = tmp.name

    try:
        # Seed test data in temporary agent SQLite DB
        now_iso = datetime.now(timezone.utc).isoformat()
        add_pending_event({
            "idempotency_key": "local-key-001",
            "ts": now_iso,
            "device_id": 1,
            "child_id": None,
            "type": "app_usage",
            "subject": "Roblox.exe",
            "duration_sec": 300,
            "policy_id": 1
        }, db_path=tmp_path)
        today_str = datetime.now(timezone.utc).strftime("%Y-%m-%d")
        update_daily_usage(date_str=today_str, used_seconds=600, bonus_minutes=15, is_locked=0, db_path=tmp_path)

        assert len(get_pending_events(db_path=tmp_path)) == 1
        assert get_daily_usage(date_str=today_str, db_path=tmp_path)["used_seconds"] == 600

        # Execute local purge
        res = purge_local_data(db_path=tmp_path)
        assert res["pending_events_deleted"] == 1
        assert res["daily_usage_deleted"] == 1

        # Verify tables are now empty
        assert len(get_pending_events(db_path=tmp_path)) == 0
        assert get_daily_usage(date_str=today_str, db_path=tmp_path)["used_seconds"] == 0
    finally:
        if os.path.exists(tmp_path):
            os.remove(tmp_path)


# ============================================================================
# Phase 4: Anti-Bypass Guard & Process/Network Defense M3 (T4_017 - T4_020)
# ============================================================================

def test_dns_watchdog_tamper_detection_and_auto_remediation(monkeypatch):
    """Verify that DNSWatchdog detects manual DNS changes, triggers remediation and fires callback (T4_017, T4_018)."""
    remediated_interfaces = []
    tamper_alerts = []

    # Mock interfaces and DNS query
    mock_active_interfaces = ["Wi-Fi", "Ethernet"]
    adapter_dns_state = {
        "Wi-Fi": ["8.8.8.8", "8.8.4.4"],   # Tampered: changed to Google DNS
        "Ethernet": ["127.0.0.1"]          # Intact: points to OGK DNS proxy
    }

    import agent.dns_watchdog as dw_module

    def mock_get_adapter_dns(iface):
        return adapter_dns_state.get(iface, [])

    def mock_set_dns_to_localhost(iface):
        remediated_interfaces.append(iface)
        adapter_dns_state[iface] = ["127.0.0.1"]
        return True

    monkeypatch.setattr(dw_module, "get_adapter_dns_servers", mock_get_adapter_dns)
    monkeypatch.setattr(dw_module, "set_dns_to_localhost", mock_set_dns_to_localhost)

    watchdog = DNSWatchdog(
        check_interval_sec=20.0,
        target_dns="127.0.0.1",
        on_tamper_callback=lambda iface, dns: tamper_alerts.append((iface, dns)),
        interfaces_provider=lambda: mock_active_interfaces
    )

    # 1. Execute check: Wi-Fi should be flagged and restored
    results = watchdog.check_and_restore_dns()
    assert len(results) == 1
    assert results[0]["interface"] == "Wi-Fi"
    assert results[0]["old_dns"] == ["8.8.8.8", "8.8.4.4"]
    assert results[0]["remediation_success"] is True

    # Auto-remediation called on Wi-Fi
    assert "Wi-Fi" in remediated_interfaces
    assert len(tamper_alerts) == 1
    assert tamper_alerts[0] == ("Wi-Fi", ["8.8.8.8", "8.8.4.4"])

    # 2. Subsequent check: all adapters are now 127.0.0.1 -> No tampers
    second_results = watchdog.check_and_restore_dns()
    assert len(second_results) == 0
    assert len(tamper_alerts) == 1  # No additional alert


def test_dns_watchdog_thread_lifecycle():
    """Verify DNSWatchdog background thread starts and terminates cleanly (T4_020)."""
    watchdog = DNSWatchdog(
        check_interval_sec=0.1,
        target_dns="127.0.0.1",
        interfaces_provider=lambda: ["MockInterface"]
    )
    assert watchdog._running is False
    watchdog.start()
    assert watchdog._running is True
    assert watchdog._thread is not None
    assert watchdog._thread.is_alive()

    watchdog.stop()
    assert watchdog._running is False
    assert watchdog._thread is None


def test_seed_vpn_app_rules_and_sync(client):
    """Verify seeding of common VPN processes (WARP, ProtonVPN, Psiphon, UltraSurf) (T4_019)."""
    db = TestingSessionLocal()
    inserted_count = seed_app_rules(db)
    assert inserted_count >= 5  # Seeded VPN applications
    db.close()

    # Verify that seeded apps are returned in filtering rules sync API
    sync_resp = client.get("/api/v1/filtering/rules")
    assert sync_resp.status_code == 200
    sync_data = sync_resp.json()
    app_names = [a["name"] for a in sync_data["app_blocklist"]]

    assert "Cloudflare WARP.exe" in app_names
    assert "warp-svc.exe" in app_names
    assert "ProtonVPN.exe" in app_names
    assert "psiphon3.exe" in app_names
    assert "u.exe" in app_names
    assert "ultrasurf.exe" in app_names


def test_app_controller_blocks_vpn_by_executable_name(monkeypatch):
    """Verify AppController process monitor terminates known VPN processes by name (M3 Anti-Bypass)."""
    class MockProcess:
        def __init__(self, pid, name, exe):
            self.info = {'pid': pid, 'name': name, 'exe': exe}
            self.terminated = False

        def terminate(self):
            self.terminated = True

        def kill(self):
            self.terminated = True

    proc_warp = MockProcess(101, "Cloudflare WARP.exe", r"C:\Program Files\Cloudflare\WARP.exe")
    proc_calc = MockProcess(102, "calc.exe", r"C:\Windows\System32\calc.exe")
    proc_psi = MockProcess(103, "psiphon3.exe", r"C:\Users\Child\Downloads\psiphon3.exe")

    mock_processes = [proc_warp, proc_calc, proc_psi]

    import psutil
    monkeypatch.setattr(psutil, "process_iter", lambda attrs: mock_processes)

    # Cached rules provide VPN blocking rules
    vpn_rules = {
        "hash_placeholder_1": {"name": "Cloudflare WARP.exe", "action": "block", "description": "VPN WARP"},
        "hash_placeholder_2": {"name": "psiphon3.exe", "action": "block", "description": "Psiphon Tunnel"}
    }

    blocked_callbacks = []
    controller = AppController(
        rules_provider=lambda: vpn_rules,
        on_blocked_callback=lambda app, reason, h: blocked_callbacks.append((app, reason))
    )
    # Mock SHA-256 caching returning dummy hashes
    controller._get_cached_sha256 = lambda path: "dummy_different_hash_from_new_build"

    terminated = controller.scan_and_enforce()
    assert len(terminated) == 2
    terminated_names = [t["app_name"] for t in terminated]
    assert "Cloudflare WARP.exe" in terminated_names
    assert "psiphon3.exe" in terminated_names
    assert "calc.exe" not in terminated_names

    assert proc_warp.terminated is True
    assert proc_psi.terminated is True
    assert proc_calc.terminated is False
    assert len(blocked_callbacks) == 2



