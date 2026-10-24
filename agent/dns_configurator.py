"""Windows DNS Adapter Configurator for Open Guardian Kids (T3_036).
Directs primary network interface DNS to 127.0.0.1 during active agent session,
and restores DHCP upon graceful termination.
"""

import sys
import subprocess
import logging
from typing import Optional, List

logger = logging.getLogger("OGK_DNSConfig")


def get_active_interfaces() -> List[str]:
    """Discover names of active network interfaces (e.g. 'Wi-Fi', 'Ethernet') on Windows."""
    if sys.platform != "win32":
        return ["MockInterface"]

    interfaces = []
    try:
        output = subprocess.check_output(
            ["netsh", "interface", "ipv4", "show", "interfaces"],
            stderr=subprocess.DEVNULL,
            text=True
        )
        for line in output.splitlines():
            line = line.strip()
            if "connected" in line.lower():
                parts = line.split()
                if len(parts) >= 5:
                    iface_name = " ".join(parts[4:])
                    if iface_name and iface_name not in interfaces and "loopback" not in iface_name.lower():
                        interfaces.append(iface_name)
    except Exception as e:
        logger.warning(f"Could not discover network interfaces via netsh: {e}")
        interfaces = ["Wi-Fi", "Ethernet"]

    return interfaces or ["Wi-Fi"]


def set_dns_to_localhost(interface_name: Optional[str] = None) -> bool:
    """Configure network adapter DNS to 127.0.0.1 (T3_036)."""
    if sys.platform != "win32":
        logger.info(f"[SIMULATED] Set DNS to 127.0.0.1 on {interface_name or 'MockInterface'}")
        return True

    targets = [interface_name] if interface_name else get_active_interfaces()
    success = False

    for iface in targets:
        try:
            cmd = f'netsh interface ipv4 set dns name="{iface}" static 127.0.0.1 primary'
            res = subprocess.run(cmd, shell=True, capture_output=True, text=True)
            if res.returncode == 0:
                logger.info(f"Successfully configured DNS on interface '{iface}' to 127.0.0.1")
                success = True
            else:
                logger.warning(f"netsh returned code {res.returncode} for interface '{iface}': {res.stderr.strip()}")
        except Exception as e:
            logger.error(f"Failed to configure DNS for '{iface}': {e}")

    return success


def restore_dns_to_dhcp(interface_name: Optional[str] = None) -> bool:
    """Restore network adapter DNS to automatic DHCP (T3_036)."""
    if sys.platform != "win32":
        logger.info(f"[SIMULATED] Restore DNS to DHCP on {interface_name or 'MockInterface'}")
        return True

    targets = [interface_name] if interface_name else get_active_interfaces()
    success = False

    for iface in targets:
        try:
            cmd = f'netsh interface ipv4 set dns name="{iface}" dhcp'
            res = subprocess.run(cmd, shell=True, capture_output=True, text=True)
            if res.returncode == 0:
                logger.info(f"Successfully restored DNS on interface '{iface}' to DHCP")
                success = True
        except Exception as e:
            logger.error(f"Failed to restore DHCP for '{iface}': {e}")

    return success
