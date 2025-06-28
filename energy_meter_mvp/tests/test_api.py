import os
import sys
import shutil
import pytest
from pathlib import Path

# Add the parent directory to the Python path
sys.path.insert(0, str(Path(__file__).parent.parent))

from fastapi.testclient import TestClient
from main import app, EXPORT_DIR
from database import engine, Base

client = TestClient(app)

@pytest.fixture(autouse=True)
def setup_and_teardown():
    # Clean up exports and DB before each test
    if os.path.exists(EXPORT_DIR):
        shutil.rmtree(EXPORT_DIR)
    if os.path.exists('jobs.db'):
        engine.dispose()  # Close all connections before deleting
        os.remove('jobs.db')
    # Recreate DB schema
    Base.metadata.create_all(bind=engine)
    yield
    if os.path.exists(EXPORT_DIR):
        shutil.rmtree(EXPORT_DIR)
    if os.path.exists('jobs.db'):
        engine.dispose()
        os.remove('jobs.db')

def test_happy_path():
    req = {
        "smart_meter_id": "123",
        "start_datetime": "2024-01-01T00:00:00Z",
        "end_datetime": "2024-01-01T00:10:00Z",
        "format": "csv"
    }
    resp = client.post("/api/export/csv", json=req)
    assert resp.status_code == 200
    job_id = resp.json()["job_id"]
    # Wait for job to complete
    import time
    for _ in range(10):
        status = client.get(f"/api/export/status/{job_id}").json()
        if status["status"] == "completed":
            break
        time.sleep(0.5)
    assert status["status"] == "completed"
    # Download file
    dl = client.get(f"/api/export/download/{job_id}")
    assert dl.status_code == 200
    assert "text/csv" in dl.headers["content-type"]
    assert b"timestamp,smart_meter_id,energy_kwh" in dl.content

def test_invalid_smart_meter():
    req = {
        "smart_meter_id": "999",
        "start_datetime": "2024-01-01T00:00:00Z",
        "end_datetime": "2024-01-01T00:10:00Z",
        "format": "csv"
    }
    resp = client.post("/api/export/csv", json=req)
    assert resp.status_code == 200
    job_id = resp.json()["job_id"]
    import time
    for _ in range(10):
        status = client.get(f"/api/export/status/{job_id}").json()
        if status["status"] == "failed":
            break
        time.sleep(0.5)
    assert status["status"] == "failed"
    assert "not found" in status["error"]["message"].lower()

def test_invalid_date_range():
    req = {
        "smart_meter_id": "123",
        "start_datetime": "2024-01-02T00:00:00Z",
        "end_datetime": "2024-01-01T00:00:00Z",
        "format": "csv"
    }
    resp = client.post("/api/export/csv", json=req)
    assert resp.status_code == 400
    assert "end_datetime must be after start_datetime" in resp.text

def test_job_not_found():
    resp = client.get("/api/export/status/doesnotexist")
    assert resp.status_code == 200
    assert resp.json()["status"] == "not_found"

def test_concurrent_requests():
    req = {
        "smart_meter_id": "123",
        "start_datetime": "2024-01-01T00:00:00Z",
        "end_datetime": "2024-01-01T00:05:00Z",
        "format": "csv"
    }
    job_ids = []
    for _ in range(3):
        resp = client.post("/api/export/csv", json=req)
        assert resp.status_code == 200
        job_ids.append(resp.json()["job_id"])
    import time
    for job_id in job_ids:
        for _ in range(10):
            status = client.get(f"/api/export/status/{job_id}").json()
            if status["status"] == "completed":
                break
            time.sleep(0.5)
        assert status["status"] == "completed" 