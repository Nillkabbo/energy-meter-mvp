# OpenWatt Sandbox API

This is a minimal sandbox environment for candidate developers to demonstrate their ability to work with the OpenWatt software stack.

## Architecture

The sandbox follows the same architecture as the main OpenWatt API:
- FastAPI-based REST API
- Modular router structure
- Configuration management
- Docker containerization

## Quick Start

### Using Docker

```bash
# Build the image
docker build -t openwatt-sandbox-api .

# Run in development mode
docker run -p 8000:8000 -e ENV=dev openwatt-sandbox-api

# Run in production mode
docker run -p 8000:8000 -e ENV=prod openwatt-sandbox-api
```

### Using Docker Compose

```bash
# Run with docker-compose
docker-compose up --build
```

### Local Development

```bash
# Install dependencies
pip install -r requirements.txt

# Run the development server
python -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

## API Endpoints

- `GET /` - Root endpoint with API info
- `GET /health` - Health check
- `GET /api/demo/` - List demo items
- `GET /api/demo/{item_id}` - Get specific demo item
- `POST /api/demo/` - Create new demo item
- `PUT /api/demo/{item_id}` - Update demo item
- `DELETE /api/demo/{item_id}` - Delete demo item
- `GET /api/demo/info/environment` - Environment information

## API Documentation

Once the server is running, visit:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Environment Variables

- `ENV` - Environment (dev/test/prod), defaults to dev
- `JWT_SECRET` - JWT secret key for authentication
- `DATABASE_URL` - Database connection string

## Project Structure

```
api/
├── main.py              # FastAPI application entry point
├── config.py            # Configuration management
├── requirements.txt     # Python dependencies
├── Dockerfile          # Docker configuration
├── README.md           # This file
└── routers/
    ├── __init__.py     # Package initialization
    └── demo.py         # Demo router with example endpoints
``` 