"""Main entry point for the Open Guardian Kids (OGK) Client Agent.
Manages enrollment workflow, launches heartbeat background worker, and system tray icon.
"""

import os
import sys
import argparse

# Ensure project root is in sys.path
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

try:
    from agent.config import APP_TITLE, APP_VERSION, SERVER_URL, DEVICE_NAME
    from agent.fingerprint import get_device_fingerprint
    from agent.storage import load_credentials
    from agent.enrollment_client import pair_with_server
    from agent.heartbeat_client import start_heartbeat_thread
    from agent.tray import init_tray_icon, show_startup_notification, show_tray_notification
    from agent.screen_time_tracker import ScreenTimeTracker
    from agent.system_locker import SystemLocker
    from agent.policy_syncer import sync_policy_from_server
    from agent.ws_listener import WebSocketListener
    from agent.dns_proxy import DNSProxyServer
    from agent.app_controller import AppController
    from agent.event_collector import EventCollector
    from agent.storage import save_dns_rules_cache, load_dns_rules_cache, save_app_rules_cache, load_app_rules_cache
except ImportError:
    from config import APP_TITLE, APP_VERSION, SERVER_URL, DEVICE_NAME
    from fingerprint import get_device_fingerprint
    from storage import load_credentials, save_dns_rules_cache, load_dns_rules_cache, save_app_rules_cache, load_app_rules_cache
    from enrollment_client import pair_with_server
    from heartbeat_client import start_heartbeat_thread
    from tray import init_tray_icon, show_startup_notification, show_tray_notification
    from screen_time_tracker import ScreenTimeTracker
    from system_locker import SystemLocker
    from policy_syncer import sync_policy_from_server
    from ws_listener import WebSocketListener
    from dns_proxy import DNSProxyServer
    from app_controller import AppController
    from event_collector import EventCollector



def print_banner():
    """Print standard ethical banner on startup."""
    print("=" * 65)
    print(f"  {APP_TITLE} — Phiên bản {APP_VERSION}")
    print("  Triết lý: Đồng hành, không theo dõi lén (Luật Trẻ Em 2016)")
    print("=" * 65)


def prompt_enrollment(server_url: str = SERVER_URL) -> bool:
    """Guide child or parent through pairing device to parent account."""
    fingerprint = get_device_fingerprint()
    print("\n [!] Máy tính này chưa được ghép đôi với tài khoản phụ huynh.")
    print(f"     Mã nhận diện máy (Fingerprint): {fingerprint}")
    print(f"     Máy chủ kết nối: {server_url}\n")
    print(" Vui lòng đăng nhập vào Web Dashboard phụ huynh (http://127.0.0.1:8000/devices),")
    print(" nhấn '+ Thêm Thiết Bị Mới' và lấy mã ghép đôi 8 ký tự.")

    while True:
        try:
            code = input("\n Nhập mã ghép đôi 8 ký tự (hoặc gõ 'q' để thoát): ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\n [x] Hủy bỏ ghép đôi.")
            return False

        if code.lower() in ("q", "quit", "exit"):
            return False

        if len(code) != 8:
            print(" [x] Lỗi: Mã ghép đôi phải gồm chính xác 8 ký tự. Vui lòng thử lại.")
            continue

        print(f" [*] Đang gửi yêu cầu ghép đôi mã '{code.upper()}' lên máy chủ...")
        success, msg, _ = pair_with_server(code, device_name=DEVICE_NAME, server_url=server_url)

        if success:
            print(f" [✓] {msg}")
            return True
        else:
            print(f" [x] Thất bại: {msg}")
            print(" Vui lòng kiểm tra lại mã trên Dashboard hoặc tạo mã mới nếu mã cũ đã hết hạn.")


