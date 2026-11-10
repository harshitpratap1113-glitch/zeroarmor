"""
ZeroArmor Core Orchestrator - v2.0 Titanium Shield Edition
Coordinates all 32 defense vectors, manages threat telemetry, enforcement modes,
and SIEM / Webhook alerting.
"""

import enum
import functools
import json
import sys
import time
from typing import Dict, List, Any, Optional, Callable

class DefenseMode(str, enum.Enum):
    BLOCK = "BLOCK"      # Strict Active Defense: Intercept and neutralize
    AUDIT = "AUDIT"      # Passive Canary Mode: Log telemetry without blocking
    DECEIVE = "DECEIVE"  # Active Honeypot: Deceptive response trap

class ShieldBlockedException(PermissionError):
    """Raised when ZeroArmor intercepts and neutralizes a live cyber exploit."""
    def __init__(self, rule_name: str, details: str, payload: str = ""):
        self.rule_name = rule_name
        self.details = details
        self.payload = payload
        super().__init__(f"[ZeroArmor Titanium] Blocked {rule_name}: {details}")

class ThreatEvent:
    def __init__(self, rule: str, reason: str, payload: str = "", source: str = "local"):
        self.timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        self.rule = rule
        self.reason = reason
        self.payload = payload[:300]
        self.source = source

    def to_dict(self) -> Dict[str, Any]:
        return {
            "timestamp": self.timestamp,
            "rule": self.rule,
            "reason": self.reason,
            "payload": self.payload,
            "source": self.source
        }

    def to_cef(self) -> str:
        """Format event in Common Event Format (CEF) for SIEM ingest."""
        clean_rule = self.rule.replace("|", "-")
        clean_reason = self.reason.replace("|", "-")
        clean_payload = self.payload.replace("|", "-")
        return (
            f"CEF:0|ZeroArmor|TitaniumRASP|2.0.0|{clean_rule}|{clean_reason}|8|"
            f"msg={clean_reason} cs1={clean_payload} cs1Label=Payload"
        )

class ZeroArmorCore:
    _instance: Optional['ZeroArmorCore'] = None

    def __init__(self):
        self.version = "2.0.0"
        self.mode = DefenseMode.BLOCK
        self.active_shields: Dict[str, bool] = {}
        self.telemetry: List[Dict[str, Any]] = []
        self._armed = False
        self.enabled = True
        self.webhook_url: Optional[str] = None
        self._safe_cache: Dict[str, bool] = {}

    @classmethod
    def get_instance(cls) -> 'ZeroArmorCore':
        if cls._instance is None:
            cls._instance = ZeroArmorCore()
        return cls._instance

    def set_mode(self, mode: DefenseMode):
        """Configure engine mode: BLOCK (strict), AUDIT (monitoring), or DECEIVE."""
        self.mode = mode

    def set_webhook(self, url: str):
        """Set outbound webhook URL for real-time security alerts."""
        self.webhook_url = url

    def record_threat(self, rule_name: str, reason: str, payload: str = "", block: bool = True):
        if not getattr(self, "enabled", True):
            return
        
        event = ThreatEvent(rule=rule_name, reason=reason, payload=payload)
        self.telemetry.append(event.to_dict())
        
        # High-contrast Terminal Alert
        sys.stderr.write(
            f"\n\033[91m[ZeroArmor TITANIUM THREAT INTERCEPTED]\033[0m\n"
            f"   |-- Rule: \033[93m{rule_name}\033[0m\n"
            f"   |-- Mode: \033[94m{self.mode.value}\033[0m\n"
            f"   |-- Reason: {reason}\n"
            f"   \\-- Neutralized Payload: \033[90m{payload[:120]}\033[0m\n\n"
        )
        sys.stderr.flush()

        # Fire webhook if configured (asynchronous / non-blocking best-effort)
        if self.webhook_url:
            self._dispatch_webhook(event)

        # Enforce action based on active defense mode
        if block and self.mode == DefenseMode.BLOCK:
            raise ShieldBlockedException(rule_name, reason, payload)

    def _dispatch_webhook(self, event: ThreatEvent):
        try:
            import urllib.request
            data = json.dumps(event.to_dict()).encode("utf-8")
            req = urllib.request.Request(
                self.webhook_url,
                data=data,
                headers={"Content-Type": "application/json", "User-Agent": "ZeroArmor-Titanium-RASP/2.0"}
            )
            # Timeout 1s to prevent blocking
            urllib.request.urlopen(req, timeout=1.0)
        except Exception:
            pass

    def auto_arm(self):
        """Automatically ignite all 32 Titanium security layers upon import."""
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
            arm_rate_limiter,
            arm_prompt_injection,
            arm_graphql_guard,
            arm_xxe,
            arm_nosql_injection,
            arm_open_redirect,
            arm_jwt_guard,
            arm_insecure_crypto,
            arm_yaml_gadget,
            arm_dns_rebinding,
            arm_honeytoken
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
            ("Anti-Bot Rate Limiter", arm_rate_limiter),
            ("LLM Prompt Injection & AI RASP", arm_prompt_injection),
            ("GraphQL Query Depth & Complexity Bomb", arm_graphql_guard),
            ("XML External Entity (XXE) & Bomb Shield", arm_xxe),
            ("NoSQL & MongoDB Injection Jail", arm_nosql_injection),
            ("Open Redirect & Phishing Boundary", arm_open_redirect),
            ("JWT Alg None & Signature Trap", arm_jwt_guard),
            ("Insecure Cryptography Enforcer", arm_insecure_crypto),
            ("YAML Object Gadget Defense", arm_yaml_gadget),
            ("DNS Rebinding & Subnet Enclosure", arm_dns_rebinding),
            ("Active Honeytoken & Canary Deception", arm_honeytoken)
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
            "version": self.version,
            "status": "ARMED" if self._armed else "DISARMED",
            "mode": self.mode.value,
            "active_shields_count": sum(1 for v in self.active_shields.values() if v),
            "total_shields_count": len(self.active_shields),
            "shields": self.active_shields,
            "blocked_attacks_count": len(self.telemetry)
        }

    def print_status(self):
        active = sum(1 for v in self.active_shields.values() if v)
        total = len(self.active_shields)
        sys.stderr.write(
            f"\033[92m[ZeroArmor v{self.version} Titanium]: Z+ Security Active ({active}/{total} Defense Layers Armed) [Mode: {self.mode.value}]\033[0m\n"
        )
        sys.stderr.flush()

    def export_telemetry_json(self, filepath: Optional[str] = None) -> str:
        data = json.dumps(self.telemetry, indent=2)
        if filepath:
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(data)
        return data

    def export_telemetry_cef(self, filepath: Optional[str] = None) -> str:
        lines = []
        for t in self.telemetry:
            event = ThreatEvent(rule=t["rule"], reason=t["reason"], payload=t.get("payload", ""), source=t.get("source", "local"))
            event.timestamp = t["timestamp"]
            lines.append(event.to_cef())
        cef_data = "\n".join(lines)
        if filepath:
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(cef_data)
        return cef_data

def get_shield() -> ZeroArmorCore:
    return ZeroArmorCore.get_instance()
