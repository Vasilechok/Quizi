#!/usr/bin/env bash
set -e

cd /app/quiz_project

python manage.py migrate --noinput

python manage.py runserver 0.0.0.0:8000




