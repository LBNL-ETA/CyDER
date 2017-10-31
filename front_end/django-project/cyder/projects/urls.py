from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.projects, name='projects'),
    url(r'^create$', views.create, name='createproject'),
    url(r'^edit/(?P<project_id>[0-9]*)$', views.edit, name='editproject'),
    url(r'^results/(?P<project_id>[0-9]*)$', views.results, name='projectresults'),
]
