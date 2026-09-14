"""Tenant-scoped persistent dataset repository."""
from __future__ import annotations
import hashlib, sqlite3
from dataclasses import dataclass
from pathlib import Path
from uuid import uuid4
import pandas as pd

@dataclass(frozen=True)
class DatasetRecord:
    dataset_id: str; owner_id: str; filename: str; rows: int; columns: int; storage_path: str
class DatasetNotFound(LookupError): pass
class DatasetAccessDenied(PermissionError): pass

class DatasetRepository:
    def __init__(self, root='storage', db_path=None):
        self.root=Path(root).resolve(); self.root.mkdir(parents=True, exist_ok=True)
        self.db_path=Path(db_path or self.root/'metadata.sqlite3').resolve(); self.db_path.parent.mkdir(parents=True, exist_ok=True)
        with sqlite3.connect(self.db_path) as con:
            con.execute('CREATE TABLE IF NOT EXISTS datasets(dataset_id TEXT PRIMARY KEY, owner_id TEXT NOT NULL, filename TEXT NOT NULL, rows INTEGER NOT NULL, columns INTEGER NOT NULL, storage_path TEXT NOT NULL, sha256 TEXT NOT NULL, created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP)')
            con.execute('CREATE INDEX IF NOT EXISTS idx_datasets_owner ON datasets(owner_id)')
    @staticmethod
    def _safe(value):
        if not value or value in {'.','..'} or Path(value).name != value or '/' in value or '\\' in value: raise ValueError('unsafe path component')
        return value
    def _path(self, owner, did):
        base=(self.root/self._safe(owner)/'datasets').resolve(); base.mkdir(parents=True, exist_ok=True)
        target=(base/(self._safe(did)+'.csv')).resolve()
        if self.root not in target.parents: raise ValueError('path escaped storage root')
        return target
    def create(self, owner_id, filename, frame):
        if not owner_id or not filename or not isinstance(frame,pd.DataFrame): raise ValueError('invalid dataset input')
        did=uuid4().hex; path=self._path(owner_id,did); frame.to_csv(path,index=False)
        digest=hashlib.sha256(path.read_bytes()).hexdigest()
        with sqlite3.connect(self.db_path) as con: con.execute('INSERT INTO datasets VALUES(?,?,?,?,?,?,?,CURRENT_TIMESTAMP)',(did,owner_id,Path(filename).name,len(frame),len(frame.columns),str(path),digest))
        return DatasetRecord(did,owner_id,Path(filename).name,len(frame),len(frame.columns),str(path))
    def _record(self, owner, did):
        with sqlite3.connect(self.db_path) as con: row=con.execute('SELECT dataset_id,owner_id,filename,rows,columns,storage_path FROM datasets WHERE dataset_id=? AND owner_id=?',(did,owner)).fetchone()
        if not row: raise DatasetAccessDenied('dataset does not belong to authenticated user')
        return DatasetRecord(*row)
    def get(self, owner_id, dataset_id):
        rec=self._record(owner_id,dataset_id); path=Path(rec.storage_path).resolve()
        if not path.is_file() or self.root not in path.parents: raise DatasetNotFound('dataset payload is missing or invalid')
        return rec,pd.read_csv(path)
    def list_owned(self, owner_id):
        with sqlite3.connect(self.db_path) as con: rows=con.execute('SELECT dataset_id,owner_id,filename,rows,columns,storage_path FROM datasets WHERE owner_id=? ORDER BY created_at DESC',(owner_id,)).fetchall()
        return [DatasetRecord(*r) for r in rows]
    def delete(self, owner_id, dataset_id):
        rec=self._record(owner_id,dataset_id)
        with sqlite3.connect(self.db_path) as con: con.execute('DELETE FROM datasets WHERE dataset_id=? AND owner_id=?',(dataset_id,owner_id))
        Path(rec.storage_path).unlink(missing_ok=True)
