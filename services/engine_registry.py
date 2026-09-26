"""Canonical engine registry for tenant-scoped analytics.

This adapter keeps engine selection in one place and avoids route handlers
importing competing implementations directly. Engines are injected lazily so
optional dependencies do not break application startup.
"""
from __future__ import annotations

from dataclasses import dataclass
from importlib import import_module
from typing import Any, Callable


@dataclass(frozen=True)
class EngineSpec:
    name: str
    module: str
    attribute: str


ENGINE_SPECS = {
    "forecast": EngineSpec("forecast", "forecast_engine", "forecast_data"),
    "correlation": EngineSpec("correlation", "correlation_engine", "calculate_correlation"),
    "root_cause": EngineSpec("root_cause", "root_cause_analysis_engine", "run_root_cause_analysis"),
}


def resolve_engine(name: str) -> Callable[..., Any]:
    """Resolve one approved engine; reject arbitrary import paths."""
    try:
        spec = ENGINE_SPECS[name]
    except KeyError as exc:
        raise ValueError(f"Unsupported engine: {name}") from exc
    module = import_module(spec.module)
    fn = getattr(module, spec.attribute, None)
    if not callable(fn):
        raise RuntimeError(f"Configured engine is unavailable: {name}")
    return fn
