"""Persistent security/session store backed by SQLite."""
from __future__ import annotations
import os, sqlite3, secrets
from pathlib import Path
from datetime import datetime, timezone

DB_PATH = Path(os.getenv("GENESIS_SECURITY_DB", "genesis_security.sqlite3"))

def _conn():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    c = sqlite3.connect(DB_PATH, check_same_thread=False)
    c.row_factory = sqlite3.Row
    return c

def init_db():
    with _conn() as c:
        c.executescript('''
        CREATE TABLE IF NOT EXISTS users (
          id TEXT PRIMARY KEY, username TEXT UNIQUE NOT NULL, password_hash TEXT NOT NULL,
          role TEXT NOT NULL DEFAULT 'analyst', created_at TEXT NOT NULL, disabled INTEGER NOT NULL DEFAULT 0
        );
        CREATE TABLE IF NOT EXISTS sessions (
          jti TEXT PRIMARY KEY, user_id TEXT NOT NULL, expires_at TEXT NOT NULL,
          revoked INTEGER NOT NULL DEFAULT 0, created_at TEXT NOT NULL,
          FOREIGN KEY(user_id) REFERENCES users(id)
        );
        CREATE INDEX IF NOT EXISTS idx_sessions_user ON sessions(user_id);
        CREATE TABLE IF NOT EXISTS datasets (
          id TEXT PRIMARY KEY, user_id TEXT NOT NULL, path TEXT NOT NULL, created_at TEXT NOT NULL,
          FOREIGN KEY(user_id) REFERENCES users(id)
        );
        CREATE INDEX IF NOT EXISTS idx_datasets_user ON datasets(user_id);
        CREATE TABLE IF NOT EXISTS charts (
          id TEXT PRIMARY KEY, user_id TEXT NOT NULL, path TEXT NOT NULL, created_at TEXT NOT NULL,
          FOREIGN KEY(user_id) REFERENCES users(id)
        );
        CREATE INDEX IF NOT EXISTS idx_charts_user ON charts(user_id);
        ''')

def now(): return datetime.now(timezone.utc).isoformat()
def new_id(): return secrets.token_urlsafe(18)

def get_user(username):
    with _conn() as c: return c.execute('SELECT * FROM users WHERE username=?', (username,)).fetchone()
def get_user_by_id(uid):
    with _conn() as c: return c.execute('SELECT * FROM users WHERE id=?', (uid,)).fetchone()
def create_user(username, password_hash, role='analyst'):
    uid = new_id()
    with _conn() as c:
        c.execute('INSERT INTO users(id,username,password_hash,role,created_at) VALUES(?,?,?,?,?)', (uid, username, password_hash, role, now()))
    return uid
def create_session(user_id, jti, expires_at):
    with _conn() as c: c.execute('INSERT INTO sessions(jti,user_id,expires_at,created_at) VALUES(?,?,?,?)', (jti,user_id,expires_at,now()))
def session_valid(jti, user_id):
    with _conn() as c:
        r=c.execute('SELECT * FROM sessions WHERE jti=? AND user_id=? AND revoked=0', (jti,user_id)).fetchone()
        if not r: return False
        return datetime.fromisoformat(r['expires_at']) > datetime.now(timezone.utc)
def revoke_session(jti):
    with _conn() as c: c.execute('UPDATE sessions SET revoked=1 WHERE jti=?', (jti,))
def add_dataset(dataset_id,user_id,path):
    with _conn() as c: c.execute('INSERT OR REPLACE INTO datasets(id,user_id,path,created_at) VALUES(?,?,?,?)',(dataset_id,user_id,path,now()))
def owned_dataset(dataset_id,user_id):
    with _conn() as c: return c.execute('SELECT * FROM datasets WHERE id=? AND user_id=?',(dataset_id,user_id)).fetchone()
def add_chart(chart_id,user_id,path):
    with _conn() as c: c.execute('INSERT OR REPLACE INTO charts(id,user_id,path,created_at) VALUES(?,?,?,?)',(chart_id,user_id,path,now()))
def owned_chart(chart_id,user_id):
    with _conn() as c: return c.execute('SELECT * FROM charts WHERE id=? AND user_id=?',(chart_id,user_id)).fetchone()
