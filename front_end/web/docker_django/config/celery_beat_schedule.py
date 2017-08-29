"""
Usage:

# Task executed at 11pm everyday
'schedule': crontab(minute=0, hour=23)

# Task executed every minutes
'schedule': timedelta(seconds=60)
"""

from __future__ import absolute_import
from celery.schedules import crontab
from datetime import timedelta


def return_CELERYBEAT_SCHEDULE():
    CELERYBEAT_SCHEDULE = {
        'calibrate all the models':{
            'task': 'docker_django.apps.cyder.periodic_tasks.calibrate_models',
            'schedule': timedelta(hours=12),
        },
    }
    return CELERYBEAT_SCHEDULE


def return_CELERYBEAT_ROUTES():
    CELERYBEAT_ROUTES = {
                'docker_django.apps.cyder.periodic_tasks.calibrate_models': {'queue': 'web_framework'},
                }
    return CELERYBEAT_ROUTES
