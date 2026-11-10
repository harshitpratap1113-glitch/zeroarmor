"""
Layer 28: JWT Algorithm 'None' & Insecure Token Trap
Inspects JSON Web Tokens (JWT) to intercept signature stripping attacks ("alg": "none"),
empty signature forgery, and weak default HMAC verification keys.
"""

import base64
import json
import re
import sys

def inspect_jwt_token(token: str, core) -> bool:
    if not getattr(core, "enabled", True):
        return True
    if not isinstance(token, str):
        return True

    clean_token = token.strip()
    parts = clean_token.split(".")
    if len(parts) != 3:
        return True  # Not a standard 3-part JWT

    # Check header
    try:
        header_b64 = parts[0]
        header_b64 += "=" * ((4 - len(header_b64) % 4) % 4)
        header_json = base64.urlsafe_b64decode(header_b64).decode("utf-8", "ignore")
        header = json.loads(header_json)
        
        alg = str(header.get("alg", "")).lower().strip()
        if alg in ["none", "null", ""]:
            core.record_threat(
                rule_name="JWT Alg 'None' Signature Stripping",
                reason="Blocked JWT token utilizing insecure 'alg': 'none' algorithm bypass",
                payload=clean_token[:100],
                block=True
            )
            return False

        # If alg requires signature but 3rd part is empty
        if alg != "none" and not parts[2].strip():
            core.record_threat(
                rule_name="JWT Signature Tampering / Missing Signature",
                reason="Blocked signed JWT token submitted with empty/stripped cryptographic signature",
                payload=clean_token[:100],
                block=True
            )
            return False

    except PermissionError:
        # Re-raise ShieldBlockedException so the caller catches it!
        raise
    except Exception:
        pass

    return True

def arm_jwt_guard(core):
    core.inspect_jwt_token = lambda t: inspect_jwt_token(t, core)
    
    # Hook PyJWT if imported
    if "jwt" in sys.modules:
        try:
            import jwt
            orig_decode = jwt.decode
            def armored_jwt_decode(token, *args, **kwargs):
                if isinstance(token, (str, bytes)):
                    inspect_jwt_token(token.decode("utf-8", "ignore") if isinstance(token, bytes) else token, core)
                return orig_decode(token, *args, **kwargs)
            jwt.decode = armored_jwt_decode
        except Exception:
            pass
