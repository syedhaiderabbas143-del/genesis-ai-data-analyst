"""FastAPI helpers for binding requests to an authenticated tenant."""
from __future__ import annotations

from fastapi import HTTPException, Request


def require_tenant(request: Request) -> str:
    """Read the authenticated user id set by the JWT authentication layer."""
    user_id = getattr(request.state, "user_id", None)
    if not user_id:
        raise HTTPException(status_code=401, detail="authenticated tenant required")
    return str(user_id)
