"""Small in-process rate limiter for single-process development deployments.
For production, replace with Redis/API-gateway based limiting.
"""
from collections import defaultdict, deque
from time import monotonic
from threading import Lock
from fastapi import Request, HTTPException

class InMemoryRateLimiter:
    def __init__(self, limit: int = 60, window_seconds: int = 60):
        self.limit = limit
        self.window_seconds = window_seconds
        self._hits = defaultdict(deque)
        self._lock = Lock()

    def check(self, key: str) -> None:
        now = monotonic()
        with self._lock:
            q = self._hits[key]
            while q and now - q[0] >= self.window_seconds:
                q.popleft()
            if len(q) >= self.limit:
                raise HTTPException(status_code=429, detail="Rate limit exceeded")
            q.append(now)

limiter = InMemoryRateLimiter()

def rate_limit_dependency(request: Request):
    client = request.client.host if request.client else "unknown"
    limiter.check(client)
