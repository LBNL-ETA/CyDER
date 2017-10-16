from django.conf.urls import url, include
from rest_framework import routers

apirouter = routers.DefaultRouter()
urlpatterns = []

# Import the api.py from each cyder.* app installed
import re
import importlib
from django.apps import apps
apps = apps.get_app_configs()
regex = re.compile(r'^cyder.')
for app in apps:
    if regex.match(app.name):
        try:
            importlib.import_module(app.name + '.api')
        except ModuleNotFoundError:
            pass

urlpatterns.append(url(r'^', include(apirouter.urls)))
