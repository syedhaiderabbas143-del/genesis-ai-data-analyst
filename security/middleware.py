"""Opt-in route security middleware for the Genesis AI Data Analyst API."""
import os
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse
from .auth import require_api_key
from .rate_limit import limiter
from .legacy_routes import legacy_routes_disabled, is_legacy_path, legacy_decommission_response

SENSITIVE_PREFIXES = ("/upload", "/ask", "/filter", "/dashboard", "/charts", "/correlation", "/forecast", "/report")

class RouteSecurityMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        if legacy_routes_disabled() and is_legacy_path(request.url.path):
            return legacy_decommission_response()
        if os.getenv("GENESIS_SECURITY_ENFORCED", "false").lower() != "true":
            return await call_next(request)
        path = request.url.path
        if path.startswith(SENSITIVE_PREFIXES):
            client = request.client.host if request.client else "unknown"
            try:
                limiter.check(client)
            except Exception as exc:
                if getattr(exc, "status_code", None) == 429:
                    return JSONResponse({"detail": "Rate limit exceeded"}, status_code=429)
                raise
            expected = os.getenv("GENESIS_API_KEY")
            supplied = request.headers.get("x-api-key")
            if not expected:
                return JSONResponse({"detail": "Authentication is not configured"}, status_code=503)
            if not supplied or supplied != expected:
                return JSONResponse({"detail": "Invalid or missing API key"}, status_code=401)
        return await call_next(request)
