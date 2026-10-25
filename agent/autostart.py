"""Windows Auto-Start Manager for Open Guardian Kids (OGK) Client Agent.
Ensures the Agent automatically launches upon Windows boot / user login
to maintain continuous parental guidance and protection.
"""

import os
import sys
import winreg
from typing import Tuple, Optional

APP_REG_KEY = "OpenGuardianKidsAgent"
REG_RUN_PATH = r"Software\Microsoft\Windows\CurrentVersion\Run"


def get_agent_launch_command() -> str:
    """Construct the optimal silent launch command using pythonw.exe if available."""
    # Find pythonw.exe to avoid pop-up console window
    python_dir = os.path.dirname(sys.executable)
    pythonw = os.path.join(python_dir, "pythonw.exe")
    exe = pythonw if os.path.isfile(pythonw) else sys.executable

    agent_main = os.path.join(os.path.dirname(os.path.abspath(__file__)), "main.py")
    return f'"{exe}" "{agent_main}"'


def is_autostart_enabled() -> bool:
    """Check if Open Guardian Kids is registered in Windows Startup Registry."""
    try:
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, REG_RUN_PATH, 0, winreg.KEY_READ) as key:
            val, _ = winreg.QueryValueEx(key, APP_REG_KEY)
            return bool(val)
    except FileNotFoundError:
        return False
    except Exception:
        return False


def enable_autostart() -> Tuple[bool, str]:
    """Register agent launch command into HKCU\\...\\Run so it starts with Windows."""
    cmd = get_agent_launch_command()
    try:
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, REG_RUN_PATH, 0, winreg.KEY_SET_VALUE) as key:
            winreg.SetValueEx(key, APP_REG_KEY, 0, winreg.REG_SZ, cmd)
        return True, f"Đã đăng ký khởi động cùng Windows thành công: {cmd}"
    except Exception as e:
        return False, f"Không thể ghi vào Windows Registry: {str(e)}"


def disable_autostart() -> Tuple[bool, str]:
    """Remove Open Guardian Kids from Windows Startup Registry."""
    try:
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, REG_RUN_PATH, 0, winreg.KEY_SET_VALUE) as key:
            winreg.DeleteValue(key, APP_REG_KEY)
        return True, "Đã hủy kích hoạt tự khởi động cùng Windows."
    except FileNotFoundError:
        return True, "Ứng dụng chưa được cài đặt tự khởi động."
    except Exception as e:
        return False, f"Lỗi khi xóa khỏi Windows Registry: {str(e)}"


def install_startup_vbs_shortcut() -> Tuple[bool, str]:
    """Create a silent launcher script in Windows Startup folder as a robust redundancy."""
    try:
        startup_dir = os.path.join(
            os.environ.get("APPDATA", ""),
            r"Microsoft\Windows\Start Menu\Programs\Startup"
        )
        if not os.path.isdir(startup_dir):
            return False, "Không tìm thấy thư mục Windows Startup."

        vbs_path = os.path.join(startup_dir, "OpenGuardianKids_SilentLaunch.vbs")
        cmd = get_agent_launch_command().replace('"', '""')
        vbs_content = (
            'Set WshShell = CreateObject("WScript.Shell")\n'
            f'WshShell.Run "{cmd}", 0, False\n'
            'Set WshShell = Nothing\n'
        )

        with open(vbs_path, "w", encoding="utf-8") as f:
            f.write(vbs_content)

        return True, f"Đã tạo tệp khởi động ngầm tại: {vbs_path}"
    except Exception as e:
        return False, f"Lỗi tạo tệp khởi động ngầm: {str(e)}"


def remove_startup_vbs_shortcut() -> Tuple[bool, str]:
    """Remove the silent launcher script from Windows Startup folder."""
    try:
        startup_dir = os.path.join(
            os.environ.get("APPDATA", ""),
            r"Microsoft\Windows\Start Menu\Programs\Startup"
        )
        vbs_path = os.path.join(startup_dir, "OpenGuardianKids_SilentLaunch.vbs")
        if os.path.isfile(vbs_path):
            os.remove(vbs_path)
            return True, "Đã gỡ tệp khởi động ngầm."
        return True, "Tệp không tồn tại."
    except Exception as e:
        return False, f"Lỗi xóa tệp: {str(e)}"


if __name__ == "__main__":
    if sys.stdout.encoding != "utf-8":
        try:
            sys.stdout.reconfigure(encoding="utf-8")
        except Exception:
            pass
    print("Kiểm tra trạng thái tự khởi động cùng Windows:")
    active = is_autostart_enabled()
    print(f" - Trạng thái hiện tại: {'ĐÃ BẬT' if active else 'CHƯA BẬT'}")
    print(f" - Lệnh khởi động dự kiến: {get_agent_launch_command()}")
