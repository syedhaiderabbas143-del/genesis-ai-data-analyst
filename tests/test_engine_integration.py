from services.engine_registry import resolve_engine


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
