from django.conf.urls import url, include
from rest_framework import routers
from . import geojson
from . import views

router = routers.DefaultRouter()
router.register(r'models', views.ModelViewSet)

urlpatterns = [
    url(r'^geojson/models$', geojson.models_list),
    url(r'^geojson/models/(?P<modelfile>[0-9a-zA-Z.]+)$', geojson.get_model),
    url(r'^', include(router.urls)),
]
