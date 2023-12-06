#!/bin/sh

set -e

python manage.py migrate --no-input
gunicorn exercise.wsgi -b 0.0.0.0:8000 --reload
