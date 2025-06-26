import os
import sys

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))

# Add current directory to sys.path
if CURRENT_DIR not in sys.path:
  sys.path.insert(0, CURRENT_DIR)

import config
from fastapi import FastAPI, Request
from routers import demo

app = FastAPI(
  title="OpenWatt Sandbox API",
  description="Minimal sandbox environment for candidate developers",
  version="1.0.0",
  root_path='/api'
)

# Include routers
app.include_router(demo.router)

@app.get("/")
async def root():
  """Root endpoint for the sandbox API."""
  return {
    "message": "Welcome to OpenWatt Sandbox API",
    "version": "1.0.0",
    "status": "running"
  }

@app.get("/health")
async def health():
  """Health check endpoint."""
  return {
    "status": "healthy",
    "environment": config.env
  }
