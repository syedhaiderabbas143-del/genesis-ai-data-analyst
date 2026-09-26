"""Optional API-key authentication foundation.
Set GENESIS_API_KEY to enable protection for selected routes.
"""
import os
from fastapi import Header, HTTPException, status

def require_api_key(x_api_key: str | None = Header(default=None)) -> str:
    expected = os.getenv("GENESIS_API_KEY")
    if not expected:
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail="Authentication is not configured")
    if not x_api_key or x_api_key != expected:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or missing API key")
    return x_api_key
