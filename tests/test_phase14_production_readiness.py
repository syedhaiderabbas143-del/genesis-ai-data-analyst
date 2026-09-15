from pathlib import Path


def test_all_expected_v2_routes_are_registered_in_source():
    tenant = Path('api/tenant_routes.py').read_text()
    advanced = Path('api/advanced_routes.py').read_text()
    expected_tenant = ['/v2', "@router.post('/upload')", "@router.get('/datasets')", "@router.delete('/datasets/{dataset_id}')", "@router.post('/datasets/{dataset_id}/filter')", "@router.post('/datasets/{dataset_id}/ask')"]
    expected_advanced = ["@router.get('/datasets/{dataset_id}/dashboard')", "@router.post('/datasets/{dataset_id}/correlation')", "@router.post('/datasets/{dataset_id}/forecast')", "@router.get('/datasets/{dataset_id}/report')"]
    assert all(item in tenant for item in expected_tenant)
    assert all(item in advanced for item in expected_advanced)


def test_production_env_example_documents_required_controls():
    env = Path('.env.example').read_text()
    assert 'GENESIS_JWT_SECRET' in env
    assert 'GENESIS_DISABLE_LEGACY_ROUTES' in env
    assert 'GENESIS_MAX_UPLOAD_BYTES' in env


def test_live_fastapi_application_imports_and_exposes_routes(monkeypatch):
    monkeypatch.setenv('GENESIS_JWT_SECRET', 'x' * 40)
    from main import app
    def test_live_fastapi_application_imports_and_exposes_routes(monkeypatch):
     monkeypatch.setenv('GENESIS_JWT_SECRET', 'x' * 40)

    from main import app

    paths = set(app.openapi().get("paths", {}).keys())

    for path in [
        '/auth/register',
        '/auth/login',
        '/v2/upload',
        '/v2/datasets',
        '/v2/datasets/{dataset_id}/dashboard',
        '/v2/datasets/{dataset_id}/correlation',
        '/v2/datasets/{dataset_id}/forecast',
        '/v2/datasets/{dataset_id}/report'
    ]:
        assert path in paths
    for path in ['/auth/register', '/auth/login', '/v2/upload', '/v2/datasets', '/v2/datasets/{dataset_id}/dashboard', '/v2/datasets/{dataset_id}/correlation', '/v2/datasets/{dataset_id}/forecast', '/v2/datasets/{dataset_id}/report']:
        assert path in paths


def test_legacy_decommission_switch_is_not_applied_to_v2():
    from security.legacy_routes import is_legacy_path
    assert not is_legacy_path('/v2/upload')
    assert not is_legacy_path('/v2/datasets/abc/report')


def test_production_report_and_deployment_docs_exist():
    assert Path('PHASE14_PRODUCTION_READINESS_REPORT.md').exists()
    assert Path('DEPLOYMENT_CHECKLIST.md').exists()
