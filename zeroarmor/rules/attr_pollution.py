"""
Layer 10: Class Attribute Pollution Freeze
Hooks json.loads and object parsers to stop Python attribute tampering (__class__, __globals__, __proto__).
"""

import json
import re

POLLUTION_PATTERN = re.compile(
    r'("(__class__|__globals__|__subclasses__|__code__|__proto__|constructor)")',
    re.IGNORECASE
)

def inspect_json_string(s: str, core) -> bool:
    if isinstance(s, (str, bytes)):
        s_str = s.decode("utf-8", "ignore") if isinstance(s, bytes) else s
        match = POLLUTION_PATTERN.search(s_str)
        if match:
            core.record_threat(
                rule_name="Class Attribute Pollution",
                reason=f"Detected attempted Python object hierarchy tampering: {match.group(0)}",
                payload=s_str[:100],
                block=True
            )
            return False
    return True

def arm_attr_pollution(core):
    orig_json_loads = json.loads

    def armored_json_loads(s, *args, **kwargs):
        inspect_json_string(s, core)
        return orig_json_loads(s, *args, **kwargs)

    json.loads = armored_json_loads
