from cyder.api.urls import apirouter

from django.db.models import Q
from django.urls import reverse
from rest_framework import viewsets
from rest_framework.decorators import detail_route, list_route
from rest_framework.response import Response
from .models import Model, Node, Device, Section
from .serializers import ModelSerializer

class ModelViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Model.objects.all()
    serializer_class = ModelSerializer
    lookup_field = 'name'

    @list_route(url_path='geojson')
    def list_geojson(self, request):
        models = Model.objects.all()

        features = []
        for model in models:
            first_node = Node.objects.filter(model=model)[0]
            features.append({
                "type": "Feature",
                "geometry": {
                    "type": "Point",
                    "coordinates": [first_node.longitude,first_node.latitude]
                    },
                "properties": {
                    "modelname": model.name,
                    "url": 'https://' if request.is_secure() else 'http://' + request.get_host() + reverse("api:model-geojson", args=[model.name])
                    }
                });

        return Response({"type": "FeatureCollection", "features": features })

    @detail_route(url_path='geojson')
    def detail_geojson(self, request, name=None):
        model = Model.objects.get(name=name)
        nodes = Node.objects.filter(model=model)
        lines = Device.objects.filter(Q(model=model), Q(device_type=10) | Q(device_type=13)).select_related('section__from_node', 'section__to_node')

        features = []
        for line in lines:
            features.append({
                "type": "Feature",
                "geometry": {
                    "type": "LineString",
                    "coordinates": [
                        [line.section.from_node.longitude,line.section.from_node.latitude],
                        [line.section.to_node.longitude,line.section.to_node.latitude]
                        ]
                    },
                });
        for node in nodes:
            features.append({
                "type": "Feature",
                "geometry": {
                    "type": "Point",
                    "coordinates": [node.longitude,node.latitude]
                    },
                });

        return Response({"type": "FeatureCollection", "features": features })

apirouter.register(r'models', ModelViewSet)
