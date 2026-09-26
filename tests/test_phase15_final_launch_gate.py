from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_required_v2_route_modules_exist():
    assert (ROOT / 'api' / 'tenant_routes.py').exists()
    assert (ROOT / 'api' / 'advanced_routes.py').exists()


def test_legacy_decommission_switch_is_documented():
    text = (ROOT / 'PHASE13_LEGACY_DECOMMISSION_SMOKE_REPORT.md').read_text(encoding='utf-8')
    assert 'GENESIS_DISABLE_LEGACY_ROUTES' in text


def test_production_readiness_report_exists():
    assert (ROOT / 'PHASE14_PRODUCTION_READINESS_REPORT.md').exists()


def test_no_obvious_secret_literals_in_python_sources():
    bad = []
    for path in ROOT.rglob('*.py'):
        if 'tests' in path.parts or any(part in {'.venv', '__pycache__'} for part in path.parts):
            continue
        text = path.read_text(encoding='utf-8', errors='ignore').lower()
        for marker in ('sk-', '-----begin private key-----', 'password = ' + chr(34)):
            if marker in text:
                bad.append((str(path), marker))
    assert not bad, bad


def test_readme_contains_deployment_guidance():
    text = (ROOT / 'README.md').read_text(encoding='utf-8').lower()
    assert 'deploy' in text or 'production' in text
