from unittest.mock import patch

import pandas as pd

from services.engine_registry import resolve_engine
from orchestration_engine import run_orchestration


def test_engine_registry_rejects_arbitrary_imports():
    try:
        resolve_engine("os.system")
    except ValueError:
        return
    raise AssertionError("arbitrary engine name was accepted")


def test_engine_registry_resolves_canonical_engines():
    forecast = resolve_engine("forecast")
    correlation = resolve_engine("correlation")
    root_cause = resolve_engine("root_cause")

    assert callable(forecast)
    assert callable(correlation)
    assert callable(root_cause)


def test_orchestration_executes_canonical_correlation_engine():
    df = pd.DataFrame({
        "sales": [100, 120, 140, 160],
        "profit": [20, 25, 30, 35],
        "cost": [80, 95, 110, 125],
    })

    fake_result = {
        "method": "pearson",
        "correlations": {
            "sales": {"profit": 1.0}
        }
    }

    with patch(
        "services.engine_registry.resolve_engine",
        return_value=lambda df: fake_result
    ) as resolve_engine_mock:
        result = run_orchestration(df)

    resolve_engine_mock.assert_called()
    assert result["success"] is True
    assert "execution_results" in result
    assert result["execution_results"]["correlation"] == fake_result


def test_orchestration_executes_canonical_segmentation_engine():
    df = pd.DataFrame({
        "sales": [100, 120, 140, 160, 180, 200],
        "profit": [20, 25, 30, 35, 40, 45],
        "cost": [80, 95, 110, 125, 140, 155],
        "city": ["A", "A", "B", "B", "C", "C"],
    })

    result = run_orchestration(df)

    assert result["success"] is True
    assert "execution_results" in result
    assert "segmentation" in result["execution_results"]
    assert result["execution_results"]["segmentation"]["success"] is True


def test_engine_registry_resolves_canonical_segmentation_engine():
    segmentation = resolve_engine("segmentation")

    assert callable(segmentation)
