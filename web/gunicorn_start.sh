#!/bin/bash
DJANGODIR=/usr/src/app/docker_django             # Django project direct
DJANGO_SETTINGS_MODULE=docker_django.settings    # which settings file should Django use
DJANGO_WSGI_MODULE=docker_django.wsgi            # WSGI module name

export DJANGO_SETTINGS_MODULE=$DJANGO_SETTINGS_MODULE
export PYTHONPATH=$DJANGODIR:$PYTHONPATH

# Start your Django Unicorn
exec /usr/local/bin/gunicorn ${DJANGO_WSGI_MODULE}:application -w 2 -b :8000
