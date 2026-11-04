"""
ZeroArmor 🛡️ - 22-Vector Runtime Application Self-Protection (RASP) Library.
Just 'import zeroarmor' to immunize any Python application instantly.
Free Community Edition.
"""

__version__ = "1.0.0"
__author__ = "ZeroArmor Cyber Defense Labs"
__license__ = "Apache-2.0"

from .core import ZeroArmorCore, get_shield, ShieldBlockedException

# Singleton auto-arm on import!
_core = get_shield()
_core.auto_arm()

# Export clean helpers if developer wants manual controls
def status():
    """Return dictionary of active shields and blocked attack telemetry."""
    return _core.get_status()

def print_status():
    """Print high-contrast status banner in console."""
    _core.print_status()

def get_telemetry():
    """Return list of all blocked threat events."""
    return _core.telemetry

__all__ = ["status", "print_status", "get_telemetry", "ShieldBlockedException"]
