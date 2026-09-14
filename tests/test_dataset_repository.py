import pandas as pd
import pytest
from security.dataset_repository import DatasetRepository, DatasetAccessDenied

def test_owner_isolation(tmp_path):
    repo=DatasetRepository(tmp_path/'storage'); rec=repo.create('user-a','sample.csv',pd.DataFrame({'x':[1,2]}))
    assert repo.get('user-a',rec.dataset_id)[0].owner_id=='user-a'
    with pytest.raises(DatasetAccessDenied): repo.get('user-b',rec.dataset_id)

def test_list_delete_scoped(tmp_path):
    repo=DatasetRepository(tmp_path/'storage'); a=repo.create('a','a.csv',pd.DataFrame({'x':[1]})); b=repo.create('b','b.csv',pd.DataFrame({'x':[2]}))
    assert [r.dataset_id for r in repo.list_owned('a')]==[a.dataset_id]
    repo.delete('a',a.dataset_id)
    with pytest.raises(DatasetAccessDenied): repo.get('a',a.dataset_id)
    assert repo.get('b',b.dataset_id)[0].owner_id=='b'
