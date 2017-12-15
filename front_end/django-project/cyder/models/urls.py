from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.model_viewer, name='model_viewer'),
    url(r'^(?P<modelname>[0-9a-zA-Z _()]*)/$', views.model_viewer, name='model_viewer'),
]
