"""FastAPI authentication and role dependencies."""
from fastapi import Header, HTTPException, status, Depends
from .jwt_auth import decode_token

def current_user(authorization: str | None = Header(default=None)):
    if not authorization or not authorization.lower().startswith('bearer '):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Bearer token required')
    try: return decode_token(authorization.split(' ',1)[1].strip())
    except Exception: raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid or expired session')

def require_role(*roles):
    def dep(user=Depends(current_user)):
        if user.get('role') not in roles: raise HTTPException(status_code=403, detail='Insufficient role')
        return user
    return dep
