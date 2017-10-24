from cyder.api.urls import apirouter, urlpatterns

from rest_framework import status
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import detail_route, list_route
from .models import Project
from .serializers import ProjectSerializer
from django.shortcuts import get_object_or_404
from sim_worker.celery import app

class ProjectViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    lookup_field = 'id'

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        if instance.status == "Started" or instance.status == "Pending":
            return Response({ "error" : "Can't update a project when it is currently in simulation" }, status=status.HTTP_401_UNAUTHORIZED)
        instance.status = "NeedSim"
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.status == "Started" or instance.status == "Pending":
            return Response({ "error" : "Can't delete a project when it is currently in simulation" }, status=status.HTTP_401_UNAUTHORIZED)
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

    @detail_route(methods=['post'])
    def revoke(self, request, *args, **kwargs):
        project = self.get_object()
        app.control.revoke(project.task_id)
        project.status = "NeedSim"
        return Response({ "status": "Project simulation revoked" })

apirouter.register(r'projects', ProjectViewSet)
