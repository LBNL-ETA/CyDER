from django.conf.urls import url, include
from rest_framework import routers
from rest_framework.authtoken import views as token_views
from . import views

apirouter = routers.DefaultRouter()
urlpatterns = [
    url(r'^token-auth/$', token_views.obtain_auth_token),
    url(r'^token-session/$', views.token_from_session),
]

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
