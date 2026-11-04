"""
Layer 19: Insecure CORS Wildcard Guard
Inspects response headers to prevent dangerous wildcard origins combined with credentials.
"""

def inspect_cors_headers(headers: dict, core) -> bool:
    origin = headers.get("Access-Control-Allow-Origin") or headers.get("access-control-allow-origin")
    credentials = headers.get("Access-Control-Allow-Credentials") or headers.get("access-control-allow-credentials")

    if origin == "*" and str(credentials).lower() == "true":
        core.record_threat(
            rule_name="Insecure CORS Wildcard with Credentials",
            reason="Detected critical CORS vulnerability: 'Access-Control-Allow-Origin: *' with credentials allowed",
            payload="CORS Misconfiguration",
            block=True
        )
        return False
    return True

def arm_cors(core):
    core.inspect_cors_headers = lambda h: inspect_cors_headers(h, core)
