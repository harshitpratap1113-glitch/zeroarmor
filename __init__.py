"""
ZeroArmor root module alias - v2.0 Titanium Edition
"""

from .zeroarmor import (
    status,
    print_status,
    get_telemetry,
    export_telemetry_json,
    export_telemetry_cef,
    set_mode,
    set_webhook,
    DefenseMode,
    ShieldBlockedException,
    ZeroArmorCore,
    get_shield,
    ZeroArmorMiddleware,
    shield_app,
    inspect_prompt,
    inspect_graphql_query,
    inspect_nosql_input,
    inspect_redirect_url,
    inspect_jwt_token
)

__version__ = "2.0.0"

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
    "ZeroArmorCore",
    "get_shield",
    "ZeroArmorMiddleware",
    "shield_app",
    "inspect_prompt",
    "inspect_graphql_query",
    "inspect_nosql_input",
    "inspect_redirect_url",
    "inspect_jwt_token"
]
