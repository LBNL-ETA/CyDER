from __future__ import division
from django.shortcuts import render, redirect
from django.shortcuts import get_list_or_404, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
import models as m
import form as f
import api
import ast
from rest_framework import viewsets, mixins, status
from rest_framework.response import Response
from rest_framework.decorators import detail_route, list_route
from rest_framework.decorators import api_view
import serializers as s
import datetime
import upmu as u
import calibration as c
import simulation as sim
import sys
import traceback
import filter as filt


@login_required
def home(request):
    return render(request, 'home.html', {})


@login_required
def model(request, id):
    result_dict = {}
    model = get_object_or_404(m.Model, id=id)
    result_dict['model'] = s.DetailModelSerializer(model).data
    return render(request, 'model.html', result_dict)


@login_required
def calibration(request, id):
    query = get_object_or_404(m.CalibrationHistory, id=id)
    serializer = s.SingleCalibrationHistorySerializer(query)
    return render(request, 'calibration.html', serializer.data)


@login_required
def my_models(request):
    return render(request, 'my_models.html', api.my_models_info_dict(request))


@login_required
def my_models_settings(request, id):
    return render(request, 'my_models_settings.html', {'usermodel_id': id})

@login_required
def my_models_scenarios(request, id):
    usermodel = get_object_or_404(m.UserModel, pk=id)
    scenario, created = m.ElectricVehicleScenario.objects.get_or_create(usermodel=usermodel)
    if request.method == "POST":
        form = f.ElectricVehicleScenarioForm(request.POST, instance=scenario)
        if form.is_valid():
            scenario = form.save(commit=False)
            scenario.save()
            return redirect('my_models_settings', id=id)
    else:
        form = ElectricVehicleScenarioForm(instance=scenario)
    return render(request, 'my_models_scenarios.html', {'usermodel_id': id, 'form': form})


@login_required
def my_models_review(request, id):
    result_dict = {}
    result_dict['usermodel_id'] = id
    usermodel = get_object_or_404(m.UserModel, id=id)
    model = get_object_or_404(m.Model, id=usermodel.model_id)
    result_dict['model'] = s.DetailModelSerializer(model).data
    return render(request, 'my_models_review.html', result_dict)


@login_required
def my_models_general_settings(request, id):
    instance = get_object_or_404(UserModel, id=id)
    form = f.UserModelDescriptionForm(request.POST or None, instance=instance)
    if form.is_valid():
        form.save()
        messages.add_message(request, messages.SUCCESS, 'The description was updated!')

    return render(request, 'my_models_general_settings.html', {'form': form, 'usermodel_id': id, 'model_id': form.instance.model.id})


@login_required
def my_models_add_devices(request, id):
    user_model = get_object_or_404(m.UserModel, id=id)
    return render(request, 'my_models_add_devices.html', {'usermodel_id': id, 'model_id': user_model.model.id})


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


class UserModelViewSet(mixins.RetrieveModelMixin,
                       viewsets.GenericViewSet):
    queryset = m.UserModel.objects.all()
    # http_method_names = ['get', 'head', 'post']

    def retrieve(self, request, pk):
        serializer = s.UserModelSerializer(get_object_or_404(m.UserModel, id=pk))
        return Response(serializer.data)

    @detail_route(methods=['POST'], serializer_class=s.ActionSerializer)
    def simulate(self, request, pk):
        try:
            # Change simulation status
            usermodel = m.UserModel.objects.get(id=pk)
            usermodel.in_progress = True
            usermodel.save()

            # Launch simulation
            sim.simulate(pk)
        except:
            usermodel.status = str(traceback.format_exc())
            usermodel.save()
            return Response({'error': str(traceback.format_exc())})

        # Change status to done
        usermodel.in_progress = False
        usermodel.status = "Success"
        usermodel.result_available = True
        usermodel.save()
        return Response({'status': 'success'})

    # @detail_route(methods=['POST'], serializer_class=s.ActionSerializer)
    # def general_settings(self, request, pk):
    #     instance = get_object_or_404(UserModel, id=id)
    #     form = UserModelDescriptionForm(request.POST or None, instance=instance)


class NodeResultViewSet(mixins.ListModelMixin,
                        viewsets.GenericViewSet):
    filter_backends = (filt.NodeResultFilter,)
    queryset = m.NodeResult.objects.all()
    pagination_class = None

    def list(self, request):
        sim_id = request.GET.get("simulation_id", None)
        node_id = request.GET.get("node_id", None)
        if node_id:
            queryset = m.NodeResult.objects.filter(usermodel=sim_id, node_id=node_id)
        else:
            queryset = m.NodeResult.objects.filter(usermodel=sim_id)
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
        serializer = s.ElectricVehicleScenarioSerializer(get_object_or_404(m.ElectricVehicleScenario, usermodel_id=pk))
        return Response(serializer.data)

    def create(self, request):
        serializer = s.ElectricVehicleScenarioSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
            # usermodel = get_object_or_404(m.UserModel, id=serializer.data['usermodel'])
            # m.ElectricVehicleScenario.objects.create(usermodel=usermodel, **serializer.data)
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


# @api_view(['GET'])
# def calibration(request, id):
#     """
#     List all snippets, or create a new snippet.
#     """
#     if request.method == 'GET':
#         try:
#             data = c.calibrate(id)
#         except:
#             return Response({'error': str(traceback.format_exc())})
#         return Response(data)


@login_required
def show_upmu_data(request):
    return render(request, 'upmu_visualization.html', {})


@login_required
def show_node_result(request, id):
    return render(request, 'node_result_visualization.html', {'simulation_id': id})

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
