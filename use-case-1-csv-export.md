# Use Case 1: Smart Meter CSV Export

## Overview

Implement a CSV export system for smart meter data that processes requests asynchronously using background jobs. This exercise demonstrates your ability to work with:

- RESTful API design
- Background job processing
- File generation and storage
- Error handling and status tracking
- Database operations

## Requirements

### 1. CSV Export Endpoint

Create a POST endpoint that accepts smart meter export requests:

**Endpoint**: `POST /api/export/csv`

**Request Body**:
```json
{
  "smart_meter_id": "string",
  "start_datetime": "2024-01-01T00:00:00Z",
  "end_datetime": "2024-01-31T23:59:59Z",
  "format": "csv"
}
```

**Response**:
```json
{
  "job_id": "uuid-string",
  "status": "pending",
  "message": "Export job created successfully"
}
```

### 2. Job Status Endpoint

Create a GET endpoint to check job status:

**Endpoint**: `GET /api/export/status/{job_id}`

**Response - Pending**:
```json
{
  "job_id": "uuid-string",
  "status": "pending",
  "message": "Job is being processed",
  "created_at": "2024-01-01T10:00:00Z",
  "updated_at": "2024-01-01T10:00:00Z"
}
```

**Response - Completed**:
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

**Response - Failed**:
```json
{
  "job_id": "uuid-string",
  "status": "failed",
  "message": "Export failed",
  "created_at": "2024-01-01T10:00:00Z",
  "updated_at": "2024-01-01T10:01:15Z",
  "error": {
    "code": "SMART_METER_NOT_FOUND",
    "message": "Smart meter with ID '123' not found",
    "details": "The specified smart meter does not exist in the system"
  }
}
```

**Response - Not Found**:
```json
{
  "status": "not_found",
  "message": "Job with ID 'uuid-string' not found"
}
```

### 3. File Download Endpoint

Create a GET endpoint to download completed CSV files:

**Endpoint**: `GET /api/export/download/{job_id}`

**Response**: CSV file with appropriate headers:
- `Content-Type: text/csv`
- `Content-Disposition: attachment; filename="smart_meter_123_20240101_20240131.csv"`

## Technical Implementation

### Background Job Processing

You should implement a simple background job system. Options include:

1. **Threading**: Use Python's `threading` module for simple background processing
2. **Celery**: For more robust job queuing (optional enhancement)
3. **Async/Await**: Use FastAPI's background tasks

### Data Storage

- **Job Status**: Store job information in a database table
- **CSV Files**: Store generated files in a designated directory
- **Smart Meter Data**: Use mock data or create a simple data structure

### CSV Format

The exported CSV should include:
- Timestamp (ISO format)
- Smart meter ID
- Energy consumption (kWh)
- Power (kW)
- Voltage (V)
- Current (A)

Example CSV structure:
```csv
timestamp,smart_meter_id,energy_kwh,power_kw,voltage_v,current_a
2024-01-01T00:00:00Z,123,0.5,2.1,230.1,9.1
2024-01-01T00:01:00Z,123,0.6,2.3,230.2,9.2
```

## Error Handling

Implement proper error handling for:

- Invalid smart meter ID
- Invalid date ranges (end before start)
- Date ranges too large (e.g., > 1 year)
- Missing required fields
- Job processing failures
- File generation errors

## Validation Rules

- Smart meter ID: Required, string format
- Start datetime: Required, ISO 8601 format, must be in the past
- End datetime: Required, ISO 8601 format, must be after start datetime
- Maximum date range: 1 year
- Minimum date range: 1 minute

## Database Schema

Create a `jobs` table with the following structure:

```sql
CREATE TABLE jobs (
    id UUID PRIMARY KEY,
    smart_meter_id VARCHAR NOT NULL,
    start_datetime TIMESTAMP NOT NULL,
    end_datetime TIMESTAMP NOT NULL,
    status VARCHAR NOT NULL DEFAULT 'pending',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    file_path VARCHAR,
    error_message TEXT,
    record_count INTEGER,
    file_size_bytes BIGINT
);
```

## Testing Requirements

Implement tests for:

1. **Happy path**: Successful CSV export
2. **Error cases**: Invalid inputs, missing data
3. **Job lifecycle**: Pending → Completed/Failed
4. **File download**: Correct file generation and download
5. **Concurrent requests**: Multiple simultaneous exports

## Bonus Features (Optional)

- **Progress tracking**: Show percentage completion
- **Email notifications**: Notify when export is ready
- **Export history**: List all exports for a smart meter
- **Export scheduling**: Schedule recurring exports
- **Multiple formats**: Support JSON, XML exports
- **Compression**: Gzip CSV files for large exports

## Submission

Submit your implementation with:

1. **Code**: All source files
2. **Tests**: Unit and integration tests
3. **Documentation**: API documentation and setup instructions
4. **Database**: Migration scripts or schema
5. **README**: How to run and test the implementation

## Evaluation Criteria

- **Code quality**: Clean, readable, well-structured code
- **API design**: RESTful principles, proper HTTP status codes
- **Error handling**: Comprehensive error scenarios
- **Testing**: Good test coverage
- **Documentation**: Clear API documentation
- **Performance**: Efficient background processing
- **Security**: Proper input validation and file handling
