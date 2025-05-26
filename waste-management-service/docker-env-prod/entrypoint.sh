#!/bin/bash

alembic upgrade head

echo "Starting app with Gunicorn..."
exec gunicorn --bind 0.0.0.0:8004 -w 4 -k uvicorn.workers.UvicornWorker run:app