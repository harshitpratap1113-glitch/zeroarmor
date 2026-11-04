"""
Layer 2: RCE & Shell Jail Armor
Hooks subprocess and os command functions to block command injection chains and reverse shells.
"""

import os
import re
import subprocess

DANGEROUS_CMD_REGEX = re.compile(
    r"(\|\s*bash\b|"
    r"\|\s*sh\b|"
    r";\s*rm\b|"
    r"&&\s*curl\b|"
    r"&&\s*wget\b|"
    r";\s*wget\b|"
    r";\s*curl\b|"
    r"`.*?`|"
    r"\$\(.*?\)|"
    r"\bnc\s+-[el]|"
    r"/bin/(ba)?sh|"
    r"cmd\.exe\s+/c\s*calc|"
    r"powershell(\.exe)?\s+(-e|-enc|-encodedcommand))",
    re.IGNORECASE
)

def inspect_cmd(cmd, core) -> bool:
    if not getattr(core, "enabled", True):
        return True
    if isinstance(cmd, (list, tuple)):
        cmd_str = " ".join(str(c) for c in cmd)
    else:
        cmd_str = str(cmd)

    match = DANGEROUS_CMD_REGEX.search(cmd_str)
    if match:
        core.record_threat(
            rule_name="Command Injection (RCE)",
            reason=f"Detected shell execution exploit chain: '{match.group(0)}'",
            payload=cmd_str,
            block=True
        )
        return False
    return True

def arm_rce(core):
    # 1. Hook subprocess.Popen
    orig_popen = subprocess.Popen
    def armored_popen(args, *pargs, **kwargs):
        inspect_cmd(args, core)
        return orig_popen(args, *pargs, **kwargs)
    subprocess.Popen = armored_popen

    # 2. Hook os.system
    if hasattr(os, "system"):
        orig_os_system = os.system
        def armored_os_system(command):
            inspect_cmd(command, core)
            return orig_os_system(command)
        os.system = armored_os_system

    # 3. Hook os.popen
    if hasattr(os, "popen"):
        orig_os_popen = os.popen
        def armored_os_popen(cmd, *pargs, **kwargs):
            inspect_cmd(cmd, core)
            return orig_os_popen(cmd, *pargs, **kwargs)
        os.popen = armored_os_popen
