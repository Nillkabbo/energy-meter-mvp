# Smart Meter CSV Export MVP

## Overview
A FastAPI-based REST API that implements asynchronous CSV export for smart meter data with job tracking and file download capabilities. This MVP demonstrates background job processing, file generation, and comprehensive error handling.

## Features
- ✅ RESTful API design with proper HTTP status codes
- ✅ Background job processing using FastAPI BackgroundTasks
- ✅ CSV file generation and storage
- ✅ Job status tracking (pending → completed/failed)
- ✅ File download with proper headers
- ✅ Comprehensive error handling and validation
- ✅ SQLite database with SQLAlchemy ORM
- ✅ Mock smart meter data generation
- ✅ Complete test suite with pytest

## Project Structure
```
OpenWatts/
├── main.py                 # FastAPI application with endpoints
├── models.py              # SQLAlchemy database models
├── schemas.py             # Pydantic request/response models
├── database.py            # Database connection setup
├── background.py          # Background job processing logic
├── mock_data.py           # Mock smart meter data generation
├── requirements.txt       # Python dependencies
├── migrations/
│   └── create_db.py       # Database migration script
├── tests/
│   └── test_api.py        # API test suite
├── exports/               # Generated CSV files (created at runtime)
├── jobs.db               # SQLite database (created at runtime)
└── README.md             # This file
```

## Setup Instructions

### Prerequisites
- Python 3.8 or higher
- pip (Python package installer)

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd OpenWatts
   ```

2. **Create and activate virtual environment**
   ```bash
   # Windows
   python -m venv venv
   venv\Scripts\activate

   # Linux/Mac
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Initialize database**
   ```bash
   python migrations/create_db.py
   ```

5. **Start the server**
   ```bash
   uvicorn main:app --reload
   ```

The API will be available at `http://localhost:8000`

## API Endpoints

### 1. Create CSV Export Job
**POST** `/api/export/csv`

Creates a new CSV export job for smart meter data.

**Request Body:**
```json
{
  "smart_meter_id": "string",
  "start_datetime": "2024-01-01T00:00:00Z",
  "end_datetime": "2024-01-31T23:59:59Z",
  "format": "csv"
}
```

**Response (200 OK):**
```json
{
  "job_id": "uuid-string",
  "status": "pending",
  "message": "Export job created successfully"
}
```

### 2. Check Job Status
**GET** `/api/export/status/{job_id}`

Returns the current status of an export job.

**Response - Pending (200 OK):**
```json
{
  "job_id": "uuid-string",
  "status": "pending",
  "message": "Job is being processed",
  "created_at": "2024-01-01T10:00:00Z",
  "updated_at": "2024-01-01T10:00:00Z"
}
```

**Response - Completed (200 OK):**
```json
{
  "job_id": "uuid-string",
  "status": "completed",
  "message": "Export completed successfully",
  "created_at": "2024-01-01T10:00:00Z",
  "updated_at": "2024-01-01T10:05:30Z",
  "file_info": {
    "filename": "smart_meter_123_20240101_20240131.csv",
    "download_url": "/api/export/download/{job_id}",
    "file_size_bytes": 1024000,
    "record_count": 1440,
    "export_period": {
      "start": "2024-01-01T00:00:00Z",
      "end": "2024-01-31T23:59:59Z"
    }
  }
}
```

**Response - Failed (200 OK):**
```json
{
  "job_id": "uuid-string",
  "status": "failed",
  "message": "Export failed",
  "created_at": "2024-01-01T10:00:00Z",
  "updated_at": "2024-01-01T10:01:15Z",
  "error": {
    "code": "SMART_METER_NOT_FOUND",
    "message": "Smart meter with ID '999' not found",
    "details": "The specified smart meter does not exist in the system"
  }
}
```

**Response - Not Found (200 OK):**
```json
{
  "status": "not_found",
  "message": "Job with ID 'uuid-string' not found"
}
```

### 3. Download CSV File
**GET** `/api/export/download/{job_id}`

Downloads the generated CSV file for a completed job.

**Response Headers:**
- `Content-Type: text/csv; charset=utf-8`
- `Content-Disposition: attachment; filename="smart_meter_123_20240101_20240131.csv"`

**Response Body:** CSV file content

## Validation Rules

- **Smart meter ID**: Required, string format (only "123" is supported in MVP)
- **Start datetime**: Required, ISO 8601 format, must be in the past
- **End datetime**: Required, ISO 8601 format, must be after start datetime
- **Maximum date range**: 1 year
- **Minimum date range**: 1 minute
- **Format**: Must be "csv" (only format supported in MVP)

