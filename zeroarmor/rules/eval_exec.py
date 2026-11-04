"""
Layer 6: Code Injection (eval/exec) Sandbox
Hooks builtins.eval and builtins.exec to stop dynamic Python code injection attacks.
"""

import builtins
import re

EVAL_EXPLOIT_PATTERN = re.compile(
    r"(__import__|__builtins__|__subclasses__|subprocess|os\.system|os\.popen|builtins\.|importlib)",
    re.IGNORECASE
)

def inspect_code_string(source, core) -> bool:
    if isinstance(source, str):
        if EVAL_EXPLOIT_PATTERN.search(source):
            core.record_threat(
                rule_name="Dynamic Code Injection (eval/exec)",
                reason="Blocked execution of dangerous runtime Python payload accessing system internals",
                payload=source[:100],
                block=True
            )
            return False
    return True

def arm_eval_exec(core):
    orig_eval = builtins.eval
    orig_exec = builtins.exec

    def armored_eval(source, *args, **kwargs):
        inspect_code_string(source, core)
        return orig_eval(source, *args, **kwargs)

    def armored_exec(source, *args, **kwargs):
        inspect_code_string(source, core)
        return orig_exec(source, *args, **kwargs)

    builtins.eval = armored_eval
    builtins.exec = armored_exec
