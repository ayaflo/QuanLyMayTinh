"""System tray icon and child notification interface.
Complies with Principle NT1 (Child awareness): Always displays visible tray icon,
never runs in hidden or stealth mode, and shows startup notification.
"""

from typing import Optional, Callable
from PIL import Image, ImageDraw
import pystray
from pystray import MenuItem as item, Menu

try:
    from .config import APP_TITLE, DEVICE_NAME
    from .storage import load_credentials
    from .autostart import is_autostart_enabled, enable_autostart, disable_autostart
except ImportError:
    from config import APP_TITLE, DEVICE_NAME
    from storage import load_credentials
    from autostart import is_autostart_enabled, enable_autostart, disable_autostart


def create_shield_icon_image(size: int = 64) -> Image.Image:
    """Generate a high-contrast shield icon image dynamically using Pillow."""
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # Outer shield polygon (Emerald & Cyan theme)
    shield_coords = [
        (size * 0.5, size * 0.08),   # Top center peak
        (size * 0.88, size * 0.22),  # Top right
        (size * 0.82, size * 0.62),  # Mid right curve
        (size * 0.5, size * 0.92),   # Bottom center point
        (size * 0.18, size * 0.62),  # Mid left curve
        (size * 0.12, size * 0.22),  # Top left
    ]

    # Draw shield gradient-like base
    draw.polygon(shield_coords, fill=(14, 165, 233, 255), outline=(16, 185, 129, 255))

    # Inner highlight shield
    inner_coords = [
        (size * 0.5, size * 0.2),
        (size * 0.76, size * 0.3),
        (size * 0.72, size * 0.58),
        (size * 0.5, size * 0.82),
        (size * 0.28, size * 0.58),
        (size * 0.24, size * 0.3),
    ]
    draw.polygon(inner_coords, fill=(16, 185, 129, 255))

    # Center white checkmark / cross emblem
    draw.line([(size * 0.36, size * 0.48), (size * 0.46, size * 0.60), (size * 0.64, size * 0.38)], fill=(255, 255, 255, 255), width=3)

    return img


def show_startup_notification(icon: pystray.Icon) -> None:
    """Display mandatory notification alerting child that OGK is active (NT1).

    NT1: 'Trẻ biết mình đang được hỗ trợ: Tray icon luôn hiển thị rõ ràng khi Agent chạy;
    thông báo bật lên khi Agent khởi động; tuyệt đối không có chế độ chạy ẩn.'
    """
    try:
        icon.notify(
            title="Open Guardian Kids",
            message="Open Guardian Kids đang hoạt động và đồng hành cùng em."
        )
    except Exception as e:
        print(f" [i] Thông báo NT1: Open Guardian Kids đang hoạt động và đồng hành cùng em ({e})")


def open_child_view():
    """Launch Child Transparency & Voice GUI window (NT3 & NT5)."""
    import threading
    try:
        from .child_view import ChildViewWindow
    except ImportError:
        from child_view import ChildViewWindow

    def _run():
        app = ChildViewWindow()
        app.show()

    t = threading.Thread(target=_run, daemon=True, name="OGK_ChildViewWindow")
    t.start()


def on_request_more_time(icon, item):
    """Handler for NT3: Trẻ có tiếng nói - Xin thêm giờ."""
    open_child_view()


def on_transparency_view(icon, item):
    """Handler for NT5: Minh bạch hai chiều - Trẻ được xem báo cáo."""
    open_child_view()


def open_pairing_dialog():
    """Launch friendly Pairing GUI window from tray icon."""
    import threading
    try:
        from .pairing_gui import prompt_pairing_gui
    except ImportError:
        from pairing_gui import prompt_pairing_gui

    def _run():
        prompt_pairing_gui()

    t = threading.Thread(target=_run, daemon=True, name="OGK_PairingDialog")
    t.start()


def show_tray_notification(icon: Optional[pystray.Icon], title: str, message: str) -> None:
    """Show a balloon notification popup on Windows."""
    if icon:
        try:
            icon.notify(title=title, message=message)
            return
        except Exception:
            pass
    print(f" [i] {title}: {message}")


def init_tray_icon(
    on_exit_callback: Optional[Callable] = None,
    get_remaining_minutes_fn: Optional[Callable[[], int]] = None
) -> pystray.Icon:
    """Initialize system tray icon with ethical menu and action handlers.

    Returns:
        pystray.Icon instance ready to be run via .run()
    """
    icon_image = create_shield_icon_image(64)

    def on_exit(icon, item):
        print(" [!] Trẻ bấm Thoát trên khay hệ thống. Tác tử tiếp tục chạy nền bảo vệ và duy trì khởi động cùng Windows.")
        show_tray_notification(
            icon,
            "Open Guardian Kids",
            "Tác tử tiếp tục hoạt động ngầm để quản lý thời gian và an toàn mạng. Chỉ có phụ huynh gỡ bỏ thiết bị mới dừng tác tử."
        )
        # Chỉ thông báo và không hủy tác tử; không gọi on_exit_callback

    def on_check_time(icon, item):
        mins = get_remaining_minutes_fn() if get_remaining_minutes_fn else "Đang đồng bộ..."
        show_tray_notification(
            icon,
            "Thời Gian Sử Dụng",
            f"Thời gian hôm nay còn lại: {mins} phút. Hãy cân đối việc học tập và nghỉ ngơi nhé!"
        )

    creds = load_credentials()
    device_label = creds.get("device_name", DEVICE_NAME) if creds else DEVICE_NAME

    def on_autostart_info(icon, item):
        try:
            enable_autostart()
        except Exception:
            pass
        show_tray_notification(
            icon,
            "Khởi Động Cùng Windows",
            "Open Guardian Kids là phần mềm giám sát mặc định luôn khởi động cùng Windows. Không thể tắt tính năng này."
        )

    # Đảm bảo tự động khởi động cùng Windows luôn được kích hoạt
    try:
        enable_autostart()
    except Exception:
        pass

    menu = Menu(
        item("🖥️ Mở giao diện", on_transparency_view, default=True),
        Menu.SEPARATOR,
        item("⏱️ Xem thời gian còn lại hôm nay", on_check_time),
        item("⏳ Xin thêm thời gian...", on_request_more_time),
        item("🔗 Ghép đôi lại thiết bị...", lambda icon, item: open_pairing_dialog()),
        item("🔒 Khởi động cùng Windows (Bắt buộc)", on_autostart_info, checked=lambda item: True),
        Menu.SEPARATOR,
        item(f"🛡️ {APP_TITLE}", None, enabled=False),
        item(f"💻 Máy: {device_label}", None, enabled=False),
        item("🟢 Trạng thái: Đang bảo vệ & đồng hành", None, enabled=False),
        Menu.SEPARATOR,
        item("Thoát", on_exit)
    )

    icon = pystray.Icon(
        name="OGK-Agent",
        icon=icon_image,
        title="Open Guardian Kids - Đang đồng hành cùng em",
        menu=menu
    )

    return icon
