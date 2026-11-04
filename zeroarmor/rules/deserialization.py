"""
Layer 5: Deserialization Sanitizer
Hooks pickle, _pickle, and yaml to block arbitrary object reconstruction and RCE gadgets.
"""

import pickle
import sys
import re

PICKLE_RCE_PATTERN = re.compile(
    b"(posix|nt|os|subprocess|builtins|eval|exec|system|popen)",
    re.IGNORECASE
)

def inspect_pickle_data(data: bytes, core) -> bool:
    if not isinstance(data, (bytes, bytearray)):
        return True

    if PICKLE_RCE_PATTERN.search(data):
        core.record_threat(
            rule_name="Insecure Deserialization (Pickle RCE)",
            reason="Blocked untrusted pickle payload containing system/os execution gadgets",
            payload=str(data[:60]),
            block=True
        )
        return False
    return True

def arm_deserialization(core):
    # Hook standard pickle
    orig_pickle_loads = pickle.loads
    def armored_pickle_loads(data, *args, **kwargs):
        inspect_pickle_data(data, core)
        return orig_pickle_loads(data, *args, **kwargs)
    pickle.loads = armored_pickle_loads

    # Hook _pickle if available
    if "_pickle" in sys.modules:
        try:
            import _pickle
            orig__pickle_loads = _pickle.loads
            def armored__pickle_loads(data, *args, **kwargs):
                inspect_pickle_data(data, core)
                return orig__pickle_loads(data, *args, **kwargs)
            _pickle.loads = armored__pickle_loads
        except Exception:
            pass

    # Hook yaml if present to force safe_load
    if "yaml" in sys.modules:
        try:
            import yaml
            if hasattr(yaml, "load"):
                orig_yaml_load = yaml.load
                def armored_yaml_load(stream, Loader=None):
                    if Loader is None or Loader == getattr(yaml, "Loader", None):
                        Loader = getattr(yaml, "SafeLoader", None)
                    return orig_yaml_load(stream, Loader=Loader)
                yaml.load = armored_yaml_load
        except Exception:
            pass
