import ast
from pathlib import Path
import pandas as pd
from security.dataset_repository import DatasetRepository, DatasetAccessDenied

ROOT = Path(__file__).resolve().parents[1]

def test_repository_round_trip_uses_csv_and_owner_scope(tmp_path):
    repo = DatasetRepository(root=tmp_path / 'storage')
    record = repo.create('user-a', 'sample.xlsx', pd.DataFrame({'x':[1,2], 'y':[3,4]}))
    assert record.storage_path.endswith('.csv')
    _, frame = repo.get('user-a', record.dataset_id)
    assert frame.to_dict('list') == {'x':[1,2], 'y':[3,4]}
    try:
        repo.get('user-b', record.dataset_id)
    except DatasetAccessDenied:
        pass
    else:
        raise AssertionError('cross-tenant dataset access was not denied')

def test_migrated_api_layer_has_no_legacy_dataframe_globals():
    for name in ('api/tenant_routes.py', 'api/advanced_routes.py'):
        tree = ast.parse((ROOT / name).read_text())
        source = (ROOT / name).read_text()
        assert 'latest_df' not in source
        assert 'current_df' not in source
        assert tree is not None

def test_advanced_routes_are_registered_in_source():
    source = (ROOT / 'api/advanced_routes.py').read_text()
    for route in ('/dashboard', '/correlation', '/forecast', '/report'):
        assert route in source
