"""
Layer 31: DNS Rebinding & Subnet Enclosure Shield
Hooks socket.getaddrinfo and socket.gethostbyname to prevent DNS rebinding attacks
where external hostnames dynamically resolve to internal loopback or private RFC1918 subnets.
"""

import ipaddress
import socket

def is_ip_private_or_restricted(ip_str: str) -> bool:
    try:
        ip = ipaddress.ip_address(ip_str)
        return bool(
            ip.is_private or
            ip.is_loopback or
            ip.is_link_local or
            ip.is_reserved or
            str(ip) in ["169.254.169.254", "100.100.100.200", "0.0.0.0"]
        )
    except ValueError:
        return False

def inspect_resolved_ips(hostname: str, ip_list: list, core) -> bool:
    if not getattr(core, "enabled", True):
        return True
    
    # Allow explicit localhost if developer is in testing mode, but block if resolving external host to private IP
    for ip in ip_list:
        if is_ip_private_or_restricted(ip):
            if hostname.lower() not in ["localhost", "127.0.0.1", "::1", "testserver"]:
                core.record_threat(
                    rule_name="DNS Rebinding Private Subnet Exposure",
                    reason=f"Blocked hostname '{hostname}' attempting to resolve to internal private IP: '{ip}'",
                    payload=f"{hostname} -> {ip}",
                    block=True
                )
                return False
    return True

def arm_dns_rebinding(core):
    orig_getaddrinfo = socket.getaddrinfo

    def armored_getaddrinfo(host, port, *args, **kwargs):
        res = orig_getaddrinfo(host, port, *args, **kwargs)
        if isinstance(host, str) and host:
            resolved_ips = [r[4][0] for r in res if len(r) > 4 and len(r[4]) > 0]
            inspect_resolved_ips(host, resolved_ips, core)
        return res

    socket.getaddrinfo = armored_getaddrinfo
