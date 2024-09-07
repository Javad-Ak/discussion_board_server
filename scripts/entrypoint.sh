#!/bin/sh

python manage.py makemigrations accounts discussions
python manage.py migrate

gunicorn --env DJANGO_SETTINGS_MODULE=discussion_board.settings discussion_board.wsgi:application --bind 0.0.0.0:8000