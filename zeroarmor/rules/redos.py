"""
Layer 8: ReDoS Catastrophic Backtracking Guard
Hooks re.compile to detect vulnerable evil regex patterns causing CPU denial-of-service.
"""

import re

EVIL_REGEX_PATTERN = re.compile(
    r"(\(.*?[+*]\)[+*]|"          # Nested quantifiers like (a+)+
    r"\(.*?[+*]\|.*?[+*]\)[+*]|"  # Overlapping alternatives like (a+|b+)+
    r"\\w\+.*?\\w\+\$)",          # Repeated wildcards without anchors
    re.IGNORECASE
)

def inspect_regex_pattern(pattern, core) -> bool:
    if isinstance(pattern, (str, bytes)):
        p_str = pattern.decode("utf-8", "ignore") if isinstance(pattern, bytes) else pattern
        # If it matches obvious nested quantifier explosive pattern
        if EVIL_REGEX_PATTERN.search(p_str) and len(p_str) < 50:
            core.record_threat(
                rule_name="ReDoS Catastrophic Backtracking",
                reason=f"Detected potentially explosive regex pattern causing CPU freeze: {p_str}",
                payload=p_str,
                block=True
            )
            return False
    return True

def arm_redos(core):
    orig_compile = re.compile

    def armored_compile(pattern, *args, **kwargs):
        inspect_regex_pattern(pattern, core)
        return orig_compile(pattern, *args, **kwargs)

    re.compile = armored_compile
