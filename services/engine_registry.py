"""Canonical engine registry for tenant-scoped analytics.

This adapter keeps engine selection in one place and routes approved
analytics engines through the compatibility-safe facade.
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
    "forecast": EngineSpec(
        "forecast",
        "services.advanced_engine_facade",
        "forecast_with_engine",
    ),
    "correlation": EngineSpec(
        "correlation",
        "services.advanced_engine_facade",
        "correlation_with_engine",
    ),
    "root_cause": EngineSpec(
        "root_cause",
        "services.advanced_engine_facade",
        "root_cause_with_engine",
    ),
    "segmentation": EngineSpec(
        "segmentation",
        "services.advanced_engine_facade",
        "segmentation_with_engine",
    ),
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


