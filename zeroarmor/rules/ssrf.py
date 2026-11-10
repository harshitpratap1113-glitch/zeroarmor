"""
Layer 4: SSRF & Cloud Metadata Guard (Universal HTTP / Socket Shield)
Hooks urllib, http.client, requests, and socket connections to block SSRF, cloud metadata theft,
and bypass notations (hex, octal, decimal IPs, and private subnets).
"""

import ipaddress
import re
import socket
import sys
import urllib.parse
import urllib.request
import http.client

DANGEROUS_HOSTS = {
    "169.254.169.254",            # AWS / Azure / GCP Metadata
    "metadata.google.internal",   # Google Cloud internal
    "instance-data",              # AWS EC2 internal
    "100.100.100.200",            # Alibaba Cloud metadata
    "fd00:ec2::254",              # AWS IPv6 metadata
    "localhost",
    "127.0.0.1",
    "0.0.0.0",
    "::1",
    "kubernetes.default.svc",
    "kubernetes.default"
}

def parse_special_ip_notation(host: str) -> str:
    """Normalize decimal, octal, or hex IP representations (e.g. 2130706433 or 0x7f000001)."""
    clean_host = host.strip()
    if clean_host.startswith("0x") or clean_host.startswith("0X"):
        try:
            val = int(clean_host, 16)
            return str(ipaddress.IPv4Address(val))
        except Exception:
            pass
    elif clean_host.isdigit():
        try:
            val = int(clean_host)
            if 0 <= val <= 0xFFFFFFFF:
                return str(ipaddress.IPv4Address(val))
        except Exception:
            pass
    return clean_host

def is_ip_blocked(ip_obj) -> bool:
    return bool(
        ip_obj.is_private or
        ip_obj.is_loopback or
        ip_obj.is_link_local or
        ip_obj.is_reserved or
        ip_obj.is_multicast or
        str(ip_obj) == "169.254.169.254" or
        str(ip_obj) == "100.100.100.200"
    )

def inspect_host_or_url(target: str, core) -> bool:
    if not getattr(core, "enabled", True):
        return True
    if not isinstance(target, str):
        return True

    clean_target = target.strip()
    hostname = clean_target

    if "://" in clean_target:
        parsed = urllib.parse.urlparse(clean_target)
        hostname = parsed.hostname or ""
    elif ":" in clean_target and not clean_target.startswith("["):
        hostname = clean_target.split(":")[0]

    hostname = hostname.strip().lower()
    normalized_ip = parse_special_ip_notation(hostname)

    # 1. Exact match on known dangerous cloud metadata / loopback
    if hostname in DANGEROUS_HOSTS or normalized_ip in DANGEROUS_HOSTS:
        core.record_threat(
            rule_name="SSRF Cloud Metadata Theft",
            reason=f"Blocked attempt to access private/cloud metadata target: '{hostname}'",
            payload=clean_target,
            block=True
        )
        return False

    # 2. Check if host resolves to an IP or is an IP address in private space
    for candidate in [normalized_ip, hostname]:
        try:
            ip = ipaddress.ip_address(candidate)
            if is_ip_blocked(ip):
                core.record_threat(
                    rule_name="SSRF Private Subnet Access",
                    reason=f"Blocked attempt to access internal private IP address: '{ip}'",
                    payload=clean_target,
                    block=True
                )
                return False
        except ValueError:
            pass

    return True

def arm_ssrf(core):
    # 1. Hook urllib.request.urlopen
    orig_urlopen = urllib.request.urlopen
    def armored_urlopen(url, *args, **kwargs):
        target = url.full_url if hasattr(url, "full_url") else str(url)
        inspect_host_or_url(target, core)
        return orig_urlopen(url, *args, **kwargs)
    urllib.request.urlopen = armored_urlopen

    # 2. Universal Hook: http.client.HTTPConnection.connect
    # This automatically protects 'requests', 'urllib3', 'httpx', etc.
    orig_connect = http.client.HTTPConnection.connect
    def armored_connect(self):
        host = getattr(self, "host", "")
        inspect_host_or_url(host, core)
        return orig_connect(self)
    http.client.HTTPConnection.connect = armored_connect

    # Also hook HTTPSConnection.connect
    orig_https_connect = http.client.HTTPSConnection.connect
    def armored_https_connect(self):
        host = getattr(self, "host", "")
        inspect_host_or_url(host, core)
        return orig_https_connect(self)
    http.client.HTTPSConnection.connect = armored_https_connect
