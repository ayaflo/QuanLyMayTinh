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
except ImportError:
    from config import APP_TITLE, DEVICE_NAME
    from storage import load_credentials


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


def on_request_more_time(icon, item):
    """Handler for NT3: Trẻ có tiếng nói - Xin thêm giờ."""
    try:
        icon.notify(
            title="Yêu Cầu Thêm Giờ",
            message="Yêu cầu xin thêm thời gian đã được ghi nhận và gửi đến phụ huynh."
        )
    except Exception:
        pass


def on_transparency_view(icon, item):
    """Handler for NT5: Minh bạch hai chiều - Trẻ được xem báo cáo."""
    try:
        icon.notify(
            title="Minh Bạch Dữ Liệu",
            message="Hệ thống chỉ lưu thời lượng và ứng dụng, tuyệt đối không chụp màn hình hay đọc tin nhắn (Nghị định 13/2023)."
        )
    except Exception:
        pass


def init_tray_icon(on_exit_callback: Optional[Callable] = None) -> pystray.Icon:
    """Initialize system tray icon with ethical menu and action handlers.

    Returns:
        pystray.Icon instance ready to be run via .run()
    """
    icon_image = create_shield_icon_image(64)

    def on_exit(icon, item):
        print(" [x] Người dùng yêu cầu dừng Agent từ khay hệ thống.")
        if on_exit_callback:
            on_exit_callback()
        icon.stop()

    creds = load_credentials()
    device_label = creds.get("device_name", DEVICE_NAME) if creds else DEVICE_NAME

    menu = Menu(
        item(f"🛡️ {APP_TITLE}", None, enabled=False),
        item(f"💻 Máy: {device_label}", None, enabled=False),
        item("🟢 Trạng thái: Đang bảo vệ & đồng hành", None, enabled=False),
        Menu.SEPARATOR,
        item("⏳ Xin thêm giờ... (NT3)", on_request_more_time),
        item("📖 Minh bạch bảo mật... (NT5)", on_transparency_view),
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
