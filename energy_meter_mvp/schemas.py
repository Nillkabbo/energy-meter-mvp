from pydantic import BaseModel
from typing import Optional, Dict, Any, Literal
from datetime import datetime

class ExportRequest(BaseModel):
    smart_meter_id: str
    start_datetime: str
    end_datetime: str
    format: Literal['csv'] = 'csv'

class ExportJobResponse(BaseModel):
    job_id: str
    status: str
    message: str

class ExportStatusPendingResponse(BaseModel):
    job_id: str
    status: str
    message: str
    created_at: str
    updated_at: str

class ExportStatusCompletedResponse(BaseModel):
    job_id: str
    status: str
    message: str
    created_at: str
    updated_at: str
    file_info: Dict[str, Any]

class ExportStatusFailedResponse(BaseModel):
    job_id: str
    status: str
    message: str
    created_at: str
    updated_at: str
    error: Dict[str, Any]

class ExportStatusNotFoundResponse(BaseModel):
    status: str
    message: str 