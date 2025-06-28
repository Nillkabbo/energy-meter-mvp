from fastapi import FastAPI, HTTPException, BackgroundTasks, Depends, Response
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from uuid import uuid4
from datetime import datetime, timedelta
import os

from database import SessionLocal, engine
from models import Job, Base
from schemas import ExportRequest, ExportJobResponse, ExportStatusPendingResponse, ExportStatusCompletedResponse, ExportStatusFailedResponse, ExportStatusNotFoundResponse
from background import process_export_job

app = FastAPI()
EXPORT_DIR = 'exports'

# Create tables
Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def validate_request(data: ExportRequest):
    # Validate smart_meter_id
    if not data.smart_meter_id or not isinstance(data.smart_meter_id, str):
        raise HTTPException(status_code=400, detail="Invalid or missing smart_meter_id")
    # Validate datetimes
    try:
        start = datetime.fromisoformat(data.start_datetime.replace('Z', ''))
        end = datetime.fromisoformat(data.end_datetime.replace('Z', ''))
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid datetime format. Use ISO 8601.")
    now = datetime.utcnow()
    if start >= end:
        raise HTTPException(status_code=400, detail="end_datetime must be after start_datetime")
    if end > now:
        raise HTTPException(status_code=400, detail="end_datetime must be in the past")
    if (end - start) > timedelta(days=366):
        raise HTTPException(status_code=400, detail="Maximum date range is 1 year")
    if (end - start) < timedelta(minutes=1):
        raise HTTPException(status_code=400, detail="Minimum date range is 1 minute")
    if data.format != 'csv':
        raise HTTPException(status_code=400, detail="Only 'csv' format is supported")
    return start, end

@app.post('/api/export/csv', response_model=ExportJobResponse)
def export_csv(request: ExportRequest, background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    start, end = validate_request(request)
    job_id = str(uuid4())
    job = Job(
        id=job_id,
        smart_meter_id=request.smart_meter_id,
        start_datetime=request.start_datetime,
        end_datetime=request.end_datetime,
        status='pending',
    )
    db.add(job)
    db.commit()
    background_tasks.add_task(process_export_job, job_id, db)
    return ExportJobResponse(job_id=job_id, status='pending', message='Export job created successfully')

@app.get('/api/export/status/{job_id}')
def get_status(job_id: str, db: Session = Depends(get_db)):
    job = db.query(Job).filter(Job.id == job_id).first()
    if not job:
        return ExportStatusNotFoundResponse(status='not_found', message=f"Job with ID '{job_id}' not found")
    if job.status == 'pending':
        return ExportStatusPendingResponse(
            job_id=job.id,
            status=job.status,
            message='Job is being processed',
            created_at=job.created_at.isoformat() if job.created_at else '',
            updated_at=job.updated_at.isoformat() if job.updated_at else '',
        )
    elif job.status == 'completed':
        start = job.start_datetime
        end = job.end_datetime
        filename = os.path.basename(job.file_path) if job.file_path else ''
        return ExportStatusCompletedResponse(
            job_id=job.id,
            status=job.status,
            message='Export completed successfully',
            created_at=job.created_at.isoformat() if job.created_at else '',
            updated_at=job.updated_at.isoformat() if job.updated_at else '',
            file_info={
                'filename': filename,
                'download_url': f'/api/export/download/{job.id}',
                'file_size_bytes': job.file_size_bytes,
                'record_count': job.record_count,
                'export_period': {
                    'start': start,
                    'end': end
                }
            }
        )
    elif job.status == 'failed':
        return ExportStatusFailedResponse(
            job_id=job.id,
            status=job.status,
            message='Export failed',
            created_at=job.created_at.isoformat() if job.created_at else '',
            updated_at=job.updated_at.isoformat() if job.updated_at else '',
            error={
                'code': 'EXPORT_FAILED',
                'message': job.error_message or 'Unknown error',
                'details': job.error_message or ''
            }
        )

@app.get('/api/export/download/{job_id}')
def download_csv(job_id: str, db: Session = Depends(get_db)):
    job = db.query(Job).filter(Job.id == job_id).first()
    if not job or job.status != 'completed' or not job.file_path or not os.path.exists(job.file_path):
        raise HTTPException(status_code=404, detail='File not found or job not completed')
    filename = os.path.basename(job.file_path)
    return FileResponse(
        path=job.file_path,
        media_type='text/csv',
        filename=filename,
        headers={
            'Content-Disposition': f'attachment; filename="{filename}"'
        }
    ) 