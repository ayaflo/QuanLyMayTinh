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
    from agent.config import APP_TITLE, APP_VERSION, SERVER_URL, DEVICE_NAME, REQUEST_TIMEOUT
    from agent.fingerprint import get_device_fingerprint
    from agent.storage import load_credentials, clear_credentials
    from agent.enrollment_client import pair_with_server
    from agent.heartbeat_client import start_heartbeat_thread
    from agent.tray import init_tray_icon, show_startup_notification, show_tray_notification
    from agent.screen_time_tracker import ScreenTimeTracker
    from agent.system_locker import SystemLocker
    from agent.policy_syncer import sync_policy_from_server
    from agent.ws_listener import WebSocketListener
    from agent.dns_proxy import DNSProxyServer
    from agent.dns_configurator import set_dns_to_localhost, restore_dns_to_dhcp
    from agent.dns_watchdog import DNSWatchdog
    from agent.app_controller import AppController
    from agent.event_collector import EventCollector
    from agent.storage import (
        save_dns_rules_cache,
        load_dns_rules_cache,
        save_app_rules_cache,
        load_app_rules_cache,
        purge_local_data
    )
except ImportError:
    from config import APP_TITLE, APP_VERSION, SERVER_URL, DEVICE_NAME, REQUEST_TIMEOUT
    from fingerprint import get_device_fingerprint
    from storage import (
        load_credentials,
        clear_credentials,
        save_dns_rules_cache,
        load_dns_rules_cache,
        save_app_rules_cache,
        load_app_rules_cache,
        purge_local_data
    )
    from enrollment_client import pair_with_server
    from heartbeat_client import start_heartbeat_thread
    from tray import init_tray_icon, show_startup_notification, show_tray_notification
    from screen_time_tracker import ScreenTimeTracker
    from system_locker import SystemLocker
    from policy_syncer import sync_policy_from_server
    from ws_listener import WebSocketListener
    from dns_proxy import DNSProxyServer
    from dns_configurator import set_dns_to_localhost, restore_dns_to_dhcp
    from dns_watchdog import DNSWatchdog
    from app_controller import AppController
    from event_collector import EventCollector



def print_banner():
    """Print standard ethical banner on startup."""
    print("=" * 65)
    print(f"  {APP_TITLE} — Phiên bản {APP_VERSION}")
    print("  Triết lý: Đồng hành, không theo dõi lén (Luật Trẻ Em 2016)")
    print("=" * 65)


def prompt_enrollment_cli(server_url: str = SERVER_URL) -> bool:
    """Guide child or parent through pairing device via CLI input."""
    fingerprint = get_device_fingerprint()
    print("\n [!] Máy tính này chưa được ghép đôi với tài khoản phụ huynh.")
    print(f"     Mã nhận diện máy (Fingerprint): {fingerprint}")
    print(f"     Máy chủ kết nối: {server_url}\n")
    print(f" Vui lòng đăng nhập vào Web Dashboard phụ huynh ({server_url}/devices),")
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


def prompt_enrollment(server_url: str = SERVER_URL, use_gui: bool = True) -> bool:
    """Guide child or parent through pairing device to parent account via GUI (or CLI fallback)."""
    if use_gui:
        try:
            try:
                from agent.pairing_gui import prompt_pairing_gui
            except ImportError:
                from pairing_gui import prompt_pairing_gui

            print("\n [*] Đang mở giao diện kết nối thân thiện cho trẻ và phụ huynh...")
            success = prompt_pairing_gui(server_url=server_url, default_device_name=DEVICE_NAME)
            if success:
                return True
            print(" [i] Đã đóng giao diện ghép đôi. Chuyển sang chế độ dòng lệnh...")
        except Exception as e:
            print(f" [!] Không thể khởi động giao diện đồ họa ({e}), chuyển sang dòng lệnh...")

    return prompt_enrollment_cli(server_url=server_url)


