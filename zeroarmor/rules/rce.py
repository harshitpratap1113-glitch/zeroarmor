"""
Layer 2: RCE & Shell Jail Armor (Hardened Execution Boundary)
Hooks subprocess, os, and runtime process execution to neutralize shell injection chains,
download cradles, reverse shells, and destructive commands.
"""

import os
import re
import subprocess

DANGEROUS_CMD_REGEX = re.compile(
    r"(\|\s*(ba)?sh\b|"
    r"\|\s*powershell\b|"
    r";\s*rm\b|"
    r";\s*del\b|"
    r"&&\s*(rm|del|curl|wget|certutil)\b|"
    r";\s*(curl|wget|certutil)\b|"
    r"`.*?`|"
    r"\$\(.*?\)|"
    r"\bnc(\.exe)?\s+(-[el]|--exec)|"
    r"/bin/(ba)?sh|"
    r"/dev/tcp/\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}|"
    r"powershell(\.exe)?\s+(-e|-enc|-encodedcommand)\b|"
    r"(invoke-expression|iex)\s*[\(\{]|"
    r"downloadstring\s*\(|"
    r"rm\s+-rf\s+(/|\*)|"
    r"del\s+/[fF]\s+/[sS]|"
    r"mkfifo\s+/tmp/)",
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
            reason=f"Detected shell execution exploit chain or reverse shell payload: '{match.group(0)}'",
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

    # 2. Hook subprocess.run
    if hasattr(subprocess, "run"):
        orig_run = subprocess.run
        def armored_run(args, *pargs, **kwargs):
            inspect_cmd(args, core)
            return orig_run(args, *pargs, **kwargs)
        subprocess.run = armored_run

    # 3. Hook subprocess.call
    if hasattr(subprocess, "call"):
        orig_call = subprocess.call
        def armored_call(args, *pargs, **kwargs):
            inspect_cmd(args, core)
            return orig_call(args, *pargs, **kwargs)
        subprocess.call = armored_call

    # 4. Hook os.system
    if hasattr(os, "system"):
        orig_os_system = os.system
        def armored_os_system(command):
            inspect_cmd(command, core)
            return orig_os_system(command)
        os.system = armored_os_system

    # 5. Hook os.popen
    if hasattr(os, "popen"):
        orig_os_popen = os.popen
        def armored_os_popen(cmd, *pargs, **kwargs):
            inspect_cmd(cmd, core)
            return orig_os_popen(cmd, *pargs, **kwargs)
        os.popen = armored_os_popen
