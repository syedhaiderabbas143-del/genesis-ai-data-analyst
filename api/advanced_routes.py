
from __future__ import annotations
from typing import Any
import pandas as pd
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from security.dependencies import current_user
from security.dataset_repository import DatasetRepository, DatasetAccessDenied, DatasetNotFound
from forecast_engine import run_forecast_analysis

router = APIRouter(prefix='/v2', tags=['advanced-analytics'])
_repo = DatasetRepository(root='storage')

class ForecastRequest(BaseModel):
    target_column: str = Field(min_length=1, max_length=200)
    periods: int = Field(default=12, ge=1, le=100)

class CorrelationRequest(BaseModel):
    method: str = Field(default='pearson', pattern='^(pearson|spearman)$')

def _owner(user: dict) -> str:
    owner = str(user.get('sub') or user.get('user_id') or '').strip()
    if not owner:
        raise HTTPException(401, 'Authenticated user identity missing')
    return owner

def _frame(owner: str, dataset_id: str) -> pd.DataFrame:
    try:
        _, frame = _repo.get(owner, dataset_id)
        return frame
    except (DatasetAccessDenied, DatasetNotFound):
        raise HTTPException(404, 'Dataset not found')

@router.get('/datasets/{dataset_id}/dashboard')
def dashboard(dataset_id: str, user: dict = Depends(current_user)):
    frame = _frame(_owner(user), dataset_id)
    charts = {}
    for column in frame.columns[:12]:
        counts = frame[column].astype(str).value_counts().head(20)
        charts[str(column)] = [{'label': str(k), 'value': int(v)} for k, v in counts.items()]
    return {'success': True, 'dataset_id': dataset_id, 'rows': len(frame), 'columns': len(frame.columns), 'charts': charts}

@router.post('/datasets/{dataset_id}/correlation')
def correlation(dataset_id: str, request: CorrelationRequest, user: dict = Depends(current_user)):
    frame = _frame(_owner(user), dataset_id)
    numeric = frame.select_dtypes(include='number')
    if numeric.empty:
        raise HTTPException(400, 'Dataset has no numeric columns')
    matrix = numeric.corr(method=request.method).replace({float('nan'): None}).to_dict()
    return {'success': True, 'dataset_id': dataset_id, 'method': request.method, 'columns': list(numeric.columns), 'matrix': matrix}

@router.post('/datasets/{dataset_id}/forecast')
def forecast(dataset_id: str, request: ForecastRequest, user: dict = Depends(current_user)):
    frame = _frame(_owner(user), dataset_id)
    try:
        result = run_forecast_analysis(frame, request.target_column, request.periods)
    except ValueError as exc:
        raise HTTPException(400, str(exc)) from exc
    return {'success': True, 'dataset_id': dataset_id, 'result': result}

@router.get('/datasets/{dataset_id}/report')
def report(dataset_id: str, user: dict = Depends(current_user)):
    frame = _frame(_owner(user), dataset_id)
    numeric = frame.select_dtypes(include='number')
    return {'success': True, 'dataset_id': dataset_id, 'report': {'rows': int(len(frame)), 'columns': int(len(frame.columns)), 'missing_values': int(frame.isna().sum().sum()), 'numeric_summary': numeric.describe().replace({float('nan'): None}).to_dict()}}
