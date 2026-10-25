"""Agent configuration file for Open Guardian Kids (OGK).
Defines server endpoints, heartbeat intervals, and local storage paths.
"""

import os
import platform
from urllib.parse import urlparse


def _load_env_file():
    """Load configuration variables from .env file if available."""
    candidates = [
        os.path.join(os.getcwd(), ".env"),
        os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), ".env"),
        os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env")
    ]
    for env_path in candidates:
        if os.path.isfile(env_path):
            try:
                with open(env_path, "r", encoding="utf-8") as f:
                    for line in f:
                        line = line.strip()
                        if line and not line.startswith("#") and "=" in line:
                            k, v = line.split("=", 1)
                            k, v = k.strip(), v.strip().strip("\"'")
                            if k not in os.environ:
                                os.environ[k] = v
            except Exception:
                pass
            break


_load_env_file()

# Server connection configuration with intelligent cloud resolution
_raw_server_url = os.getenv("OGK_SERVER_URL", os.getenv("SERVER_URL", "")).strip()

if _raw_server_url:
    if not _raw_server_url.startswith(("http://", "https://")):
        _raw_server_url = f"https://{_raw_server_url}"
    SERVER_URL = _raw_server_url.rstrip("/")
    _parsed = urlparse(SERVER_URL)
    SERVER_HOST = _parsed.hostname or "127.0.0.1"
    SERVER_PORT = _parsed.port or (443 if _parsed.scheme == "https" else 80)
else:
    SERVER_HOST = os.getenv("SERVER_HOST", "127.0.0.1").strip()
    # Auto-detect cloud hosting domains (Render, Railway, Vercel, Fly)
    if any(cloud_domain in SERVER_HOST for cloud_domain in [".onrender.com", ".railway.app", ".vercel.app", ".fly.dev"]):
        SERVER_PORT = int(os.getenv("SERVER_PORT", "443"))
        _scheme = "https" if SERVER_PORT == 443 or os.getenv("USE_SSL", "true").lower() == "true" else "http"
        SERVER_URL = f"{_scheme}://{SERVER_HOST}" if SERVER_PORT in (80, 443) else f"{_scheme}://{SERVER_HOST}:{SERVER_PORT}"
    else:
        SERVER_PORT = int(os.getenv("SERVER_PORT", "8000"))
        _scheme = "https" if os.getenv("USE_SSL", "false").lower() == "true" else "http"
        SERVER_URL = f"{_scheme}://{SERVER_HOST}:{SERVER_PORT}"

DEFAULT_SERVER_URL = SERVER_URL

# Network timeouts in seconds (Cloud-friendly for Render/Cloud cold starts)
REQUEST_TIMEOUT = int(os.getenv("OGK_REQUEST_TIMEOUT", "30"))

# Heartbeat interval in seconds (default: 60s as specified in Week 1 DoD)
HEARTBEAT_INTERVAL = int(os.getenv("OGK_HEARTBEAT_INTERVAL", "60"))

# Local SQLite cache database for storing paired credentials and policy cache
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.getenv("OGK_AGENT_DB", os.path.join(BASE_DIR, "agent_cache.db"))

# Device identification metadata
DEVICE_NAME = os.getenv("OGK_DEVICE_NAME", platform.node() or "Windows PC")
APP_TITLE = "Open Guardian Kids (OGK)"
APP_VERSION = "0.4.0"

