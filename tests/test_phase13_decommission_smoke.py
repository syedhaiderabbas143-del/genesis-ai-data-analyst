import os
from pathlib import Path


def test_legacy_policy_is_opt_in_and_returns_410():
    from security.legacy_routes import is_legacy_path, legacy_routes_disabled
    assert is_legacy_path('/upload')
    assert is_legacy_path('/api/analytics/forecast-history')
    assert not is_legacy_path('/v2/datasets')
    assert legacy_routes_disabled() is False


def test_v2_route_modules_are_present_and_tenant_scoped():
    tenant = Path('api/tenant_routes.py').read_text()
    advanced = Path('api/advanced_routes.py').read_text()
    for route in ["/upload", "/datasets", "/datasets/{dataset_id}/filter", "/datasets/{dataset_id}/ask"]:
        assert route in tenant
    for route in ["/dashboard", "/correlation", "/forecast", "/report"]:
        assert route in advanced
    assert 'Depends(current_user)' in tenant
    assert 'Depends(current_user)' in advanced


def test_decommission_middleware_blocks_legacy_when_enabled(monkeypatch):
    monkeypatch.setenv('GENESIS_DISABLE_LEGACY_ROUTES', 'true')
    from security.legacy_routes import legacy_routes_disabled, is_legacy_path
    assert legacy_routes_disabled()
    assert is_legacy_path('/upload')
    assert is_legacy_path('/genesis/clean/ai')


def test_compile_targets_exist():
    assert Path('main.py').exists()
    assert Path('api/tenant_routes.py').exists()
    assert Path('api/advanced_routes.py').exists()
