"""
ZeroArmor Universal Web Middleware
Compatible with ASGI (FastAPI / Starlette) and WSGI (Flask / Django).
"""

from .core import get_shield, ShieldBlockedException
from .rules.headers import inject_security_headers

class ZeroArmorMiddleware:
    """Universal ASGI & WSGI Middleware."""
    def __init__(self, app):
        self.app = app
        self.core = get_shield()

    # ASGI Support (FastAPI / Starlette)
    async def __call__(self, scope, receive, send):
        if scope["type"] == "http":
            client_ip = scope.get("client", ("127.0.0.1", 0))[0]
            
            # 1. Rate Limiting Check
            if hasattr(self.core, "rate_limiter"):
                if not self.core.rate_limiter.is_allowed(client_ip, self.core):
                    async def send_429(s):
                        await send({
                            "type": "http.response.start",
                            "status": 429,
                            "headers": [(b"content-type", b"text/plain")]
                        })
                        await send({
                            "type": "http.response.body",
                            "body": b"429 Too Many Requests - Blocked by ZeroArmor"
                        })
                    return await send_429(send)

            # 2. Intercept response to inject security headers & scan for DLP
            async def armored_send(message):
                if message["type"] == "http.response.start":
                    headers = dict(message.get("headers", []))
                    # Convert to str dict
                    str_headers = {k.decode("latin1"): v.decode("latin1") for k, v in headers.items()}
                    inject_security_headers(str_headers)
                    # Convert back
                    message["headers"] = [(k.encode("latin1"), v.encode("latin1")) for k, v in str_headers.items()]
                elif message["type"] == "http.response.body":
                    body_bytes = message.get("body", b"")
                    if hasattr(self.core, "inspect_outbound_data") and body_bytes:
                        try:
                            text = body_bytes.decode("utf-8", "ignore")
                            self.core.inspect_outbound_data(text)
                        except ShieldBlockedException:
                            message["body"] = b"[ZeroArmor DLP Alert: Outbound Sensitive Data Leak Blocked]"

                await send(message)

            return await self.app(scope, receive, armored_send)
        else:
            return await self.app(scope, receive, send)
