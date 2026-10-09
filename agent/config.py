"""Agent configuration file for Open Guardian Kids (OGK).
Defines server endpoints, heartbeat intervals, and local storage paths.
"""

import os
import platform

# Server connection configuration
SERVER_HOST = os.getenv("SERVER_HOST", "127.0.0.1")
SERVER_PORT = int(os.getenv("SERVER_PORT", "8000"))
DEFAULT_SERVER_URL = f"http://{SERVER_HOST}:{SERVER_PORT}"
SERVER_URL = os.getenv("OGK_SERVER_URL", os.getenv("SERVER_URL", DEFAULT_SERVER_URL)).rstrip("/")

# Heartbeat interval in seconds (default: 60s as specified in Week 1 DoD)
HEARTBEAT_INTERVAL = int(os.getenv("OGK_HEARTBEAT_INTERVAL", "60"))

# Local SQLite cache database for storing paired credentials and policy cache
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.getenv("OGK_AGENT_DB", os.path.join(BASE_DIR, "agent_cache.db"))

# Device identification metadata
DEVICE_NAME = os.getenv("OGK_DEVICE_NAME", platform.node() or "Windows PC")
APP_TITLE = "Open Guardian Kids (OGK)"
APP_VERSION = "0.1.0"
