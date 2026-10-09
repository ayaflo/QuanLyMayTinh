"""Hardware fingerprint extractor for Windows client agent.
Extracts persistent MachineGuid from Windows Registry, with fallback to hardware MAC.
"""

import sys
import uuid
import hashlib
import platform


def get_device_fingerprint() -> str:
    """Retrieve unique, persistent hardware fingerprint for the machine.

    On Windows:
        Reads MachineGuid from HKEY_LOCAL_MACHINE\\SOFTWARE\\Microsoft\\Cryptography.
    Fallback:
        Generates SHA-256 hash combining node name and hardware MAC address.
    """
    if sys.platform == "win32":
        try:
            import winreg
            key = winreg.OpenKey(
                winreg.HKEY_LOCAL_MACHINE,
                r"SOFTWARE\Microsoft\Cryptography",
                0,
                winreg.KEY_READ | winreg.KEY_WOW64_64KEY
            )
            guid, _ = winreg.QueryValueEx(key, "MachineGuid")
            winreg.CloseKey(key)
            if guid and len(str(guid).strip()) > 0:
                return str(guid).strip()
        except Exception:
            pass

    # Universal hardware fallback
    mac = uuid.getnode()
    node = platform.node()
    raw = f"{node}:{mac}:{sys.platform}"
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()[:36]


if __name__ == "__main__":
    fp = get_device_fingerprint()
    print(f"Device Fingerprint: {fp}")
