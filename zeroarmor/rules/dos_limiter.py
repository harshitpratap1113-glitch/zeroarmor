"""
Layer 9: Memory Bomb & DoS Limiter
Enforces maximum payload and memory allocation thresholds to prevent Out-Of-Memory (OOM) crashes.
"""

MAX_PAYLOAD_BYTES = 10 * 1024 * 1024 # 10 MB default limit

def check_payload_size(size_in_bytes: int, core) -> bool:
    if size_in_bytes > MAX_PAYLOAD_BYTES:
        core.record_threat(
            rule_name="Memory Bomb / DoS Payload",
            reason=f"Incoming payload ({size_in_bytes} bytes) exceeds maximum security threshold (10MB)",
            payload=f"Payload size: {size_in_bytes} bytes",
            block=True
        )
        return False
    return True

def arm_dos_limiter(core):
    # Registered into core for ASGI/WSGI middleware and internal stream reads
    core.check_payload_size = lambda sz: check_payload_size(sz, core)
