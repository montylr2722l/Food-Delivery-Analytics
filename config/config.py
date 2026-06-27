import os

# Project root directory
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Data directories
RAW_DATA_DIR = os.path.join(PROJECT_ROOT, 'data', 'raw')

# Ensure directories exist
os.makedirs(RAW_DATA_DIR, exist_ok=True)
