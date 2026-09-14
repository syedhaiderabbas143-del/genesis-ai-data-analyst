from pathlib import Path

import pytest

from security.tenant import TenantAccessError, TenantResourceStore, tenant_path


def test_tenant_cannot_read_other_tenant_resource():
    store = TenantResourceStore()
    resource = store.create("user-a", "datasets")
    with pytest.raises(TenantAccessError):
        store.get_owned("user-b", "datasets", resource.resource_id)


def test_tenant_path_is_confined(tmp_path: Path):
    path = tenant_path(tmp_path, "user-a", "charts", "chart-1")
    assert path == (tmp_path / "user-a" / "charts" / "chart-1").resolve()
    with pytest.raises(ValueError):
        tenant_path(tmp_path, "../user-a", "charts", "chart-1")
