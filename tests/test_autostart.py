"""Tests for Windows Auto-Start Manager (agent/autostart.py).
Verifies registry registration, command construction, and enablement state.
"""

import sys
import os
import pytest

# Ensure project root is in sys.path
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from agent.autostart import (
    get_agent_launch_command,
    is_autostart_enabled,
    enable_autostart,
    disable_autostart
)


def test_get_agent_launch_command():
    """Verify launch command points to python/pythonw and agent/main.py."""
    cmd = get_agent_launch_command()
    assert "main.py" in cmd
    assert ("python" in cmd.lower() or "pythonw" in cmd.lower())


def test_enable_and_disable_autostart_registry():
    """Test full cycle: enable autostart, verify is_autostart_enabled(), disable, verify disabled."""
    initial_state = is_autostart_enabled()

    try:
        # 1. Enable autostart
        ok, msg = enable_autostart()
        assert ok is True
        assert is_autostart_enabled() is True

        # 2. Disable autostart
        ok_dis, msg_dis = disable_autostart()
        assert ok_dis is True
        assert is_autostart_enabled() is False
    finally:
        # Restore initial state if it was originally enabled
        if initial_state:
            enable_autostart()
        else:
            disable_autostart()
