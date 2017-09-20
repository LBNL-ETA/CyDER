from django.conf.urls import url
from . import views
from . import geojson

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^model_viewer/(?P<modelfile>[0-9a-zA-Z.]*)$', views.model_viewer, name='model_viewer'),
    
    # geojson
    url(r'^geojson/models$', geojson.models_list),
    url(r'^geojson/models/(?P<modelfile>[0-9a-zA-Z.]+)$', geojson.get_model),
]
