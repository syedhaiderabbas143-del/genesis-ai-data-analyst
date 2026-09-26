"""JWT issuance/verification with persistent session (JTI) checks."""
from __future__ import annotations
import os, secrets
from datetime import datetime, timedelta, timezone
import jwt
from . import database

ALGORITHM='HS256'
def _secret():
    s=os.getenv('GENESIS_JWT_SECRET')
    if not s or len(s)<32: raise RuntimeError('GENESIS_JWT_SECRET must be set and at least 32 characters')
    return s

def issue_token(user_id, role, minutes=60):
    now=datetime.now(timezone.utc); exp=now+timedelta(minutes=minutes); jti=secrets.token_urlsafe(24)
    token=jwt.encode({'sub':user_id,'role':role,'jti':jti,'iat':int(now.timestamp()),'exp':exp},_secret(),algorithm=ALGORITHM)
    database.create_session(user_id,jti,exp.isoformat())
    return token

def decode_token(token):
    claims=jwt.decode(token,_secret(),algorithms=[ALGORITHM])
    if not database.session_valid(claims['jti'],claims['sub']): raise ValueError('Session is revoked or expired')
    return claims
