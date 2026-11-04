"""
Layer 4: SSRF & Cloud Metadata Guard
Hooks outbound network requests (urllib, requests, http.client) to block SSRF and cloud metadata theft.
"""

import ipaddress
import re
import sys
import urllib.parse
import urllib.request
import http.client

DANGEROUS_HOSTS = {
    "169.254.169.254", # AWS/Azure/GCP Metadata
    "127.0.0.1",
    "localhost",
    "0.0.0.0",
    "::1",
    "instance-data",
    "metadata.google.internal"
}

def inspect_url(url: str, core) -> bool:
    if not isinstance(url, str):
        return True

    parsed = urllib.parse.urlparse(url)
    hostname = parsed.hostname or ""
    hostname = hostname.strip().lower()

    # 1. Exact match on known cloud metadata / loopback
    if hostname in DANGEROUS_HOSTS:
        core.record_threat(
            rule_name="SSRF Cloud Metadata Theft",
            reason=f"Blocked attempt to access private/cloud metadata target: {hostname}",
            payload=url,
            block=True
        )
        return False

    # 2. Check if IP address is in private / loopback / link-local space
    try:
        ip = ipaddress.ip_address(hostname)
        if ip.is_private or ip.is_loopback or ip.is_link_local or ip.is_reserved:
            core.record_threat(
                rule_name="SSRF Private Subnet Access",
                reason=f"Blocked attempt to access internal private IP address: {ip}",
                payload=url,
                block=True
            )
            return False
    except ValueError:
        pass # Not a raw IP address

    return True

def arm_ssrf(core):
    # Hook urllib.request.urlopen
    orig_urlopen = urllib.request.urlopen
    def armored_urlopen(url, *args, **kwargs):
        target = url.full_url if hasattr(url, "full_url") else str(url)
        inspect_url(target, core)
        return orig_urlopen(url, *args, **kwargs)
    urllib.request.urlopen = armored_urlopen

    # Hook http.client.HTTPConnection.request
    orig_http_request = http.client.HTTPConnection.request
    def armored_http_request(self, method, url, *args, **kwargs):
        host = getattr(self, "host", "")
        inspect_url(f"http://{host}{url}", core)
        return orig_http_request(self, method, url, *args, **kwargs)
    http.client.HTTPConnection.request = armored_http_request

    # Hook requests if already in sys.modules or when imported
    if "requests" in sys.modules:
        try:
            import requests
            orig_req_send = requests.Session.send
            def armored_req_send(self, request, *args, **kwargs):
                inspect_url(request.url, core)
                return orig_req_send(self, request, *args, **kwargs)
            requests.Session.send = armored_req_send
        except Exception:
            pass
