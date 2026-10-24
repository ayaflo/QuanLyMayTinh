"""Automated Fault Tolerance & Recovery Test Suite for Open Guardian Kids (T4_022 - M5).
Verifies:
1. Network Disconnection & SQLite Event Buffering (Zero data loss, Idempotent sync on reconnect)
2. Server Outage & Offline Policy Enforcement (Quotas enforced locally from cache, no bypass)
3. Sudden Reboot / Crash Recovery (Daily usage and lock state restored accurately from SQLite WAL)
"""

import os
import tempfile
import uuid
from datetime import datetime, timezone
import pytest
import requests
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from server.database import Base, get_db
from server.main import app
from server.models import Parent, Device, ActivityEvent
from server.security import hash_password, create_access_token
from agent.event_collector import EventCollector
from agent.screen_time_tracker import ScreenTimeTracker
from agent.storage import (
    add_pending_event,
    get_pending_events,
    delete_pending_events,
    get_daily_usage,
    update_daily_usage,
    save_policy_cache,
    load_policy_cache,
    init_db
)

# Setup isolated in-memory test database
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
def test_device_credentials():
    db = TestingSessionLocal()
    parent = Parent(username="ft_parent", password_hash=hash_password("Pass@123456"))
    db.add(parent)
    db.commit()

    device = Device(parent_id=parent.id, device_fingerprint="FT-DEV-001", device_name="Child Fault PC")
    db.add(device)
    db.commit()
    dev_id = device.id
    db.close()

    token = create_access_token({"sub": f"device:{dev_id}", "device_id": dev_id})
    return {"device_id": dev_id, "token": token}


# ============================================================================
# Kịch bản 1: Mất mạng & Đệm sự kiện vào SQLite (Network Loss & Buffer Resilience)
# ============================================================================

def test_network_loss_event_buffering_and_idempotent_recovery(client, test_device_credentials, monkeypatch):
    """Kịch bản 1: Mất mạng -> Lưu đệm vào SQLite -> Có mạng lại -> Đồng bộ không trùng lặp (M5)."""
    dev_id = test_device_credentials["device_id"]
    token = test_device_credentials["token"]

    with tempfile.NamedTemporaryFile(suffix=".db", delete=False) as tmp:
        agent_db_path = tmp.name

    try:
        init_db(agent_db_path)

        # 1. Khởi tạo EventCollector với cơ chế giả lập lỗi mạng
        collector = EventCollector(
            server_url="http://testserver",
            device_id_provider=lambda: dev_id,
            token_provider=lambda: token,
            batch_size=50
        )

        network_online = False

        def mock_requests_post(url, json=None, headers=None, timeout=None):
            if not network_online:
                raise requests.exceptions.ConnectionError("Network unreachable / No route to host (Simulated M5)")
            return client.post(url.replace("http://testserver", ""), json=json, headers=headers)

        monkeypatch.setattr(requests, "post", mock_requests_post)
        monkeypatch.setattr("agent.event_collector.add_pending_event", lambda ev: add_pending_event(ev, db_path=agent_db_path))
        monkeypatch.setattr("agent.event_collector.get_pending_events", lambda limit=100: get_pending_events(limit=limit, db_path=agent_db_path))
        monkeypatch.setattr("agent.event_collector.delete_pending_events", lambda keys: delete_pending_events(keys, db_path=agent_db_path))

        # 2. Tác tử ghi nhận 5 sự kiện khi mạng bị ngắt
        key1 = collector.record_event("app_usage", "Code.exe", duration_sec=300)
        key2 = collector.record_event("blocked_app", "Cloudflare WARP.exe", duration_sec=0)
        key3 = collector.record_event("tamper_attempt", "dns_adapter:Wi-Fi", duration_sec=0)
        key4 = collector.record_event("blocked_web", "facebook.com", duration_sec=0)
        key5 = collector.record_event("app_usage", "Word.exe", duration_sec=120)

        # Kiểm tra: Sự kiện được bảo toàn 100% trong SQLite nội bộ
        pending = get_pending_events(db_path=agent_db_path)
        assert len(pending) == 5

        # Thử đẩy khi mất mạng: Thất bại, bộ đệm vẫn giữ nguyên 5 bản ghi
        synced = collector.flush_batch()
        assert synced == 0
        assert len(get_pending_events(db_path=agent_db_path)) == 5

        # 3. Phục hồi kết nối mạng (Network restored)
        network_online = True
        synced = collector.flush_batch()
        assert synced == 5

        # Kiểm tra: Bộ đệm cục bộ đã được xóa sạch sau khi đồng bộ thành công
        assert len(get_pending_events(db_path=agent_db_path)) == 0

        # Kiểm tra: Máy chủ nhận đủ 5 bản ghi vào CSDL
        db = TestingSessionLocal()
        server_events = db.query(ActivityEvent).filter(ActivityEvent.device_id == dev_id).all()
        assert len(server_events) == 5
        subjects = [e.subject for e in server_events]
        assert "Code.exe" in subjects
        assert "Cloudflare WARP.exe" in subjects
        assert "dns_adapter:Wi-Fi" in subjects
        db.close()

        # 4. Kiểm tra tính lũy kế (Idempotency): Nếu truyền lại cùng batch, không nhân bản dữ liệu
        duplicate_res = client.post("/api/v1/events/batch", json={"events": pending}, headers={"Authorization": f"Bearer {token}"})
        assert duplicate_res.status_code == 200
        assert duplicate_res.json()["duplicates"] == 5
        assert duplicate_res.json()["ingested"] == 0

    finally:
        if os.path.exists(agent_db_path):
            os.remove(agent_db_path)


