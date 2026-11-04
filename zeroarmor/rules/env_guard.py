"""
Layer 20: Sensitive File (.env/ssh/.git) Guard
Prevents exfiltration of local environment files, private keys, and git repositories.
"""

import re

SENSITIVE_FILES_REGEX = re.compile(
    r"(\.env(\.local|\.prod|\.production)?$|"
    r"\.git[/\\](config|HEAD)|"
    r"id_(rsa|ed25519|dsa)(\.pub)?$|"
    r"service_account\.json$|"
    r"credentials\.json$)",
    re.IGNORECASE
)

def inspect_sensitive_access(path_str: str, core) -> bool:
    if SENSITIVE_FILES_REGEX.search(path_str):
        core.record_threat(
            rule_name="Sensitive File Exfiltration (.env/keys)",
            reason=f"Blocked attempt to read sensitive system configuration/credential file: {path_str}",
            payload=path_str,
            block=True
        )
        return False
    return True

def arm_env_guard(core):
    core.inspect_sensitive_access = lambda p: inspect_sensitive_access(p, core)
