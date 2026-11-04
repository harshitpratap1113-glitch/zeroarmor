"""
Layer 22: Anti-Bot & In-Memory Rate Limiter
Token bucket rate-limiter per client IP to stop automated brute-force attacks and scrapers.
"""

import time
from typing import Dict, Tuple

class TokenBucketRateLimiter:
    def __init__(self, capacity: int = 60, refill_rate: float = 1.0):
        self.capacity = capacity
        self.refill_rate = refill_rate # tokens per second
        self.buckets: Dict[str, Tuple[float, float]] = {}

    def is_allowed(self, client_id: str, core) -> bool:
        now = time.time()
        tokens, last_update = self.buckets.get(client_id, (self.capacity, now))

        # Refill tokens
        elapsed = now - last_update
        tokens = min(self.capacity, tokens + elapsed * self.refill_rate)

        if tokens >= 1.0:
            self.buckets[client_id] = (tokens - 1.0, now)
            return True
        else:
            self.buckets[client_id] = (tokens, now)
            core.record_threat(
                rule_name="Anti-Bot Rate Limit Exceeded",
                reason=f"Client IP '{client_id}' exceeded maximum request burst threshold",
                payload=client_id,
                block=True
            )
            return False

_limiter = TokenBucketRateLimiter()

def arm_rate_limiter(core):
    core.rate_limiter = _limiter