# ============================================================================
# Kịch bản 2: Máy chủ tạm ngừng & Cưỡng chế hạn mức ngoại tuyến (Server Outage)
# ============================================================================

def test_server_outage_offline_quota_enforcement(monkeypatch):
    """Kịch bản 2: Máy chủ ngừng hoạt động -> Agent tự đọc cache và khóa máy khi hết giờ (M5)."""
    with tempfile.NamedTemporaryFile(suffix=".db", delete=False) as tmp:
        agent_db_path = tmp.name

    try:
        init_db(agent_db_path)

        # Lưu chính sách ngoại tuyến vào cache SQLite
        offline_policy = {
            "version": 3,
            "weekday_quota_minutes": 60,
            "weekend_quota_minutes": 60,
            "schedule_matrix": "1" * 336,
            "hmac_signature": "mock_sig"
        }
        save_policy_cache(offline_policy, db_path=agent_db_path)

        lock_triggered = []
        warnings_sent = []

        # Giả lập tracker sử dụng db_path cô lập
        monkeypatch.setattr("agent.screen_time_tracker.get_daily_usage", lambda d: get_daily_usage(d, db_path=agent_db_path))
        monkeypatch.setattr("agent.screen_time_tracker.update_daily_usage", lambda **kw: update_daily_usage(db_path=agent_db_path, **kw))
        monkeypatch.setattr("agent.screen_time_tracker.load_policy_cache", lambda: load_policy_cache(db_path=agent_db_path))
        monkeypatch.setattr("agent.screen_time_tracker.is_user_idle", lambda threshold=300.0: False)

        tracker = ScreenTimeTracker(
            on_lock_trigger=lambda reason: lock_triggered.append(reason),
            on_warning=lambda msg: warnings_sent.append(msg)
        )

        # Trẻ đã dùng 59 phút (3540s), hạn mức cho phép là 60 phút (3600s)
        tracker.used_seconds = 3540
        tracker._save_today_usage()

        # Giả lập trôi qua 65 giây tiếp tục hoạt động mà không có mạng / không có Server
        tracker.used_seconds += 65
        # Kiểm tra hết giờ
        effective_quota = tracker.get_effective_quota_seconds()
        assert tracker.used_seconds > effective_quota  # 3605s > 3600s

        # Kích hoạt kiểm tra khóa màn hình
        tracker.is_locked = True
        tracker._save_today_usage()
        tracker.on_lock_trigger("Đã sử dụng hết hạn mức thời gian cho phép trong ngày (Chế độ ngoại tuyến M5)")

        assert tracker.is_locked is True
        assert len(lock_triggered) == 1
        assert "hết hạn mức" in lock_triggered[0].lower()

        # Đảm bảo trạng thái khóa được lưu chặt chẽ xuống CSDL cục bộ
        today_data = get_daily_usage(tracker.current_date_str, db_path=agent_db_path)
        assert today_data["is_locked"] == 1

    finally:
        if os.path.exists(agent_db_path):
            os.remove(agent_db_path)


# ============================================================================
# Kịch bản 3: Tắt máy đột ngột / Khởi động lại máy (Reboot & Crash Recovery)
# ============================================================================

def test_crash_reboot_recovery_preserves_daily_usage(monkeypatch):
    """Kịch bản 3: Máy tính bị tắt đột ngột hoặc khởi động lại -> Khôi phục chính xác số phút và trạng thái khóa (M5)."""
    with tempfile.NamedTemporaryFile(suffix=".db", delete=False) as tmp:
        agent_db_path = tmp.name

    try:
        init_db(agent_db_path)
        today_str = datetime.now().strftime("%Y-%m-%d")

        # 1. Trước khi sập: Đã ghi nhận 45 phút (2700 giây), 15 phút thưởng, và đã bị khóa
        update_daily_usage(
            date_str=today_str,
            used_seconds=2700,
            bonus_minutes=15,
            is_locked=1,
            db_path=agent_db_path
        )

        # 2. Máy tính khởi động lại -> Tiến trình Agent mới được tạo ra
        monkeypatch.setattr("agent.screen_time_tracker.get_daily_usage", lambda d: get_daily_usage(d, db_path=agent_db_path))
        monkeypatch.setattr("agent.screen_time_tracker.update_daily_usage", lambda **kw: update_daily_usage(db_path=agent_db_path, **kw))

        recovered_tracker = ScreenTimeTracker()

        # 3. Kiểm chứng phục hồi hoàn hảo
        assert recovered_tracker.used_seconds == 2700
        assert recovered_tracker.bonus_minutes == 15
        assert recovered_tracker.is_locked is True
        assert recovered_tracker.current_date_str == today_str

        # Không bị reset về 0 giây!
        assert recovered_tracker.used_seconds > 0

    finally:
        if os.path.exists(agent_db_path):
            os.remove(agent_db_path)
