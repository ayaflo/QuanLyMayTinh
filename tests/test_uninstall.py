"""Tests for Agent Uninstaller and Demo Reset (agent/uninstall.py).
Verifies:
1. Interface discovery and admin checks.
2. Clean removal of blocked domains from Windows hosts file.
3. Database wipe and backup functionality.
4. Orchestrated full uninstall workflow.
"""

import os
import sys
import tempfile
import pytest

# Ensure project root is in sys.path
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from agent.uninstall import (
    is_admin,
    get_all_network_interfaces,
    restore_hosts_file_clean,
    wipe_local_agent_db,
    clean_pycache,
    run_full_uninstall,
    HOSTS_MARKER_START,
    HOSTS_MARKER_END
)


def test_is_admin_check():
    """Verify is_admin() returns a boolean without throwing exceptions."""
    res = is_admin()
    assert isinstance(res, bool)


def test_get_all_network_interfaces():
    """Verify get_all_network_interfaces returns a non-empty list of interface names."""
    ifaces = get_all_network_interfaces()
    assert isinstance(ifaces, list)
    assert len(ifaces) > 0
    assert all(isinstance(name, str) for name in ifaces)


def test_restore_hosts_file_clean_preserves_other_entries():
    """Verify restore_hosts_file_clean strips OGK blocked section and preserves standard entries."""
    with tempfile.NamedTemporaryFile("w+", delete=False, encoding="utf-8") as tmp:
        initial_content = (
            "127.0.0.1 localhost\n"
            "::1 localhost\n"
            "# Custom local entry\n"
            "192.168.1.50 myrouter.local\n\n"
            f"{HOSTS_MARKER_START}\n"
            "0.0.0.0 youtube.com\n"
            "0.0.0.0 www.youtube.com\n"
            "0.0.0.0 roblox.com\n"
            f"{HOSTS_MARKER_END}\n"
        )
        tmp.write(initial_content)
        tmp_path = tmp.name

    try:
        ok = restore_hosts_file_clean(hosts_path=tmp_path)
        assert ok is True

        with open(tmp_path, "r", encoding="utf-8") as f:
            cleaned = f.read()

        # OGK markers and blocked domains must be completely removed
        assert HOSTS_MARKER_START not in cleaned
        assert HOSTS_MARKER_END not in cleaned
        assert "youtube.com" not in cleaned
        assert "roblox.com" not in cleaned

        # Original entries must be preserved
        assert "127.0.0.1 localhost" in cleaned
        assert "myrouter.local" in cleaned
    finally:
        if os.path.exists(tmp_path):
            os.remove(tmp_path)


def test_wipe_local_agent_db_with_backup():
    """Verify wipe_local_agent_db deletes db and wal files and creates a backup."""
    tmp_dir = tempfile.mkdtemp()
    db_file = os.path.join(tmp_dir, "test_cache.db")
    wal_file = os.path.join(tmp_dir, "test_cache.db-wal")

    # Create dummy database and wal files
    with open(db_file, "w", encoding="utf-8") as f:
        f.write("DUMMY_SQLITE_DATA")
    with open(wal_file, "w", encoding="utf-8") as f:
        f.write("DUMMY_WAL_DATA")

    try:
        res = wipe_local_agent_db(db_path=db_file, backup=True)
        assert res["success"] is True
        assert not os.path.exists(db_file)
        assert not os.path.exists(wal_file)
        assert res["backup_file"] is not None
        assert os.path.exists(res["backup_file"])
    finally:
        # Cleanup temp directory
        for f in os.listdir(tmp_dir):
            try:
                os.remove(os.path.join(tmp_dir, f))
            except Exception:
                pass
        try:
            os.rmdir(tmp_dir)
        except Exception:
            pass


def test_clean_pycache_execution():
    """Verify clean_pycache runs without error."""
    count = clean_pycache()
    assert isinstance(count, int)
    assert count >= 0


def test_run_full_uninstall_structure(monkeypatch):
    """Verify run_full_uninstall orchestrates all steps and returns summary dict."""
    monkeypatch.setattr("agent.uninstall.notify_server_unenroll", lambda: {"attempted": True, "success": True, "message": "Mock success"})
    monkeypatch.setattr("agent.uninstall.restore_all_dns_adapters", lambda: [{"interface": "Mock", "ipv4": True}])
    monkeypatch.setattr("agent.uninstall.restore_hosts_file_clean", lambda: True)
    monkeypatch.setattr("agent.uninstall.remove_browser_doh_policies", lambda: True)
    monkeypatch.setattr("agent.uninstall.remove_autostart_entries", lambda: {"hkcu_registry": True})
    monkeypatch.setattr("agent.uninstall.flush_dns", lambda: True)

    summary = run_full_uninstall(wipe_db=False, verbose=False)

    assert "server_unenroll" in summary
    assert summary["server_unenroll"]["success"] is True

    assert "killed_processes" in summary
    assert "dns_restored" in summary
    assert "hosts_cleaned" in summary
    assert "browser_doh_cleaned" in summary
    assert "autostart_removed" in summary
    assert "db_wipe" in summary
    assert summary["db_wipe"]["skipped"] is True
    assert summary["hosts_cleaned"] is True
