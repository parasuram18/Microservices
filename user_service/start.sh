#!/bin/bash

# Exit immediately if a command exits with a non-zero status
set -e

# Run Alembic migrations
echo "Running database migrations..."
alembic upgrade head

# Start the FastAPI app with uvicorn
echo "Starting FastAPI app..."
exec uvicorn main:app --host 0.0.0.0 --port 8000