def main():
    parser = argparse.ArgumentParser(description=f"{APP_TITLE} Client Agent")
    parser.add_argument("--pair-code", type=str, help="Auto-pair using provided 8-char code")
    parser.add_argument("--headless", action="store_true", help="Run without system tray GUI")
    args = parser.parse_args()

    print_banner()

    # Step 1: Check existing credentials
    creds = load_credentials()

    if not creds:
        # If auto-pair code passed via argument
        if args.pair_code:
            print(f" [*] Tự động ghép đôi với mã tham số: {args.pair_code}")
            success, msg, _ = pair_with_server(args.pair_code, device_name=DEVICE_NAME)
            if not success:
                print(f" [x] Lỗi ghép đôi: {msg}")
                sys.exit(1)
            creds = load_credentials()
        else:
            enrolled = prompt_enrollment()
            if not enrolled:
                print(" [x] Chưa ghép đôi. Tác tử tạm dừng.")
                sys.exit(0)
            creds = load_credentials()

    print(f"\n [✓] Đã xác thực thiết bị ID: #{creds['device_id']} ({creds.get('device_name', DEVICE_NAME)})")

    # Step 2: Sync initial policy from server (F4)
    sync_policy_from_server()

    # Step 3: Initialize Locker & Time Tracker (F1)
    tray_icon_holder = [None]  # Mutable box for tray icon reference

    def handle_lock_trigger(reason: str):
        print(f"\n [!] CƯỠNG CHẾ KHÓA MÁY: {reason}")
        system_locker.lock_now(reason)
        if tray_icon_holder[0]:
            show_tray_notification(tray_icon_holder[0], "Khóa Màn Hình", reason)

    def handle_warning(msg: str):
        print(f"\n [i] CẢNH BÁO THỜI GIAN: {msg}")
        if tray_icon_holder[0]:
            show_tray_notification(tray_icon_holder[0], "Thời Gian Sử Dụng", msg)

    tracker = ScreenTimeTracker(
        on_lock_trigger=handle_lock_trigger,
        on_warning=handle_warning
    )
    system_locker = SystemLocker(is_lock_required_fn=lambda: tracker.is_locked)

    # Step 4: Initialize WebSocket Emergency Command Listener (< 5s)
    def handle_ws_command(action: str, payload: dict):
        if action == "lock_now":
            tracker.is_locked = True
            system_locker.lock_now("Khóa máy khẩn cấp từ phụ huynh")
            if tray_icon_holder[0]:
                show_tray_notification(tray_icon_holder[0], "Lệnh Khẩn Cấp", "Phụ huynh đã khóa màn hình máy tính!")
        elif action == "unlock":
            tracker.is_locked = False
            tracker.grace_period_active = False
            if tray_icon_holder[0]:
                show_tray_notification(tray_icon_holder[0], "Lệnh Khẩn Cấp", "Phụ huynh đã mở khóa màn hình cho em.")
        elif action == "add_time":
            mins = payload.get("minutes", 15)
            tracker.add_bonus_minutes(mins)
            if tray_icon_holder[0]:
                show_tray_notification(tray_icon_holder[0], "Thưởng Thời Gian", f"Phụ huynh đã cộng thêm {mins} phút sử dụng!")
        elif action == "policy_updated":
            sync_policy_from_server()
            sync_filtering_rules()

    ws_listener = WebSocketListener(on_command=handle_ws_command)

    # Step 5: Week 3 (Version 0.3) Workers: EventCollector, DNS Proxy, AppController
    event_collector = EventCollector(
        server_url=SERVER_URL,
        device_id_provider=lambda: creds['device_id'] if creds else 1,
        token_provider=lambda: creds['access_token'] if creds else None
    )

    def handle_dns_event(event_type: str, domain: str):
        event_collector.record_event(event_type=event_type, subject=domain)

    dns_proxy = DNSProxyServer(
        host="127.0.0.1",
        port=53,
        on_event_callback=handle_dns_event
    )

    def handle_app_blocked(app_name: str, reason: str, file_hash: str):
        event_collector.record_event(event_type="blocked_app", subject=app_name)
        if tray_icon_holder[0]:
            show_tray_notification(
                tray_icon_holder[0],
                "Ứng Dụng Bị Khóa (NT4)",
                f"'{app_name}' đã bị khóa theo quy định: {reason}"
            )

    app_controller = AppController(
        rules_provider=load_app_rules_cache,
        on_blocked_callback=handle_app_blocked
    )

    def sync_filtering_rules():
        import requests
        try:
            token = creds.get('access_token')
            headers = {"Authorization": f"Bearer {token}"} if token else {}
            res = requests.get(f"{SERVER_URL}/api/v1/filtering/rules", headers=headers, timeout=5.0)
            if res.status_code == 200:
                data = res.json()
                blocked = set(data.get("blocked_domains", []))
                whitelist = set(data.get("permanent_whitelist", []))
                dns_proxy.update_rules(blocked=blocked, whitelist=whitelist)
                app_rules = [{"sha256": a["sha256"], "name": a["name"], "action": "block", "description": a.get("description", "")} for a in data.get("app_blocklist", [])]
                save_app_rules_cache(app_rules)
                save_dns_rules_cache([{"domain": d, "action": "block"} for d in blocked] + [{"domain": d, "action": "allow", "is_permanent_whitelist": True} for d in whitelist])
                print(f" [✓] Đã đồng bộ {len(blocked)} tên miền & {len(app_rules)} khóa app.")
        except Exception as e:
            print(f" [!] Dùng bộ quy tắc lọc ngoại tuyến: {e}")
            cached_dns = load_dns_rules_cache()
            dns_proxy.update_rules(blocked=cached_dns.get("blocked_domains", set()), whitelist=cached_dns.get("permanent_whitelist", set()))

    sync_filtering_rules()

    # Step 6: Start all background workers
    hb_thread, stop_event = start_heartbeat_thread()
    tracker.start()
    system_locker.start_enforcement()
    ws_listener.start()
    event_collector.start()
    app_controller.start()
    try:
        dns_proxy.start()
    except Exception as e:
        print(f" [!] Không thể mở cổng DNS 53 (cần quyền Admin Windows hoặc cổng đang bận): {e}")

    def on_exit():
        stop_event.set()
        tracker.stop()
        system_locker.stop_enforcement()
        ws_listener.stop()
        app_controller.stop()
        dns_proxy.stop()
        event_collector.stop()

    # Step 6: Run tray icon or headless wait loop
    if args.headless:
        print(" [*] Chế độ Headless: Nhịp tim, bộ đếm giờ và WebSocket đang chạy nền. Nhấn Ctrl+C để thoát.")
        try:
            while not stop_event.is_set():
                stop_event.wait(1)
        except KeyboardInterrupt:
            print("\n [x] Dừng Agent.")
            on_exit()
    else:
        print(" [*] Khởi động biểu tượng khay hệ thống (System Tray Icon)...")
        tray_icon = init_tray_icon(
            on_exit_callback=on_exit,
            get_remaining_minutes_fn=tracker.get_remaining_minutes
        )
        tray_icon_holder[0] = tray_icon

        # Principle NT1: Alert child visibly on startup
        def on_tray_setup(icon):
            icon.visible = True
            show_startup_notification(icon)

        try:
            tray_icon.run(setup=on_tray_setup)
        except Exception as e:
            print(f" [!] Gặp sự cố khay hệ thống ({e}). Chuyển sang chờ tín hiệu...")
            try:
                while not stop_event.is_set():
                    stop_event.wait(1)
            except KeyboardInterrupt:
                pass
        finally:
            on_exit()

    print(" [*] Tác tử Open Guardian Kids đã kết thúc an toàn.")


if __name__ == "__main__":
    main()
