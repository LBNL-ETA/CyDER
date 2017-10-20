from cyder.api.urls import apirouter, urlpatterns

from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Project
from .serializers import ProjectSerializer
from django.shortcuts import get_object_or_404

class ProjectViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    lookup_field = 'id'
apirouter.register(r'projects', ProjectViewSet)
