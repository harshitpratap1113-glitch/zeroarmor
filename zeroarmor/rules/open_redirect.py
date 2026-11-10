"""
Layer 27: Open Redirect & Phishing Boundary Armor
Inspects outgoing HTTP redirect targets (Location headers and redirect calls)
to prevent phishing scams, protocol-relative domain hijacking, and javascript pseudo-protocols.
"""

import re
import urllib.parse

DANGEROUS_REDIRECT_REGEX = re.compile(
    r"^(\s*javascript:|\s*data:|\s*vbscript:|/\\|//|\\\\)",
    re.IGNORECASE
)

def inspect_redirect_url(url: str, core, allowed_domains: list = None) -> bool:
    if not getattr(core, "enabled", True):
        return True
    if not isinstance(url, str):
        return True

    clean_url = url.strip()
    
    # 1. Block dangerous scheme or protocol-relative trick
    if DANGEROUS_REDIRECT_REGEX.search(clean_url):
        core.record_threat(
            rule_name="Open Redirect / Phishing Vulnerability",
            reason=f"Blocked dangerous redirect target with scheme or protocol-relative hijack: '{clean_url}'",
            payload=clean_url,
            block=True
        )
        return False

    # 2. If it contains an external domain, verify schema and validity
    if "://" in clean_url:
        parsed = urllib.parse.urlparse(clean_url)
        if parsed.scheme.lower() not in ["http", "https"]:
            core.record_threat(
                rule_name="Open Redirect / Phishing Vulnerability",
                reason=f"Blocked non-http redirect scheme: '{parsed.scheme}'",
                payload=clean_url,
                block=True
            )
            return False

    return True

def arm_open_redirect(core):
    core.inspect_redirect_url = lambda u, allowed=None: inspect_redirect_url(u, core, allowed)
