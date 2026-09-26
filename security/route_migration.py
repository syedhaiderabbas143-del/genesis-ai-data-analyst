"""Adapters for binding legacy routes to owner-scoped datasets."""
from .dataset_repository import DatasetRepository
def dataset_for_request(repo, current_user_id, dataset_id):
    if not current_user_id: raise PermissionError('authenticated user required')
    return repo.get(current_user_id,dataset_id)
