from __future__ import division
from django.shortcuts import get_list_or_404, get_object_or_404
from django.contrib.auth.decorators import login_required
from rest_framework import viewsets, mixins, status
from rest_framework.response import Response
from rest_framework.decorators import detail_route, list_route
from rest_framework.decorators import api_view
import models as m
import calibration as c
import upmu as u
import simulation as sim
import serializers as s
import filter as filt
import datetime
import traceback

# from redis import Redis
# redis = Redis(host='redis', port=6379)


class ModelViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = m.CalibrationHistory.objects.all()

    def list(self, request):
        serializer = s.ModelSerializer(m.Model.objects.all(), many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        serializer = s.DetailModelSerializer(get_object_or_404(m.Model, id=pk))
        return Response(serializer.data)


class CalibrationViewSet(mixins.RetrieveModelMixin,
                         mixins.ListModelMixin,
                         viewsets.GenericViewSet):
    filter_backends = (filt.CalibrationHistoryFilter,)
    queryset = m.CalibrationHistory.objects.all()
    pagination_class = None

    def list(self, request):
        model_id = request.GET.get("model_id", None)
        queryset = m.CalibrationHistory.objects.filter(model_id=model_id)
        serializer = s.CalibrationHistorySerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        query = get_object_or_404(m.CalibrationHistory, id=pk)
        serializer = s.SingleCalibrationHistorySerializer(query)
        return Response(serializer.data)

    @detail_route(methods=['POST'], serializer_class=s.ActionSerializer)
    def calibration(self, request, pk):
        try:
            data = c.calibrate(pk)
        except:
            return Response({'error': str(traceback.format_exc())})
        return Response(data)


class ProjectViewSet(mixins.RetrieveModelMixin,
                       mixins.ListModelMixin,
                       viewsets.GenericViewSet):
    queryset = m.Project.objects.all()

    def retrieve(self, request, pk):
        serializer = s.ProjectSerializer(get_object_or_404(m.Project, id=pk))
        return Response(serializer.data)

    def list(sefl, request):
        queryset = get_list_or_404(m.Project, user=request.user)
        serializer = s.ProjectSerializer(queryset, many=True)
        return Response(serializer.data)

    @detail_route(methods=['POST'], serializer_class=s.ActionSerializer)
    def simulate(self, request, pk):
        try:
            # Change simulation status
            project = m.Project.objects.get(id=pk)
            project.in_progress = True
            project.save()

            # Launch simulation
            sim.simulate(pk)
        except:
            project.status = str(traceback.format_exc())
            project.save()
            return Response({'error': str(traceback.format_exc())})

        # Change status to done
        project.in_progress = False
        project.status = "Success"
        project.result_available = True
        project.save()
        return Response({'status': 'success'})


class NodeResultViewSet(mixins.ListModelMixin,
                        viewsets.GenericViewSet):
    filter_backends = (filt.NodeResultFilter,)
    queryset = m.NodeResult.objects.all()
    pagination_class = None

    def list(self, request):
        sim_id = request.GET.get("simulation_id", None)
        node_id = request.GET.get("node_id", None)
        if node_id:
            queryset = m.NodeResult.objects.filter(project_model=sim_id, node_id=node_id)
        else:
            queryset = m.NodeResult.objects.filter(project_model=sim_id)
        serializer = s.NodeResultSerializer(queryset, many=True)
        return Response(serializer.data)


class NodeViewSet(mixins.ListModelMixin,
                  viewsets.GenericViewSet):
    filter_backends = (filt.NodeFilter,)
    queryset = m.Node.objects.all()
    pagination_class = None

    def list(self, request):
        model_id = request.GET.get("model_id", None)
        if model_id:
            queryset = m.Node.objects.filter(model_id=model_id)
        else:
            return Response({'status': 'Require a model_id parameter'}, status=status.HTTP_400_BAD_REQUEST)

        serializer = s.NodeSerializer(queryset, many=True)
        return Response(serializer.data)


class ElectricVehicleScenarioViewSet(mixins.RetrieveModelMixin,
                                     mixins.CreateModelMixin,
                                     viewsets.GenericViewSet):
    queryset = m.ElectricVehicleScenario.objects.all()
    serializer_class = s.ElectricVehicleScenarioSerializer

    def retrieve(self, request, pk=None):
        serializer = s.ElectricVehicleScenarioSerializer(get_object_or_404(m.ElectricVehicleScenario, project_model=pk))
        return Response(serializer.data)

    def create(self, request):
        serializer = s.ElectricVehicleScenarioSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response({'status': 'success'})


@api_view(['GET'])
def upmu(request, date_from, date_to, location):
    """
    List all snippets, or create a new snippet.
    """
    if request.method == 'GET':
        # Prepare input
        date_from = datetime.datetime.strptime(date_from, "%Y-%m-%d_%H:%M:%S")
        if date_to not in "False":
            date_to = datetime.datetime.strptime(date_to, "%Y-%m-%d_%H:%M:%S")
        else:
            date_to = False

        return_dict = {}
        return_dict['data'] = u.get(location, date_from, date_to)
        return Response(return_dict)

# SNIPET
# class MyView(mixins.CreateModelMixin,
#                        mixins.RetrieveModelMixin,
#                        mixins.UpdateModelMixin,
#                        mixins.DestroyModelMixin,
#                        mixins.ListModelMixin,
#                        GenericViewSet):

# serializer = s.PkSerializer(data=request.data)
# if serializer.is_valid():
#     return Response(serializer.data)
# else:
#     return Response(serializer.errors,
#                     status=status.HTTP_400_BAD_REQUEST)
