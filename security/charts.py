"""Safe chart path helper; chart files must be scoped to an owner/job."""
from pathlib import Path

def safe_chart_path(root: str | Path, owner_id: str, filename: str) -> Path:
    base = Path(root).resolve() / owner_id
    base.mkdir(parents=True, exist_ok=True)
    candidate = (base / Path(filename).name).resolve()
    if base not in candidate.parents:
        raise ValueError("Invalid chart path")
    return candidate
