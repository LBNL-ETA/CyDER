from __future__ import absolute_import
from celery.schedules import crontab
from docker_django.celery_beat_schedule import return_CELERYBEAT_SCHEDULE, return_CELERYBEAT_ROUTES
from datetime import timedelta

# Celery settings
BROKER_URL = "redis://redis:6379/0"
CELERY_RESULT_BACKEND = "redis://redis:6379/0"
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_ACCEPT_CONTENT = ['json']

# give message to another worker after 15 seconds
BROKER_TRANSPORT_OPTIONS = {'visibility_timeout': 15}

# restart workers
CELERYD_POOL_RESTARTS = True

 # delete result after 15 minutes:
CELERY_TASK_RESULT_EXPIRES = 900

# hello?
BROKER_POOL_LIMIT = 0

CELERY_ROUTES = return_CELERYBEAT_ROUTES()

CELERY_IMPORTS = ("docker_django.apps.cyder.periodic_tasks")

CELERYBEAT_SCHEDULE = return_CELERYBEAT_SCHEDULE()

CELERYD_PREFETCH_MULTIPLIER = 1
CELERY_TIMEZONE = 'US/Pacific'
