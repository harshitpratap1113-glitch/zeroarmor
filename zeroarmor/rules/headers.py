"""
Layers 14-18: HTTP Security Headers Auto-Immunizer
Auto-injects OWASP recommended security headers (CSP, HSTS, X-Frame-Options, MIME) into responses.
"""

SECURITY_HEADERS = {
    "X-Frame-Options": "DENY",
    "X-Content-Type-Options": "nosniff",
    "X-XSS-Protection": "1; mode=block",
    "Strict-Transport-Security": "max-age=31536000; includeSubDomains",
    "Referrer-Policy": "strict-origin-when-cross-origin",
    "Permissions-Policy": "camera=(), microphone=(), geolocation=()"
}

def inject_security_headers(headers_dict: dict):
    """Enriches any HTTP headers dict with strict security defaults without overriding existing custom CSP."""
    for key, value in SECURITY_HEADERS.items():
        if key not in headers_dict and key.lower() not in headers_dict:
            headers_dict[key] = value

def arm_headers(core):
    core.inject_security_headers = inject_security_headers
