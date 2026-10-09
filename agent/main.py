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
    from agent.tray import init_tray_icon, show_startup_notification
except ImportError:
    from config import APP_TITLE, APP_VERSION, SERVER_URL, DEVICE_NAME
    from fingerprint import get_device_fingerprint
    from storage import load_credentials
    from enrollment_client import pair_with_server
    from heartbeat_client import start_heartbeat_thread
    from tray import init_tray_icon, show_startup_notification


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

    # Step 2: Start Heartbeat telemetry thread (every 60 seconds)
    hb_thread, stop_event = start_heartbeat_thread()

    def on_exit():
        stop_event.set()

    # Step 3: Run tray icon or wait loop
    if args.headless:
        print(" [*] Chế độ Headless: Nhịp tim đang chạy nền. Nhấn Ctrl+C để thoát.")
        try:
            while not stop_event.is_set():
                stop_event.wait(1)
        except KeyboardInterrupt:
            print("\n [x] Dừng Agent.")
            stop_event.set()
    else:
        print(" [*] Khởi động biểu tượng khay hệ thống (System Tray Icon)...")
        tray_icon = init_tray_icon(on_exit_callback=on_exit)

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
            stop_event.set()

    print(" [*] Tác tử Open Guardian Kids đã kết thúc.")


if __name__ == "__main__":
    main()
