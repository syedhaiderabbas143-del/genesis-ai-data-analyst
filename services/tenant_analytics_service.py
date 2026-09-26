"""Tenant-scoped analytics service boundary.

Route handlers should call this service with an already authenticated owner
and dataset repository. No module-level DataFrame is used here.
"""
from __future__ import annotations

from typing import Any

import pandas as pd

from security.dataset_repository import DatasetRepository


class TenantAnalyticsService:
    def __init__(self, repository: DatasetRepository):
        self.repository = repository

    def load_owned_frame(self, owner_id: str, dataset_id: str) -> pd.DataFrame:
        """Load only a dataset owned by owner_id."""
        record, frame = self.repository.get(owner_id, dataset_id)
        if record is None or frame is None:
            raise PermissionError("Dataset is not available to this user")
        return frame

    def summarize(self, owner_id: str, dataset_id: str) -> dict[str, Any]:
        frame = self.load_owned_frame(owner_id, dataset_id)
        numeric = frame.select_dtypes(include="number")
        return {
            "dataset_id": dataset_id,
            "rows": int(len(frame)),
            "columns": int(len(frame.columns)),
            "numeric_columns": list(numeric.columns),
            "missing_values": int(frame.isna().sum().sum()),
        }
