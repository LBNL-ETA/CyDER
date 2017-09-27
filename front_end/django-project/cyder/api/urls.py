from django.conf.urls import url
from . import geojson

urlpatterns = [
    url(r'^geojson/models$', geojson.models_list),
    url(r'^geojson/models/(?P<modelfile>[0-9a-zA-Z.]+)$', geojson.get_model),
]
