from __future__ import annotations
import io, os
from typing import Any
import pandas as pd
from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from pydantic import BaseModel, Field
from security.dependencies import current_user
from security.dataset_repository import DatasetRepository, DatasetAccessDenied, DatasetNotFound
router = APIRouter(prefix='/v2', tags=['tenant-datasets'])
_repo = DatasetRepository(root=os.getenv('GENESIS_DATA_ROOT', 'storage'))
class FilterRequest(BaseModel):
    column: str = Field(min_length=1, max_length=200)
    value: Any
class AskRequest(BaseModel):
    question: str = Field(min_length=1, max_length=2000)
def _owner(user: dict) -> str:
    owner = str(user.get('sub') or user.get('user_id') or '').strip()
    if not owner: raise HTTPException(401, 'Authenticated user identity missing')
    return owner
def _load_upload(upload: UploadFile) -> pd.DataFrame:
    name=(upload.filename or '').lower()
    if not name.endswith(('.csv','.xlsx','.xls')): raise HTTPException(415,'Only CSV/XLS/XLSX files are supported')
    raw=upload.file.read(); limit=int(os.getenv('GENESIS_MAX_UPLOAD_BYTES', str(25*1024*1024)))
    if len(raw)>limit: raise HTTPException(413,'Upload exceeds configured size limit')
    try: return pd.read_csv(io.BytesIO(raw)) if name.endswith('.csv') else pd.read_excel(io.BytesIO(raw))
    except Exception as exc: raise HTTPException(400, f'Could not parse dataset: {exc}') from exc
@router.post('/upload')
def upload_dataset(file: UploadFile=File(...), user: dict=Depends(current_user)):
    frame=_load_upload(file); record=_repo.create(_owner(user), file.filename or 'dataset', frame)
    return {'success':True,'dataset_id':record.dataset_id,'filename':record.filename,'rows':record.rows,'columns':record.columns}
@router.get('/datasets')
def list_datasets(user: dict=Depends(current_user)):
    return {'success':True,'datasets':[r.__dict__ for r in _repo.list_owned(_owner(user))]}
@router.delete('/datasets/{dataset_id}')
def delete_dataset(dataset_id: str, user: dict=Depends(current_user)):
    try: _repo.delete(_owner(user), dataset_id)
    except (DatasetAccessDenied, DatasetNotFound) as exc: raise HTTPException(404,'Dataset not found') from exc
    return {'success':True,'dataset_id':dataset_id}
@router.post('/datasets/{dataset_id}/filter')
def filter_dataset(dataset_id: str, request: FilterRequest, user: dict=Depends(current_user)):
    try: _, frame=_repo.get(_owner(user), dataset_id)
    except (DatasetAccessDenied, DatasetNotFound) as exc: raise HTTPException(404,'Dataset not found') from exc
    if request.column not in frame.columns: raise HTTPException(400,'Unknown dataset column')
    result=frame[frame[request.column].astype(str)==str(request.value)].head(1000)
    return {'success':True,'dataset_id':dataset_id,'rows':len(result),'data':result.where(pd.notna(result),None).to_dict(orient='records')}
@router.post('/datasets/{dataset_id}/ask')
def ask_dataset(dataset_id: str, request: AskRequest, user: dict=Depends(current_user)):
    try: _, frame=_repo.get(_owner(user), dataset_id)
    except (DatasetAccessDenied, DatasetNotFound) as exc: raise HTTPException(404,'Dataset not found') from exc
    numeric=frame.select_dtypes(include='number')
    return {'success':True,'dataset_id':dataset_id,'question':request.question,'answer':'Tenant-scoped dataset loaded successfully.','summary':{'rows':int(len(frame)),'columns':int(len(frame.columns)),'numeric_columns':list(numeric.columns)}}
