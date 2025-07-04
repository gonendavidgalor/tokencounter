#!/bin/bash
# Use PORT environment variable provided by Render
uvicorn server:app --host 0.0.0.0 --port ${PORT:-8000}
