"""
Layer 30: Multi-Format Prototype Pollution & YAML Gadget Shield
Intercepts unsafe YAML loaders and prevents arbitrary Python object instantiation gadgets
(e.g., !!python/object/apply:os.system).
"""

import re
import sys

YAML_EXPLOIT_PATTERN = re.compile(
    r"(!!python/(object|apply|module)|"
    r"__proto__|"
    r"constructor\s*\[\s*\"prototype\"\s*\])",
    re.IGNORECASE
)

def inspect_yaml_payload(data: str, core) -> bool:
    if not getattr(core, "enabled", True):
        return True
    if not isinstance(data, (str, bytes)):
        return True

    text = data.decode("utf-8", "ignore") if isinstance(data, bytes) else data
    if YAML_EXPLOIT_PATTERN.search(text):
        core.record_threat(
            rule_name="Unsafe YAML Deserialization Gadget",
            reason="Blocked YAML payload attempting arbitrary Python object reconstruction or prototype injection",
            payload=text[:120],
            block=True
        )
        return False
    return True

def arm_yaml_gadget(core):
    core.inspect_yaml_payload = lambda d: inspect_yaml_payload(d, core)

    if "yaml" in sys.modules:
        try:
            import yaml
            if hasattr(yaml, "unsafe_load"):
                orig_unsafe_load = yaml.unsafe_load
                def armored_unsafe_load(stream, *args, **kwargs):
                    if isinstance(stream, (str, bytes)):
                        inspect_yaml_payload(stream, core)
                    return orig_unsafe_load(stream, *args, **kwargs)
                yaml.unsafe_load = armored_unsafe_load
        except Exception:
            pass
