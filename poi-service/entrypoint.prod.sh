#!/usr/bin/env bash

python manage.py collectstatic --noinput
python manage.py migrate --noinput
python -m gunicorn --bind 0.0.0.0:8009 --workers 3 service.wsgi:application