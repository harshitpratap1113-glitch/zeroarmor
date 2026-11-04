"""
Layer 7: Real-Time Secret & Token Scrubber
Hooks stdout, stderr, and logging streams to scrub API keys, tokens, and passwords from logs.
Safe against Windows cp1252 character map errors.
"""

import re
import sys

SECRET_PATTERNS = [
    (re.compile(r"sk_(live|test)_[0-9a-zA-Z_]{16,}"), "[MASKED_STRIPE_SECRET_KEY]"),
    (re.compile(r"AKIA[0-9A-Z]{16}"), "[MASKED_AWS_ACCESS_KEY]"),
    (re.compile(r"ghp_[0-9a-zA-Z]{36}"), "[MASKED_GITHUB_TOKEN]"),
    (re.compile(r"AIza[0-9A-Za-z\-_]{35}"), "[MASKED_GOOGLE_API_KEY]"),
    (re.compile(r"xox[baprs]-[0-9a-zA-Z]{10,48}"), "[MASKED_SLACK_TOKEN]"),
    (re.compile(r"-----BEGIN (RSA|EC|DSA|OPENSSH) PRIVATE KEY-----"), "[MASKED_PRIVATE_SSH_KEY]"),
    (re.compile(r"eyJ[A-Za-z0-9-_=]{10,}\.eyJ[A-Za-z0-9-_=]{10,}\.[A-Za-z0-9-_.+/=]{10,}"), "[MASKED_JWT_TOKEN]")
]

def scrub_text(text: str, core) -> str:
    if not getattr(core, "enabled", True):
        return text
    if not isinstance(text, str):
        return text

    scrubbed = text
    found_secret = False
    for pattern, mask in SECRET_PATTERNS:
        if pattern.search(scrubbed):
            found_secret = True
            scrubbed = pattern.sub(mask, scrubbed)

    if found_secret:
        core.record_threat(
            rule_name="Secret Leakage Scrubber",
            reason="Sanitized live sensitive token/secret before writing to stdout/logs",
            payload="Sensitive token pattern scrubbed",
            block=False
        )
    return scrubbed

class ArmoredStream:
    def __init__(self, original_stream, core):
        self._orig = original_stream
        self._core = core

    def write(self, s):
        clean_s = scrub_text(s, self._core)
        try:
            return self._orig.write(clean_s)
        except UnicodeEncodeError:
            encoding = getattr(self._orig, "encoding", "utf-8") or "utf-8"
            safe_bytes = clean_s.encode(encoding, errors="replace")
            return self._orig.write(safe_bytes.decode(encoding, errors="ignore"))

    def flush(self):
        return self._orig.flush()

    def __getattr__(self, name):
        return getattr(self._orig, name)

def arm_secret_scrubber(core):
    sys.stdout = ArmoredStream(sys.stdout, core)
    sys.stderr = ArmoredStream(sys.stderr, core)
