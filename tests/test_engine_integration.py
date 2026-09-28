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
        "sales": [100, 120, 140, 160, 180, 200, 220, 240, 260, 280, 300, 320],
        "performance_rating": [1, 2, 1, 2, 1, 3, 4, 3, 4, 5, 3, 4],
        "cost": [80, 95, 110, 125, 140, 155, 170, 185, 200, 215, 230, 245],
        "city": ["A", "A", "B", "B", "C", "C", "A", "B", "C", "A", "B", "C"],
    })

    result = run_orchestration(df)

    assert result["success"] is True
    assert "execution_results" in result
    assert "root_cause" in result["execution_results"]

    root_cause = result["execution_results"]["root_cause"]

    assert root_cause["issue_type"] == "low_performance"
    assert root_cause["root_cause_detected"] is True
    assert root_cause["affected_records"] == 5
    assert root_cause["affected_percentage"] == 41.67
    assert root_cause["numeric_factors"]



def test_orchestration_root_cause_skips_unsupported_low_performance_target():
    df = pd.DataFrame({
        "sales": [100, 120, 140, 160, 180, 200],
        "profit": [20, 25, 30, 35, 40, 45],
        "cost": [80, 95, 110, 125, 140, 155],
        "city": ["A", "A", "B", "B", "C", "C"],
    })

    result = run_orchestration(df)

    assert result["success"] is True
    root_cause = result["execution_results"]["root_cause"]

    assert root_cause["issue_type"] == "low_performance"
    assert root_cause["root_cause_detected"] is False
    assert root_cause["root_causes"] == []
    assert root_cause["contributing_groups"] == []
    assert root_cause["numeric_factors"] == []
    assert root_cause["analysis_confidence"] == "Low"
    assert root_cause["confidence_score"] == 0


def test_orchestration_avoids_pandas4_string_dtype_warning():
    import warnings

    df = pd.DataFrame({
        "sales": [100, 120, 140],
        "cost": [80, 95, 110],
        "city": ["A", "B", "C"],
        "active": [True, False, True],
    })

    with warnings.catch_warnings(record=True) as captured:
        warnings.simplefilter("always")
        result = run_orchestration(df)

    assert result["success"] is True
    pandas4_warnings = [
        warning for warning in captured
        if warning.category.__name__ == "Pandas4Warning"
    ]
    assert pandas4_warnings == []

def test_orchestration_isolates_engine_failure_and_continues():
    df = pd.DataFrame({
        "sales": [100, 120, 140, 160, 180, 200],
        "cost": [80, 95, 110, 125, 140, 155],
        "city": ["A", "A", "B", "B", "C", "C"],
    })

    def failing_correlation_engine(_df):
        raise RuntimeError("simulated correlation failure")

    with patch(
        "services.engine_registry.resolve_engine"
    ) as mocked_resolve:
        real_resolve = resolve_engine

        def resolve_with_failure(engine_name):
            if engine_name == "correlation":
                return failing_correlation_engine
            return real_resolve(engine_name)

        mocked_resolve.side_effect = resolve_with_failure

        result = run_orchestration(df)

    assert result["success"] is True
    assert "correlation" in result["execution_results"]
    assert result["execution_results"]["correlation"]["success"] is False
    assert "error" in result["execution_results"]["correlation"]

    assert "root_cause" in result["execution_results"]
    assert "segmentation" in result["execution_results"]

def test_orchestration_reports_partial_execution_status():
    df = pd.DataFrame({
        "sales": [100, 120, 140, 160, 180, 200],
        "cost": [80, 95, 110, 125, 140, 155],
        "city": ["A", "A", "B", "B", "C", "C"],
    })

    def failing_correlation_engine(_df):
        raise RuntimeError("simulated correlation failure")

    with patch(
        "services.engine_registry.resolve_engine"
    ) as mocked_resolve:
        real_resolve = resolve_engine

        def resolve_with_failure(engine_name):
            if engine_name == "correlation":
                return failing_correlation_engine
            return real_resolve(engine_name)

        mocked_resolve.side_effect = resolve_with_failure

        result = run_orchestration(df)

    assert result["success"] is True
    assert result["execution_status"]["overall_status"] == "partial_success"
    assert result["execution_status"]["successful_engines"] == 3
    assert result["execution_status"]["failed_engines"] == 1


def test_orchestration_reports_success_when_all_executed_engines_succeed():
    df = pd.DataFrame({
        "sales": [100, 120, 140, 160, 180, 200],
        "cost": [80, 95, 110, 125, 140, 155],
        "city": ["A", "A", "B", "B", "C", "C"],
    })

    result = run_orchestration(df)

    assert result["success"] is True
    assert result["execution_status"]["overall_status"] == "success"
    assert result["execution_status"]["failed_engines"] == 0
    assert result["execution_status"]["successful_engines"] == 4


def test_orchestration_reports_failed_when_all_executed_engines_fail():
    df = pd.DataFrame({
        "sales": [100, 120, 140, 160, 180, 200],
        "cost": [80, 95, 110, 125, 140, 155],
        "city": ["A", "A", "B", "B", "C", "C"],
    })

    def failing_engine(_df):
        raise RuntimeError("simulated engine failure")

    with patch("services.engine_registry.resolve_engine") as mocked_resolve:
        mocked_resolve.return_value = failing_engine
        result = run_orchestration(df)

    assert result["success"] is True
    assert result["execution_status"]["overall_status"] == "failed"
    assert result["execution_status"]["successful_engines"] == 0
    assert result["execution_status"]["failed_engines"] == 4


def test_orchestration_reports_execution_coverage_against_recommended_workflow():
    df = pd.DataFrame({
        "sales": [100, 120, 140, 160, 180, 200],
        "cost": [80, 95, 110, 125, 140, 155],
        "city": ["A", "A", "B", "B", "C", "C"],
    })

    result = run_orchestration(df)

    execution_status = result["execution_status"]

    assert execution_status["recommended_steps"] == result["total_recommended_steps"]
    assert execution_status["executed_engines"] == 4
    assert execution_status["unexecuted_steps"] == 4

def test_orchestration_executes_canonical_data_quality_engine():
    df = pd.DataFrame({
        "sales": [100, 120, 140, 160, 180, 200],
        "cost": [80, 95, 110, 125, 140, 155],
        "city": ["A", "A", "B", "B", "C", "C"],
    })

    result = run_orchestration(df)

    assert result["execution_status"]["overall_status"] == "success"
    assert "data_quality" in result["execution_results"]
    assert result["execution_results"]["data_quality"]["success"] is True
    assert result["execution_results"]["data_quality"]["analysis_type"] == "Genesis AI Quality Agent"
