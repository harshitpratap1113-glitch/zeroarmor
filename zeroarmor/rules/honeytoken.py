"""
Layer 32: Active Honeytoken & Deception Canary
Deploys synthetic memory traps, canary header probes, and scanner honeypot endpoints
(/.env, /actuator/env, /wp-admin, /debug) to proactively identify and flag automated offensive crawlers.
"""

import time
from typing import Dict, Set

CANARY_HONEYPOT_PATHS = {
    "/.env",
    "/.git/config",
    "/actuator/env",
    "/wp-login.php",
    "/phpinfo.php",
    "/admin/config.json",
    "/.aws/credentials"
}

class DeceptionEngine:
    def __init__(self):
        self.flagged_ips: Set[str] = set()
        self.canary_tokens: Dict[str, str] = {
            "CANARY_TOKEN_99": "za_canary_sec_prod_99x",
            "CANARY_AWS_MOCK": "AKIAZA99CANARYTRAP01"
        }

    def check_honeypot_path(self, path: str, client_ip: str, core) -> bool:
        clean_path = path.split("?")[0].lower()
        if clean_path in CANARY_HONEYPOT_PATHS:
            self.flagged_ips.add(client_ip)
            core.record_threat(
                rule_name="Honeypot Scanner Trap Triggered",
                reason=f"Automated vulnerability scanner probed synthetic canary endpoint: '{clean_path}'",
                payload=f"Client: {client_ip}, Target: {clean_path}",
                block=True
            )
            return False
        return True

    def check_canary_leak(self, text: str, core) -> bool:
        for name, secret in self.canary_tokens.items():
            if secret in text:
                core.record_threat(
                    rule_name="Honeytoken Canary Compromise",
                    reason=f"Attacker submitted or exfiltrated synthetic canary credential: '{name}'",
                    payload=secret,
                    block=True
                )
                return False
        return True

_deception = DeceptionEngine()

def arm_honeytoken(core):
    core.deception = _deception
