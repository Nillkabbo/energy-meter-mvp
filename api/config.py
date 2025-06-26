import os
import json
from pathlib import Path

# Environment setup
env = os.environ.get('ENV', 'dev')

# Base directory
current_dir = os.path.dirname(os.path.abspath(__file__))
base_dir = Path(current_dir).parent

# Basic configuration
config = {
  'dev': {
    'debug': True,
    'host': '0.0.0.0',
    'port': 8000,
    'log_level': 'DEBUG'
  },
  'test': {
    'debug': False,
    'host': '0.0.0.0',
    'port': 8000,
    'log_level': 'INFO'
  },
  'prod': {
    'debug': False,
    'host': '0.0.0.0',
    'port': 8000,
    'log_level': 'WARNING'
  }
}

# Get current environment config
env_config = config.get(env, config['dev'])

# API settings
API_TITLE = "OpenWatt Sandbox API"
API_VERSION = "1.0.0"
API_DESCRIPTION = "Minimal sandbox environment for candidate developers"

# JWT settings (simplified for sandbox)
JWT_SECRET = os.environ.get("JWT_SECRET", "sandbox-secret-key-change-in-production")
JWT_ALGORITHM = "HS256"
JWT_EXPIRATION_HOURS = 24

# Database settings (placeholder for sandbox)
DATABASE_URL = os.environ.get("DATABASE_URL", "sqlite:///./sandbox.db")

# Logging
LOG_LEVEL = env_config['log_level']
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s" 