"""Compatibility-safe facade for tenant-scoped analytics engines."""
from __future__ import annotations
from typing import Any
import pandas as pd

try:
    from forecast_engine import run_forecast_analysis
except ImportError:
    run_forecast_analysis = None
try:
    from correlation_engine import calculate_correlation
except ImportError:
    calculate_correlation = None
try:
    from advanced_root_cause_engine import analyze_advanced_root_cause
except ImportError:
    analyze_advanced_root_cause = None


def ask_with_engine(df: pd.DataFrame, question: str) -> dict[str, Any]:
    """Return a deterministic safe response until the full orchestrator contract is migrated."""
    return {"question": question, "rows": int(len(df)), "columns": list(df.columns), "status": "engine_facade_ready"}


def dashboard_with_engine(df: pd.DataFrame) -> dict[str, Any]:
    result: dict[str, Any] = {"rows": int(len(df)), "columns": list(df.columns), "charts": {}}
    for col in df.select_dtypes(include="number").columns[:10]:
        result["charts"][col] = {"min": float(df[col].min()), "max": float(df[col].max()), "mean": float(df[col].mean())}
    return result


def correlation_with_engine(df: pd.DataFrame) -> Any:
    numeric = df.select_dtypes(include="number")
    return calculate_correlation(numeric) if calculate_correlation and not numeric.empty else numeric.corr().to_dict() if not numeric.empty else {}


def forecast_with_engine(df: pd.DataFrame, **kwargs: Any) -> Any:
    return run_forecast_analysis(df, **kwargs) if run_forecast_analysis else {"status": "forecast_engine_unavailable"}


def root_cause_with_engine(df: pd.DataFrame, **kwargs: Any) -> Any:
    return analyze_advanced_root_cause(df, **kwargs) if analyze_advanced_root_cause else {"status": "root_cause_engine_unavailable"}

try:
    from segmentation_engine import run_segmentation_analysis
except ImportError:
    run_segmentation_analysis = None

def segmentation_with_engine(df: pd.DataFrame, **kwargs: Any) -> Any:
    return run_segmentation_analysis(df, **kwargs) if run_segmentation_analysis else {"status": "segmentation_engine_unavailable"}
