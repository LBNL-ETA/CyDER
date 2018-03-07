from cyder.api.urls import apirouter, urlpatterns

from django.db.models import Q
from django.urls import reverse
from rest_framework import viewsets
from rest_framework.decorators import detail_route, list_route
from rest_framework.response import Response
from rest_framework_nested import routers
from rest_framework.permissions import IsAuthenticated
from .models import *
from .serializers import *
from django.conf.urls import url, include
from django.shortcuts import get_object_or_404

class ModelViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = (IsAuthenticated,)
    queryset = Model.objects.all().order_by('name')
    serializer_class = ModelSerializer
    lookup_field = 'name'

    @list_route(url_path='geojson')
    def list_geojson(self, request):
        models = Model.objects.all()

        features = []
        for model in models:
            first_node = Node.objects.filter(model=model)[0]
            features.append({
                'type': 'Feature',
                'geometry': {
                    'type': 'Point',
                    'coordinates': [first_node.longitude,first_node.latitude]
                    },
                'properties': {
                    'modelname': model.name,
                    'url': 'https://' if request.is_secure() else 'http://' + request.get_host() + reverse('api:model-geojson', args=[model.name])
                    }
                });

        return Response({'type': 'FeatureCollection', 'features': features })

    @detail_route(url_path='geojson')
    def detail_geojson(self, request, name=None):
        model = self.get_object()
        nodes = Node.objects.filter(model=model)
        lines = Device.objects.filter(Q(model=model), Q(device_type=10) | Q(device_type=13)).select_related('section__from_node', 'section__to_node')

        features = []
        for line in lines:
            features.append({
                'type': 'Feature',
                'geometry': {
                    'type': 'LineString',
                    'coordinates': [
                        [line.section.from_node.longitude,line.section.from_node.latitude],
                        [line.section.to_node.longitude,line.section.to_node.latitude]
                        ]
                    },
                'properties': {
                    'section_id': line.section.section_id,
                    'from_node': line.section.from_node.node_id,
                    'to_node': line.section.to_node.node_id,
                    },
                });
        for node in nodes:
            features.append({
                'type': 'Feature',
                'geometry': {
                    'type': 'Point',
                    'coordinates': [node.longitude,node.latitude]
                    },
                'properties' : { 'id' : node.node_id },
                });

        return Response({'type': 'FeatureCollection', 'features': features })
apirouter.register(r'models', ModelViewSet)

models_router = routers.NestedSimpleRouter(apirouter, r'models', lookup='model')

class NodeViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = (IsAuthenticated,)
    queryset = Node.objects.all()
    serializer_class = NodeSerializer
    lookup_field = 'node_id'
    def get_queryset(self):
        model = get_object_or_404(Model.objects.all(), name=self.kwargs['model_name'])
        return Node.objects.filter(model=model)
models_router.register(r'nodes', NodeViewSet, base_name='model-nodes')

class DeviceViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = (IsAuthenticated,)
    queryset = Device.objects.all()
    serializer_class = DeviceSerializer
    lookup_field = 'id'
    def get_queryset(self):
        model = get_object_or_404(Model.objects.all(), name=self.kwargs['model_name'])
        return Device.objects.filter(model=model)
models_router.register(r'devices', DeviceViewSet, base_name='model-devices')

class LoadViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = (IsAuthenticated,)
    queryset = Load.objects.all().select_related('device')
    serializer_class = LoadSerializer
    lookup_field = 'device'
    def get_queryset(self):
        model = get_object_or_404(Model.objects.all(), name=self.kwargs['model_name'])
        return Load.objects.select_related('device').filter(device__model=model)
models_router.register(r'loads', LoadViewSet, base_name='model-loads')

class PVViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = (IsAuthenticated,)
    queryset = PV.objects.all().select_related('device')
    serializer_class = PVSerializer
    lookup_field = 'device'
    def get_queryset(self):
        model = get_object_or_404(Model.objects.all(), name=self.kwargs['model_name'])
        return PV.objects.select_related('device').filter(device__model=model)
models_router.register(r'pvs', PVViewSet, base_name='model-pvs')

urlpatterns.append(url(r'^', include(models_router.urls)))
