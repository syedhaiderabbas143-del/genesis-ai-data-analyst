from services.engine_registry import resolve_engine


def test_engine_registry_rejects_arbitrary_imports():
    try:
        resolve_engine("os.system")
    except ValueError:
        return
    raise AssertionError("arbitrary engine name was accepted")
