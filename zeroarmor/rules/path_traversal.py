"""
Layer 3: Path Traversal Prison & Sensitive File Boundary
Hooks file open operations to intercept directory traversal and unauthorized path escapes.
"""

import builtins
import os
import re

TRAVERSAL_REGEX = re.compile(
    r"(\.\.[/\\]|"
    r"%2e%2e|"
    r"(/etc/(passwd|shadow|hosts|issue|sudoers))|"
    r"([cC]:\\windows\\(system32|win\.ini|boot\.ini))|"
    r"/proc/self/|"
    r"(\x00|%00))",
    re.IGNORECASE
)

def inspect_filepath(filepath, core) -> bool:
    if not getattr(core, "enabled", True):
        return True
    if not isinstance(filepath, (str, bytes, os.PathLike)):
        return True

    path_str = str(filepath)
    
    # 1. Directory traversal pattern check
    if TRAVERSAL_REGEX.search(path_str):
        core.record_threat(
            rule_name="Path Traversal (LFI)",
            reason=f"Detected directory traversal escape pattern in path: {path_str}",
            payload=path_str,
            block=True
        )
        return False
        
    # 2. Direct sensitive file (.env, SSH keys, credentials) access check
    if hasattr(core, "inspect_sensitive_access"):
        if not core.inspect_sensitive_access(path_str):
            return False

    return True

def arm_path_traversal(core):
    orig_open = builtins.open

    def armored_open(file, *args, **kwargs):
        inspect_filepath(file, core)
        return orig_open(file, *args, **kwargs)

    builtins.open = armored_open
