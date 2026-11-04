"""
Layer 12: Secure Temp File Enforcer
Hooks tempfile.mktemp to eliminate insecure TOCTOU temporary file race conditions.
"""

import tempfile

def arm_temp_file(core):
    if hasattr(tempfile, "mktemp"):
        orig_mktemp = tempfile.mktemp

        def armored_mktemp(*args, **kwargs):
            core.record_threat(
                rule_name="Insecure Temp File Race Condition (mktemp)",
                reason="mktemp() called; redirected to cryptographically secure NamedTemporaryFile",
                payload="tempfile.mktemp invocation",
                block=False
            )
            # Create securely and return filename
            with tempfile.NamedTemporaryFile(delete=False) as f:
                return f.name

        tempfile.mktemp = armored_mktemp
