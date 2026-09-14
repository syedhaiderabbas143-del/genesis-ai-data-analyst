"""Controlled decommission policy for pre-v2 endpoints."""
import os
from starlette.responses import JSONResponse

LEGACY_PREFIXES = ("/upload", "/filter", "/ask", "/dashboard", "/export", "/api/", "/genesis/")

def legacy_routes_disabled() -> bool:
    return os.getenv("GENESIS_DISABLE_LEGACY_ROUTES", "false").lower() == "true"

def is_legacy_path(path: str) -> bool:
    return path == "/upload" or path.startswith(LEGACY_PREFIXES)

def legacy_decommission_response():
    return JSONResponse({"detail": "Legacy endpoint retired. Use the /v2 API."}, status_code=410)
