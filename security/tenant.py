"""Tenant-aware dataset and artifact ownership primitives.

This module deliberately keeps persistence behind a small interface so the
legacy analytics code can migrate incrementally without sharing global state.
"""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from threading import RLock
from typing import Any
from uuid import uuid4


class TenantAccessError(PermissionError):
    """Raised when a tenant attempts to access another tenant's resource."""


@dataclass(frozen=True)
class TenantResource:
    resource_id: str
    owner_id: str
    path: str | None = None


class TenantResourceStore:
    """Thread-safe ownership registry for datasets, charts, and reports."""

    def __init__(self) -> None:
        self._resources: dict[str, dict[str, TenantResource]] = {}
        self._lock = RLock()

    def create(self, owner_id: str, resource_type: str, path: str | None = None) -> TenantResource:
        if not owner_id or not resource_type:
            raise ValueError("owner_id and resource_type are required")
        resource_id = uuid4().hex
        resource = TenantResource(resource_id, owner_id, path)
        with self._lock:
            self._resources.setdefault(resource_type, {})[resource_id] = resource
        return resource

    def get_owned(self, owner_id: str, resource_type: str, resource_id: str) -> TenantResource:
        with self._lock:
            resource = self._resources.get(resource_type, {}).get(resource_id)
        if resource is None or resource.owner_id != owner_id:
            raise TenantAccessError("resource does not belong to the authenticated tenant")
        return resource

    def delete_owned(self, owner_id: str, resource_type: str, resource_id: str) -> None:
        self.get_owned(owner_id, resource_type, resource_id)
        with self._lock:
            self._resources[resource_type].pop(resource_id, None)


def tenant_path(root: str | Path, owner_id: str, resource_type: str, resource_id: str) -> Path:
    """Return a confined tenant path; reject traversal and unsafe identifiers."""
    safe_parts = (owner_id, resource_type, resource_id)
    if any(not part or part in {".", ".."} or Path(part).name != part for part in safe_parts):
        raise ValueError("unsafe tenant path component")
    base = Path(root).resolve()
    target = (base / owner_id / resource_type / resource_id).resolve()
    if base not in target.parents:
        raise ValueError("tenant path escaped storage root")
    return target
