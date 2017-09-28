from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^(?P<modelname>[0-9a-zA-Z.]*)$', views.model_viewer, name='model_viewer'),
]
