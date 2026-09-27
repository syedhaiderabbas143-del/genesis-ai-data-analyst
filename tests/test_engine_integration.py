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

    def fake_resolve_engine(name):
        if name == "correlation":
            return lambda df: fake_result
        if name == "root_cause":
            return lambda df, **kwargs: {
                "issue_type": kwargs["issue_type"],
                "issue_title": kwargs["issue_title"],
                "issue_message": kwargs["issue_message"],
            }
        raise AssertionError(f"Unexpected engine requested: {name}")

    with patch(
        "services.engine_registry.resolve_engine",
        side_effect=fake_resolve_engine
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

def test_orchestration_executes_canonical_root_cause_engine():
    df = pd.DataFrame({
        "sales": [100, 120, 140, 160, 180, 200],
        "profit": [20, 25, 30, 35, 40, 45],
        "cost": [80, 95, 110, 125, 140, 155],
        "city": ["A", "A", "B", "B", "C", "C"],
    })

    result = run_orchestration(df)

    assert result["success"] is True
    assert "execution_results" in result
    assert "root_cause" in result["execution_results"]
    assert result["execution_results"]["root_cause"]["issue_type"] == "root_cause_analysis"
    assert result["execution_results"]["root_cause"]["issue_title"] == "Profit root cause analysis"



