"""
Layer 20: Sensitive File (.env/ssh/.git) Guard
Prevents exfiltration of local environment files, private keys, and git repositories.
"""

import re
import os

SENSITIVE_FILES_REGEX = re.compile(
    r"(\.env(\.local|\.prod|\.production|\.staging|\.test|\.bak)?$|"
    r"\.git[/\\](config|HEAD|index|refs)|"
    r"id_(rsa|ed25519|dsa|ecdsa)(\.pub)?$|"
    r"authorized_keys$|"
    r"service_account.*\.json$|"
    r"credentials\.json$|"
    r"secret(s)?\.(json|yaml|yml|toml)$|"
    r"wp-config\.php$|"
    r"\.htpasswd$)",
    re.IGNORECASE
)

def inspect_sensitive_access(path_str: str, core) -> bool:
    if not getattr(core, "enabled", True):
        return True
    if not isinstance(path_str, (str, bytes, os.PathLike)):
        return True

    clean_path = str(path_str).strip()
    if SENSITIVE_FILES_REGEX.search(clean_path):
        core.record_threat(
            rule_name="Sensitive File Exfiltration (.env/keys)",
            reason=f"Blocked attempt to access sensitive system configuration or credential file: {clean_path}",
            payload=clean_path,
            block=True
        )
        return False
    return True

def arm_env_guard(core):
    core.inspect_sensitive_access = lambda p: inspect_sensitive_access(p, core)
