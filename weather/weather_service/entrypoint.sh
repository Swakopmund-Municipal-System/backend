#!/usr/bin/env bash
set -e

python manage.py collectstatic --noinput
python -m gunicorn --bind 0.0.0.0:8011 --workers 3 service.wsgi:application
