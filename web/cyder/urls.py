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
    url(r'^', include('cyder.apps.cyder.urls')),
]
