import csv
import os
from datetime import datetime
from sqlalchemy.orm import Session
from models import Job
from mock_data import get_mock_smart_meter_data

def process_export_job(job_id: str, db: Session, export_dir: str = 'exports'):
    job = db.query(Job).filter(Job.id == job_id).first()
    if not job:
        return
    try:
        # Parse datetimes
        start = datetime.fromisoformat(job.start_datetime.replace('Z', ''))
        end = datetime.fromisoformat(job.end_datetime.replace('Z', ''))
        # Get data
        data = get_mock_smart_meter_data(job.smart_meter_id, start, end)
        if not data:
            job.status = 'failed'
            job.error_message = f"Smart meter with ID '{job.smart_meter_id}' not found or no data."
            job.updated_at = datetime.utcnow()
            db.commit()
            return
        # Prepare export dir
        os.makedirs(export_dir, exist_ok=True)
        filename = f"smart_meter_{job.smart_meter_id}_{start.strftime('%Y%m%d')}_{end.strftime('%Y%m%d')}.csv"
        file_path = os.path.join(export_dir, filename)
        # Write CSV
        with open(file_path, 'w', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=['timestamp','smart_meter_id','energy_kwh','power_kw','voltage_v','current_a'])
            writer.writeheader()
            for row in data:
                writer.writerow(row)
        # Update job
        job.status = 'completed'
        job.file_path = file_path
        job.record_count = len(data)
        job.file_size_bytes = os.path.getsize(file_path)
        job.updated_at = datetime.utcnow()
        db.commit()
    except Exception as e:
        job.status = 'failed'
        job.error_message = str(e)
        job.updated_at = datetime.utcnow()
        db.commit() 