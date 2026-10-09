"""Client enrollment service for pairing child agent with parent account.
Sends pairing code and device fingerprint to the server's claim endpoint.
"""

from typing import Optional, Dict, Any, Tuple
import requests

try:
    from .config import SERVER_URL, DEVICE_NAME
    from .fingerprint import get_device_fingerprint
    from .storage import save_credentials
except ImportError:
    from config import SERVER_URL, DEVICE_NAME
    from fingerprint import get_device_fingerprint
    from storage import save_credentials


def pair_with_server(
    code: str,
    device_name: Optional[str] = None,
    server_url: str = SERVER_URL
) -> Tuple[bool, str, Optional[Dict[str, Any]]]:
    """Submit 8-character pairing code and device fingerprint to pair with parent account.

    Args:
        code: 8-character pairing code generated from parent dashboard.
        device_name: Optional custom friendly device name.
        server_url: Server base URL.

    Returns:
        (success: bool, message: str, data: Optional[Dict])
    """
    clean_code = code.strip().upper()
    if len(clean_code) != 8:
        return False, "Mã ghép đôi phải đúng 8 ký tự", None

    fingerprint = get_device_fingerprint()
    name = device_name or DEVICE_NAME

    endpoint = f"{server_url}/api/v1/enroll/claim"
    payload = {
        "code": clean_code,
        "device_fingerprint": fingerprint,
        "device_name": name
    }

    try:
        response = requests.post(
            endpoint,
            json=payload,
            headers={"Content-Type": "application/json"},
            timeout=10
        )

        if response.status_code == 200:
            data = response.json()
            device_id = data["device_id"]
            access_token = data["access_token"]
            refresh_token = data["refresh_token"]

            # Save credentials locally
            save_credentials(
                device_id=device_id,
                access_token=access_token,
                refresh_token=refresh_token,
                device_name=name
            )

            return True, "Ghép đôi thiết bị thành công!", data
        else:
            try:
                err_data = response.json()
                detail = err_data.get("detail", f"Máy chủ trả về mã lỗi {response.status_code}")
            except Exception:
                detail = f"Máy chủ trả về mã lỗi {response.status_code}"
            return False, detail, None

    except requests.exceptions.ConnectionError:
        return False, f"Không thể kết nối đến máy chủ tại {server_url}. Vui lòng kiểm tra lại mạng hoặc máy chủ.", None
    except requests.exceptions.Timeout:
        return False, "Hết thời gian chờ phản hồi từ máy chủ.", None
    except Exception as e:
        return False, f"Lỗi không xác định: {str(e)}", None
