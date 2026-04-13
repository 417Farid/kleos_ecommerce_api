#!/bin/sh

echo "Running Alembic migrations..."
python -m alembic upgrade head

echo "Starting the application..."
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000