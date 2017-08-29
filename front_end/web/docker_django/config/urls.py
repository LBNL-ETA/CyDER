"""
Cyder django project urls.

Included apps are:
    - admin
    - cyder
"""

from django.conf.urls import include
from django.conf.urls import url
from django.contrib import admin

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^', include('docker_django.apps.cyder.urls')),
    url('^accounts/', include('django.contrib.auth.urls')),
]
