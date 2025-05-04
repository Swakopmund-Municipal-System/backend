#!/bin/bash

# Apply database migrations
python manage.py migrate

python manage.py collectstatic --noinput --clear



# Start server
exec "$@"