def main():
    parser = argparse.ArgumentParser(description=f"{APP_TITLE} Client Agent")
    parser.add_argument("--pair-code", type=str, help="Auto-pair using provided 8-char code")
    parser.add_argument("--re-pair", action="store_true", help="Xóa thông tin cũ và ghép đôi lại với máy chủ mới")
    parser.add_argument("--headless", action="store_true", help="Run without system tray GUI")
    parser.add_argument("--cli", action="store_true", help="Sử dụng chế độ dòng lệnh (CLI) thay vì giao diện đồ họa")
    args = parser.parse_args()

    print_banner()

    # Step 1: Check existing credentials
    if args.re_pair:
        print(" [*] Đang xóa thông tin ghép đôi cũ theo tham số --re-pair...")
        clear_credentials()
        creds = None
    else:
        creds = load_credentials()

    # Verify if old credentials belong to current server or need re-enrollment
    if creds and not args.pair_code:
        import requests
        try:
            test_resp = requests.get(
                f"{SERVER_URL}/api/v1/policy",
                headers={"Authorization": f"Bearer {creds['access_token']}"},
                timeout=min(REQUEST_TIMEOUT, 10)
            )
            if test_resp.status_code == 401:
                print(f"\n [!] Máy chủ tại {SERVER_URL} từ chối thông tin ghép đôi cũ (HTTP 401).")
                print("     (Tự động chuyển sang chế độ ghép đôi mới với máy chủ)...")
                clear_credentials()
                creds = None
        except Exception:
            pass

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
            use_gui = not (args.headless or args.cli)
            enrolled = prompt_enrollment(use_gui=use_gui)
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
        elif action == "purge_local_data":
            print(" [!] Nhận lệnh từ phụ huynh: Xóa toàn bộ dữ liệu máy tính (Nghị định 13/2023)...")
            purge_local_data()
            if tray_icon_holder[0]:
                show_tray_notification(
                    tray_icon_holder[0],
                    "Quyền Riêng Tư (NĐ 13/2023)",
                    "Dữ liệu lịch sử máy tính đã được xóa trắng theo yêu cầu của cha mẹ."
                )

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

    def handle_dns_tamper(interface_name: str, old_dns: list[str]):
        old_dns_str = ", ".join(old_dns) if old_dns else "dhcp_or_none"
        print(f"\n [!] PHÁT HIỆN CAN THIỆP DNS (M3) TRÊN CARD '{interface_name}': {old_dns_str} -> Đã tự động khôi phục 127.0.0.1")
        event_collector.record_event(
            event_type="tamper_attempt",
            subject=f"dns_adapter:{interface_name}"
        )
        if tray_icon_holder[0]:
            show_tray_notification(
                tray_icon_holder[0],
                "Cảnh Báo Vượt Rào Mạng (M3)",
                f"Phát hiện DNS card mạng '{interface_name}' bị can thiệp. Đã tự động khôi phục về 127.0.0.1."
            )

    dns_watchdog = DNSWatchdog(
        check_interval_sec=20.0,
        target_dns="127.0.0.1",
        on_tamper_callback=handle_dns_tamper
    )

    def handle_app_blocked(app_name: str, reason: str, file_hash: str):
        event_collector.record_event(event_type="blocked_app", subject=app_name)
        if tray_icon_holder[0]:
            show_tray_notification(
                tray_icon_holder[0],
                "Ứng Dụng Bị Khóa (NT4)",
                f"'{app_name}' đã bị khóa theo quy định: {reason}"
            )

    def handle_app_usage(app_name: str, duration_sec: int):
        event_collector.record_event(event_type="app_usage", subject=app_name, duration_sec=duration_sec)

    app_controller = AppController(
        rules_provider=load_app_rules_cache,
        on_blocked_callback=handle_app_blocked,
        on_usage_callback=handle_app_usage
    )

    def sync_filtering_rules():
        import requests
        try:
            token = creds.get('access_token')
            headers = {"Authorization": f"Bearer {token}"} if token else {}
            res = requests.get(f"{SERVER_URL}/api/v1/filtering/rules", headers=headers, timeout=REQUEST_TIMEOUT)
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
        dns_configured = set_dns_to_localhost()
        dns_watchdog.start()
        if dns_configured:
            print(" [✓] Đã cấu hình card mạng Windows trỏ DNS về 127.0.0.1 (F2 & M3).")
        else:
            print(" [!] Khuyến nghị chạy quyền Administrator để tự động đổi DNS card mạng (hoặc trỏ thủ công 127.0.0.1).")
    except Exception as e:
        print(f" [!] Không thể mở cổng DNS 53 (cần quyền Admin Windows hoặc cổng đang bận): {e}")

    def on_exit():
        stop_event.set()
        dns_watchdog.stop()
        tracker.stop()
        system_locker.stop_enforcement()
        ws_listener.stop()
        app_controller.stop()
        dns_proxy.stop()
        restore_dns_to_dhcp()
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
