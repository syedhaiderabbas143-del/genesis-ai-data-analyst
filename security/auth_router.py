"""Authentication endpoints: register, login, me, logout."""
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from . import database
from .passwords import hash_password, verify_password
from .jwt_auth import issue_token
from .dependencies import current_user

router=APIRouter(prefix='/auth',tags=['authentication'])
class Credentials(BaseModel):
    username: str = Field(min_length=3,max_length=80,pattern=r'^[A-Za-z0-9_.-]+$')
    password: str = Field(min_length=12,max_length=256)

@router.post('/register')
def register(body: Credentials):
    database.init_db()
    if database.get_user(body.username): raise HTTPException(409,'Username already exists')
    uid=database.create_user(body.username,hash_password(body.password),'analyst')
    return {'success':True,'user_id':uid,'role':'analyst'}

@router.post('/login')
def login(body: Credentials):
    database.init_db(); u=database.get_user(body.username)
    if not u or u['disabled'] or not verify_password(body.password,u['password_hash']): raise HTTPException(401,'Invalid credentials')
    return {'access_token':issue_token(u['id'],u['role']),'token_type':'bearer','role':u['role']}

@router.get('/me')
def me(user=Depends(current_user)):
    u=database.get_user_by_id(user['sub']); return {'user_id':u['id'],'username':u['username'],'role':u['role']}

@router.post('/logout')
def logout(user=Depends(current_user)):
    database.revoke_session(user['jti']); return {'success':True}
