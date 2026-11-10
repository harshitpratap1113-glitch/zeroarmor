"""
Layer 29: Insecure Cryptography & Deprecated Hash Enforcer
Hooks hashlib to intercept deprecated and broken hashing algorithms (MD5, SHA1)
when utilized in security-sensitive or password-related contexts.
"""

import hashlib

def arm_insecure_crypto(core):
    orig_md5 = hashlib.md5
    orig_sha1 = hashlib.sha1

    def armored_md5(*args, **kwargs):
        # Python 3.9+ supports usedforsecurity flag
        used_for_security = kwargs.get("usedforsecurity", True)
        if used_for_security is False:
            return orig_md5(*args, **kwargs)
            
        core.record_threat(
            rule_name="Insecure Cryptographic Hash (MD5)",
            reason="Detected invocation of collision-vulnerable MD5 algorithm for security context; upgrade to SHA-256",
            payload="hashlib.md5() invocation",
            block=False  # Record threat and warn without crashing legacy checksum utilities
        )
        return orig_md5(*args, **kwargs)

    def armored_sha1(*args, **kwargs):
        used_for_security = kwargs.get("usedforsecurity", True)
        if used_for_security is False:
            return orig_sha1(*args, **kwargs)
            
        core.record_threat(
            rule_name="Insecure Cryptographic Hash (SHA1)",
            reason="Detected invocation of collision-vulnerable SHA1 algorithm for security context; upgrade to SHA-256",
            payload="hashlib.sha1() invocation",
            block=False
        )
        return orig_sha1(*args, **kwargs)

    hashlib.md5 = armored_md5
    hashlib.sha1 = armored_sha1
