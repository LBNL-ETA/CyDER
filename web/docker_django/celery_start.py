from __future__ import absolute_import
import os
from celery import Celery
from django.conf import settings
import docker_django.celery_config
import docker_django.settings

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'docker_django.settings')
app = Celery('cyder')

# Using a string here means the worker will not have to
# pickle the object when using Windows.
app.config_from_object(docker_django.celery_config)
app.autodiscover_tasks(lambda: docker_django.settings.INSTALLED_APPS)
