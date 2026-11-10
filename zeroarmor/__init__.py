"""
ZeroArmor 🛡️ - 32-Vector Titanium Runtime Application Self-Protection (RASP) Library.
Just 'import zeroarmor' to immunize any Python application instantly.
Version 2.0.0 Titanium Edition.
"""

__version__ = "2.0.0"
__author__ = "ZeroArmor Cyber Defense Labs"
__license__ = "Apache-2.0"

from .core import ZeroArmorCore, get_shield, ShieldBlockedException, DefenseMode
from .middleware import ZeroArmorMiddleware, shield_app

# Singleton auto-arm on import!
_core = get_shield()
_core.auto_arm()

# Export clean helpers for developers
def status():
    """Return dictionary of active shields and blocked attack telemetry."""
    return _core.get_status()

def print_status():
    """Print high-contrast status banner in console."""
    _core.print_status()

def get_telemetry():
    """Return list of all blocked threat events."""
    return _core.telemetry

def export_telemetry_json(filepath=None):
    """Export telemetry events as JSON."""
    return _core.export_telemetry_json(filepath)

def export_telemetry_cef(filepath=None):
    """Export telemetry events in SIEM Common Event Format (CEF)."""
    return _core.export_telemetry_cef(filepath)

def set_mode(mode: DefenseMode):
    """Set active defense mode (BLOCK, AUDIT, DECEIVE)."""
    _core.set_mode(mode)

def set_webhook(url: str):
    """Configure outbound security alert webhook."""
    _core.set_webhook(url)

# Vector inspection hooks for custom security assertions
def inspect_prompt(text: str) -> bool:
    if hasattr(_core, "inspect_prompt"):
        return _core.inspect_prompt(text)
    return True

def inspect_graphql_query(query: str) -> bool:
    if hasattr(_core, "inspect_graphql_query"):
        return _core.inspect_graphql_query(query)
    return True

def inspect_nosql_input(data) -> bool:
    if hasattr(_core, "inspect_nosql_input"):
        return _core.inspect_nosql_input(data)
    return True

def inspect_redirect_url(url: str) -> bool:
    if hasattr(_core, "inspect_redirect_url"):
        return _core.inspect_redirect_url(url)
    return True

def inspect_jwt_token(token: str) -> bool:
    if hasattr(_core, "inspect_jwt_token"):
        return _core.inspect_jwt_token(token)
    return True

__all__ = [
    "status",
    "print_status",
    "get_telemetry",
    "export_telemetry_json",
    "export_telemetry_cef",
    "set_mode",
    "set_webhook",
    "DefenseMode",
    "ShieldBlockedException",
    "ZeroArmorMiddleware",
    "shield_app",
    "inspect_prompt",
    "inspect_graphql_query",
    "inspect_nosql_input",
    "inspect_redirect_url",
    "inspect_jwt_token"
]
