from __future__ import absolute_import
import os
from celery import Celery
from django.conf import settings
import celery_config

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings')
app = Celery('cyder')

# Using a string here means the worker will not have to
# pickle the object when using Windows.
app.config_from_object(celery_config)
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
