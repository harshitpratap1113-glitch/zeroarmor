"""
ZeroArmor Universal Web Middleware & Framework Auto-Wrapper
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
            path = scope.get("path", "")
            
            # 1. Honeypot check
            if hasattr(self.core, "deception"):
                if not self.core.deception.check_honeypot_path(path, client_ip, self.core):
                    async def send_403(s):
                        await send({
                            "type": "http.response.start",
                            "status": 403,
                            "headers": [(b"content-type", b"text/plain")]
                        })
                        await send({
                            "type": "http.response.body",
                            "body": b"403 Forbidden - Access Denied by ZeroArmor Honeypot Trap"
                        })
                    return await send_403(send)

            # 2. Rate Limiting Check
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
                            "body": b"429 Too Many Requests - Blocked by ZeroArmor Rate Limiter"
                        })
                    return await send_429(send)

            # 3. Intercept response to inject security headers & scan for DLP
            async def armored_send(message):
                if message["type"] == "http.response.start":
                    headers = dict(message.get("headers", []))
                    str_headers = {k.decode("latin1"): v.decode("latin1") for k, v in headers.items()}
                    inject_security_headers(str_headers)
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

    # WSGI Support (Flask / Django)
    def __call__(self, environ, start_response):
        client_ip = environ.get("REMOTE_ADDR", "127.0.0.1")
        path = environ.get("PATH_INFO", "")

        # Honeypot check
        if hasattr(self.core, "deception"):
            if not self.core.deception.check_honeypot_path(path, client_ip, self.core):
                start_response("403 Forbidden", [("Content-Type", "text/plain")])
                return [b"403 Forbidden - Access Denied by ZeroArmor Honeypot Trap"]

        # Rate limiter check
        if hasattr(self.core, "rate_limiter"):
            if not self.core.rate_limiter.is_allowed(client_ip, self.core):
                start_response("429 Too Many Requests", [("Content-Type", "text/plain")])
                return [b"429 Too Many Requests - Blocked by ZeroArmor Rate Limiter"]

        def armored_start_response(status, response_headers, exc_info=None):
            headers_dict = dict(response_headers)
            inject_security_headers(headers_dict)
            new_headers = list(headers_dict.items())
            return start_response(status, new_headers, exc_info)

        response = self.app(environ, armored_start_response)

        # Inspect DLP on response body
        if hasattr(self.core, "inspect_outbound_data"):
            def wrapped_response():
                for chunk in response:
                    if isinstance(chunk, bytes):
                        try:
                            text = chunk.decode("utf-8", "ignore")
                            self.core.inspect_outbound_data(text)
                        except ShieldBlockedException:
                            yield b"[ZeroArmor DLP Alert: Outbound Sensitive Data Leak Blocked]"
                            continue
                    yield chunk
            return wrapped_response()

        return response

def shield_app(app):
    """1-Line Framework Auto-Wrapper for FastAPI, Flask, Django, Starlette."""
    # Check if Flask app
    if hasattr(app, "wsgi_app"):
        app.wsgi_app = ZeroArmorMiddleware(app.wsgi_app)
        return app
    return ZeroArmorMiddleware(app)
