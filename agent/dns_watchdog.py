"""DNS Watchdog Guard for Open Guardian Kids (T4_017 & T4_018 - M3 Anti-Bypass).
Monitors active network adapters every 20 seconds to ensure DNS configuration
points to 127.0.0.1 (local sinkhole proxy).
Automatically restores 127.0.0.1 and emits 'tamper_attempt' telemetry upon detection
of unauthorized manual DNS modification or DHCP revert.
"""

import re
import sys
import time
import subprocess
import threading
import logging
from typing import Optional, List, Callable, Dict, Any

try:
    from agent.dns_configurator import get_active_interfaces, set_dns_to_localhost
except ImportError:
    try:
        from dns_configurator import get_active_interfaces, set_dns_to_localhost
    except ImportError:
        def get_active_interfaces() -> List[str]:
            return ["Wi-Fi"]
        def set_dns_to_localhost(iface: Optional[str] = None) -> bool:
            return True

logger = logging.getLogger("OGK_DNSWatchdog")

# Regex to capture IPv4 addresses
IPV4_REGEX = re.compile(r"\b(?:\d{1,3}\.){3}\d{1,3}\b")


def get_adapter_dns_servers(interface_name: str) -> List[str]:
    """Query currently configured DNS servers for a network interface on Windows (M3)."""
    if sys.platform != "win32":
        # Non-Windows simulated environment
        return ["127.0.0.1"]

    try:
        cmd = f'netsh interface ipv4 show dns name="{interface_name}"'
        res = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=5)
        if res.returncode != 0:
            logger.debug(f"netsh show dns failed for '{interface_name}': {res.stderr.strip()}")
            return []

        output = res.stdout
        # Extract all IPv4 addresses in output
        found_ips = IPV4_REGEX.findall(output)
        # Deduplicate while preserving order
        unique_ips = []
        for ip in found_ips:
            if ip not in unique_ips:
                unique_ips.append(ip)
        return unique_ips
    except Exception as e:
        logger.warning(f"Error querying DNS for adapter '{interface_name}': {e}")
        return []


class DNSWatchdog:
    """Watchdog thread that monitors active network adapter DNS and auto-remediates (T4_017, T4_018)."""

    def __init__(
        self,
        check_interval_sec: float = 20.0,
        target_dns: str = "127.0.0.1",
        on_tamper_callback: Optional[Callable[[str, List[str]], None]] = None,
        interfaces_provider: Optional[Callable[[], List[str]]] = None
    ):
        self.check_interval_sec = check_interval_sec
        self.target_dns = target_dns
        self.on_tamper_callback = on_tamper_callback
        self.interfaces_provider = interfaces_provider or get_active_interfaces

        self._running = False
        self._thread: Optional[threading.Thread] = None
        self._stop_event = threading.Event()
        self._last_alert_time: Dict[str, float] = {}

    def check_and_restore_dns(self) -> List[Dict[str, Any]]:
        """Scan active network adapters, detect DNS alterations, and remediate back to 127.0.0.1."""
        tampered_adapters = []
        try:
            active_ifaces = self.interfaces_provider()
        except Exception as e:
            logger.error(f"Failed to query active interfaces: {e}")
            return []

        for iface in active_ifaces:
            # Skip loopback or pseudo interfaces
            if not iface or "loopback" in iface.lower() or "pseudo" in iface.lower():
                continue

            current_dns = get_adapter_dns_servers(iface)

            # If 127.0.0.1 is missing from configured DNS servers
            if self.target_dns not in current_dns:
                logger.warning(
                    f"[ANTI-BYPASS M3] DNS tamper detected on adapter '{iface}'! "
                    f"Configured: {current_dns}. Restoring to {self.target_dns}..."
                )

                # Step 1: Auto-remediation (T4_018)
                remediation_ok = set_dns_to_localhost(iface)

                # Step 2: Rate-limited tamper alert & telemetry callback (once per 15s per adapter)
                now = time.time()
                last_alert = self._last_alert_time.get(iface, 0)
                if (now - last_alert) >= 15.0:
                    self._last_alert_time[iface] = now
                    if self.on_tamper_callback:
                        try:
                            self.on_tamper_callback(iface, current_dns)
                        except Exception as cb_err:
                            logger.error(f"Error in on_tamper_callback: {cb_err}")

                tampered_adapters.append({
                    "interface": iface,
                    "old_dns": current_dns,
                    "remediation_success": remediation_ok
                })

        return tampered_adapters

    def _loop(self):
        """Worker thread loop executing periodic DNS adapter health check."""
        logger.info(f"[*] DNS Watchdog started (interval={self.check_interval_sec}s, target={self.target_dns})")
        while not self._stop_event.is_set():
            try:
                self.check_and_restore_dns()
            except Exception as e:
                logger.error(f"Unexpected error in DNS Watchdog loop: {e}")

            self._stop_event.wait(timeout=self.check_interval_sec)

        logger.info("[*] DNS Watchdog loop terminated.")

    def start(self):
        """Start the watchdog daemon thread (T4_020)."""
        if self._running:
            return
        self._running = True
        self._stop_event.clear()
        self._thread = threading.Thread(
            target=self._loop,
            daemon=True,
            name="OGK_DNS_Watchdog"
        )
        self._thread.start()

    def stop(self):
        """Stop the watchdog thread gracefully."""
        self._running = False
        self._stop_event.set()
        if self._thread and self._thread.is_alive():
            self._thread.join(timeout=2.0)
        self._thread = None
