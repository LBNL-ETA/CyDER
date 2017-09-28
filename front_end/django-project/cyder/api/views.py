from cyder.grid_models.models import Model
from rest_framework import viewsets
from .serializers import ModelSerializer

class ModelViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Model.objects.all()
    serializer_class = ModelSerializer
