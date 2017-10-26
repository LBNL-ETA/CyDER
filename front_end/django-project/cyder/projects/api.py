from cyder.api.urls import apirouter, urlpatterns

from rest_framework import status
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import detail_route, list_route
from .models import Project
from .serializers import ProjectSerializer
from django.shortcuts import get_object_or_404
from celery.result import AsyncResult
import sim_worker.celery
import sim_worker.tasks

class ProjectViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    lookup_field = 'id'

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        if instance.status == "Started" or instance.status == "Pending":
            return Response({ "detail" : "Can't update a project when it is currently in simulation" }, status=status.HTTP_401_UNAUTHORIZED)
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
            return Response({ "detail" : "Can't delete a project when it is currently in simulation" }, status=status.HTTP_401_UNAUTHORIZED)
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

    @detail_route(methods=['post'])
    def revoke(self, request, *args, **kwargs):
        project = self.get_object()
        task = AsyncResult(project.task_id, app=sim_worker.celery.app)
        task.revoke(terminate=True)
        task.forget()
        project.status = "NeedSim"
        project.save()
        return Response({ "detail": "Project simulation revoked" })

    @detail_route(methods=['post'])
    def run(self, request, *args, **kwargs):
        project = self.get_object()
        if project.status == "Started" or project.status == "Pending":
            return Response({ "detail" : "Can't run a simulation on a project when it is currently in simulation" }, status=status.HTTP_401_UNAUTHORIZED)
        task = sim_worker.tasks.run_simulation.delay(None)
        project.task_id = task.id
        project.status = "Pending"
        project.save()
        return Response({ "detail": "Simulation requested for this project" })

apirouter.register(r'projects', ProjectViewSet)
