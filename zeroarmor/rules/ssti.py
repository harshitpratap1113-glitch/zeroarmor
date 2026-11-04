"""
Layer 13: SSTI (Server-Side Template Injection) Guard
Hooks Jinja2 template initialization to block sandbox escapes and arbitrary execution.
"""

import re
import sys

SSTI_EXPLOIT_PATTERN = re.compile(
    r"(\{\{.*?(__class__|__mro__|__subclasses__|__globals__|lipsum|cycler|joiner|namespace|config\.).*?\}\}|"
    r"\{%.*?(__class__|__mro__|__globals__|import).*?%\})",
    re.IGNORECASE
)

def inspect_template_source(source: str, core) -> bool:
    if isinstance(source, str) and SSTI_EXPLOIT_PATTERN.search(source):
        core.record_threat(
            rule_name="Server-Side Template Injection (SSTI)",
            reason="Blocked Jinja2 template containing Python sandbox escape gadgets",
            payload=source[:120],
            block=True
        )
        return False
    return True

def arm_ssti(core):
    if "jinja2" in sys.modules:
        try:
            import jinja2
            orig_from_string = jinja2.Environment.from_string
            def armored_from_string(self, source, *args, **kwargs):
                inspect_template_source(source, core)
                return orig_from_string(self, source, *args, **kwargs)
            jinja2.Environment.from_string = armored_from_string
        except Exception:
            pass
