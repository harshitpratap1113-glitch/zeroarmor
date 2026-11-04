"""
Layer 3: Path Traversal Prison
Hooks file open operations to intercept directory traversal and unauthorized path escapes.
"""

import builtins
import os
import re
from pathlib import Path

TRAVERSAL_REGEX = re.compile(
    r"(\.\.[/\\]|"
    r"%2e%2e|"
    r"(/etc/(passwd|shadow|hosts))|"
    r"([cC]:\\windows\\system32)|"
    r"(\x00|%00))",
    re.IGNORECASE
)

def inspect_filepath(filepath, core) -> bool:
    if not getattr(core, "enabled", True):
        return True
    if not isinstance(filepath, (str, bytes, os.PathLike)):
        return True

    path_str = str(filepath)
    if TRAVERSAL_REGEX.search(path_str):
        core.record_threat(
            rule_name="Path Traversal (LFI)",
            reason=f"Detected directory traversal escape pattern in path: {path_str}",
            payload=path_str,
            block=True
        )
        return False
    return True

def arm_path_traversal(core):
    orig_open = builtins.open

    def armored_open(file, *args, **kwargs):
        inspect_filepath(file, core)
        return orig_open(file, *args, **kwargs)

    builtins.open = armored_open
