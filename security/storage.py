"""User/job-scoped storage foundation.
Do not use module-level DataFrames for multi-user production deployments.
"""
from dataclasses import dataclass, field
from pathlib import Path
from threading import Lock
from uuid import uuid4
import pandas as pd

@dataclass
class DatasetSession:
    owner_id: str
    dataset_id: str = field(default_factory=lambda: uuid4().hex)
    dataframe: pd.DataFrame | None = None

class DatasetSessionStore:
    def __init__(self):
        self._items = {}
        self._lock = Lock()

    def create(self, owner_id: str, dataframe: pd.DataFrame) -> DatasetSession:
        session = DatasetSession(owner_id=owner_id, dataframe=dataframe.copy())
        with self._lock:
            self._items[(owner_id, session.dataset_id)] = session
        return session

    def get(self, owner_id: str, dataset_id: str) -> DatasetSession | None:
        with self._lock:
            return self._items.get((owner_id, dataset_id))

    def delete(self, owner_id: str, dataset_id: str) -> bool:
        with self._lock:
            return self._items.pop((owner_id, dataset_id), None) is not None

session_store = DatasetSessionStore()
