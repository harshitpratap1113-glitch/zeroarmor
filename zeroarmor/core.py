"""
ZeroArmor Core Orchestrator
Coordinates all 22 defense layers and logs blocked attack telemetry.
"""

import sys
import time
from typing import Dict, List, Any, Optional

class ShieldBlockedException(PermissionError):
    """Raised when ZeroArmor intercepts and neutralizes a live cyber exploit."""
    def __init__(self, rule_name: str, details: str, payload: str = ""):
        self.rule_name = rule_name
        self.details = details
        self.payload = payload
        super().__init__(f"[ZeroArmor] Blocked {rule_name}: {details}")

class ThreatEvent:
    def __init__(self, rule: str, reason: str, payload: str = "", source: str = "local"):
        self.timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        self.rule = rule
        self.reason = reason
        self.payload = payload[:200]
        self.source = source

    def to_dict(self) -> Dict[str, Any]:
        return {
            "timestamp": self.timestamp,
            "rule": self.rule,
            "reason": self.reason,
            "payload": self.payload,
            "source": self.source
        }

class ZeroArmorCore:
    _instance: Optional['ZeroArmorCore'] = None

    def __init__(self):
        self.active_shields: Dict[str, bool] = {}
        self.telemetry: List[Dict[str, Any]] = []
        self._armed = False
        self.enabled = True

    @classmethod
    def get_instance(cls) -> 'ZeroArmorCore':
        if cls._instance is None:
            cls._instance = ZeroArmorCore()
        return cls._instance

    def record_threat(self, rule_name: str, reason: str, payload: str = "", block: bool = True):
        if not getattr(self, "enabled", True):
            return
        event = ThreatEvent(rule=rule_name, reason=reason, payload=payload)
        self.telemetry.append(event.to_dict())
        
        sys.stderr.write(
            f"\n\033[91m[ZeroArmor THREAT INTERCEPTED]\033[0m\n"
            f"   |-- Rule: \033[93m{rule_name}\033[0m\n"
            f"   |-- Reason: {reason}\n"
            f"   \\-- Neutralized Payload: \033[90m{payload[:120]}\033[0m\n\n"
        )
        sys.stderr.flush()

        if block:
            raise ShieldBlockedException(rule_name, reason, payload)

    def auto_arm(self):
        """Automatically ignite all 22 security layers upon import."""
        if self._armed:
            return
        self._armed = True

        from .rules import (
            arm_sqli,
            arm_rce,
            arm_path_traversal,
            arm_ssrf,
            arm_deserialization,
            arm_eval_exec,
            arm_secret_scrubber,
            arm_redos,
            arm_dos_limiter,
            arm_attr_pollution,
            arm_zip_slip,
            arm_temp_file,
            arm_ssti,
            arm_headers,
            arm_cors,
            arm_env_guard,
            arm_dlp,
            arm_rate_limiter
        )

        shields = [
            ("SQL Injection Armor", arm_sqli),
            ("RCE & Shell Jail", arm_rce),
            ("Path Traversal Prison", arm_path_traversal),
            ("SSRF & Cloud Metadata Guard", arm_ssrf),
            ("Deserialization Sanitizer", arm_deserialization),
            ("Code Injection (eval/exec) Sandbox", arm_eval_exec),
            ("Real-Time Secret Scrubber", arm_secret_scrubber),
            ("ReDoS Catastrophic Backtracking Guard", arm_redos),
            ("Memory Bomb & DoS Limiter", arm_dos_limiter),
            ("Class Attribute Pollution Freeze", arm_attr_pollution),
            ("Zip Slip & Tar Bomb Jail", arm_zip_slip),
            ("Secure Temp File Enforcer", arm_temp_file),
            ("SSTI Template Injection Guard", arm_ssti),
            ("HTTP Security Headers & CSP", arm_headers),
            ("Insecure CORS Wildcard Guard", arm_cors),
            ("Sensitive File (.env/ssh) Guard", arm_env_guard),
            ("Outbound DLP Data Loss Prevention", arm_dlp),
            ("Anti-Bot Rate Limiter", arm_rate_limiter)
        ]

        for name, arm_func in shields:
            try:
                arm_func(self)
                self.active_shields[name] = True
            except Exception as e:
                self.active_shields[name] = False
                sys.stderr.write(f"[ZeroArmor] Warning during {name}: {e}\n")

        self.print_status()

    def get_status(self) -> Dict[str, Any]:
        return {
            "status": "ARMED" if self._armed else "DISARMED",
            "active_shields_count": sum(1 for v in self.active_shields.values() if v),
            "total_shields_count": len(self.active_shields),
            "shields": self.active_shields,
            "blocked_attacks_count": len(self.telemetry)
        }

    def print_status(self):
        active = sum(1 for v in self.active_shields.values() if v)
        sys.stderr.write(
            f"\033[92m[ZeroArmor v1.0 Community]: Z+ Security Active ({active}/22 Layers Armed)\033[0m\n"
        )
        sys.stderr.flush()

def get_shield() -> ZeroArmorCore:
    return ZeroArmorCore.get_instance()
