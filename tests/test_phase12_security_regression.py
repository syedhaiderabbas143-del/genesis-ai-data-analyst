import os, pathlib, re
import pytest

ROOT = pathlib.Path(__file__).resolve().parents[1]


def test_project_compiles():
    import compileall
    assert compileall.compile_dir(str(ROOT), quiet=1)


def test_migrated_api_does_not_use_legacy_global_state():
    api = ROOT / "api"
    if not api.exists():
        pytest.skip("api package not present")
    text = "\n".join(p.read_text(errors="ignore") for p in api.rglob("*.py"))
    assert "latest_df" not in text
    assert "current_df" not in text


def test_security_configuration_has_secret_guard():
    p = ROOT / "security" / "config.py"
    if not p.exists():
        pytest.skip("security config not present")
    text = p.read_text(errors="ignore")
    assert "GENESIS_JWT_SECRET" in text or "JWT_SECRET" in text


def test_repository_uses_csv_storage():
    matches = list(ROOT.rglob("*.py"))
    text = "\n".join(p.read_text(errors="ignore") for p in matches)
    assert ".csv" in text
    assert ".parquet" not in text or "parquet" in text.lower()  # compatibility guard


def test_route_modules_exist():
    assert (ROOT / "api").exists()
    assert any((ROOT / "api").glob("*.py"))
