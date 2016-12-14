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
        'test': {
            'task': 'test',
            'schedule': timedelta(seconds=60),
        },
    }
    return CELERYBEAT_SCHEDULE


def return_CELERYBEAT_ROUTES():
    CELERYBEAT_ROUTES = {
                'apps.cyder.periodic_tasks.test': {'queue': 'web_framework'},
                }
    return CELERYBEAT_ROUTES