## Error Handling

The API handles various error scenarios:

- **400 Bad Request**: Invalid input validation
- **404 Not Found**: Job not found or file not available
- **500 Internal Server Error**: Server-side processing errors

Common validation errors:
- Invalid datetime format
- End datetime before start datetime
- Date range too large (> 1 year)
- Date range too small (< 1 minute)
- Future end datetime
- Invalid smart meter ID

## Testing

### Run Tests
```bash
pytest tests/test_api.py -v
```

### Test Coverage
The test suite covers:
- ✅ Happy path: Successful CSV export workflow
- ✅ Error cases: Invalid inputs and missing data
- ✅ Job lifecycle: Pending → Completed/Failed transitions
- ✅ File download: Correct file generation and download
- ✅ Concurrent requests: Multiple simultaneous exports

### Manual Testing Examples

#### 1. Successful Export Workflow
```bash
# Create export job
curl -X POST "http://localhost:8000/api/export/csv" \
  -H "Content-Type: application/json" \
  -d '{
    "smart_meter_id": "123",
    "start_datetime": "2024-01-01T00:00:00Z",
    "end_datetime": "2024-01-01T00:10:00Z",
    "format": "csv"
  }'

# Check status (replace {job_id} with actual ID)
curl -X GET "http://localhost:8000/api/export/status/{job_id}"

# Download file (replace {job_id} with actual ID)
curl -X GET "http://localhost:8000/api/export/download/{job_id}" \
  -o "smart_meter_export.csv"
```

#### 2. Error Testing
```bash
# Invalid smart meter ID
curl -X POST "http://localhost:8000/api/export/csv" \
  -H "Content-Type: application/json" \
  -d '{
    "smart_meter_id": "999",
    "start_datetime": "2024-01-01T00:00:00Z",
    "end_datetime": "2024-01-01T00:10:00Z",
    "format": "csv"
  }'

# Invalid date range
curl -X POST "http://localhost:8000/api/export/csv" \
  -H "Content-Type: application/json" \
  -d '{
    "smart_meter_id": "123",
    "start_datetime": "2024-01-02T00:00:00Z",
    "end_datetime": "2024-01-01T00:00:00Z",
    "format": "csv"
  }'
```

## CSV Format

The exported CSV includes the following columns:
- `timestamp`: ISO 8601 timestamp
- `smart_meter_id`: Smart meter identifier
- `energy_kwh`: Energy consumption in kilowatt-hours
- `power_kw`: Power in kilowatts
- `voltage_v`: Voltage in volts
- `current_a`: Current in amperes

Example CSV content:
```csv
timestamp,smart_meter_id,energy_kwh,power_kw,voltage_v,current_a
2024-01-01T00:00:00Z,123,0.5,2.1,230.1,9.1
2024-01-01T00:01:00Z,123,0.6,2.3,230.2,9.2
```

## Database Schema

The application uses SQLite with the following `jobs` table:

```sql
CREATE TABLE jobs (
    id TEXT PRIMARY KEY,
    smart_meter_id TEXT NOT NULL,
    start_datetime TEXT NOT NULL,
    end_datetime TEXT NOT NULL,
    status TEXT NOT NULL DEFAULT 'pending',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    file_path TEXT,
    error_message TEXT,
    record_count INTEGER,
    file_size_bytes INTEGER
);
```

## API Documentation

Interactive API documentation is available at:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## Development

### Adding New Features
1. Update models in `models.py` for database changes
2. Add new schemas in `schemas.py` for API contracts
3. Implement endpoints in `main.py`
4. Add background processing logic in `background.py`
5. Write tests in `tests/test_api.py`

### Background Job Processing
The application uses FastAPI's `BackgroundTasks` for asynchronous processing:
- Jobs are created immediately with "pending" status
- Background tasks process the export asynchronously
- Job status is updated to "completed" or "failed"
- Files are stored in the `exports/` directory

## Production Considerations

For production deployment, consider:
- **Database**: Use PostgreSQL or MySQL instead of SQLite
- **Job Queue**: Implement Celery or Redis for robust job processing
- **File Storage**: Use cloud storage (S3, Azure Blob) instead of local files
- **Authentication**: Add API key or OAuth authentication
- **Rate Limiting**: Implement request rate limiting
- **Monitoring**: Add logging and metrics collection
- **Security**: Implement proper input sanitization and file validation

## License

This project is provided as-is for demonstration purposes.

## Support

For issues or questions, please refer to the test suite or API documentation for usage examples. 