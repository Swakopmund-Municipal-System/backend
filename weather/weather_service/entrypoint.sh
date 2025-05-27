#!/usr/bin/env bash

python manage.py collectstatic --noinput
python -m gunicorn --bind 0.0.0.0:8002 --workers 3 service.wsgi:application
