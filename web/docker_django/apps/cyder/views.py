from __future__ import division
from django.shortcuts import render, redirect
from django.shortcuts import get_list_or_404, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
import models as m
import form as f
import api
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
def my_projects(request):
    queryset = get_list_or_404(m.UserModel, user=request.user)
    serializer = s.UserModelSerializer(queryset, many=True)
    return render(request, 'my_projects.html', {'my_projects': serializer.data})


@login_required
def my_project_settings(request, id):
    return render(request, 'my_project_settings.html', {'usermodel_id': id})


@login_required
def my_project_scenarios(request, id):
    usermodel = get_object_or_404(m.UserModel, pk=id)
    scenario, created = m.ElectricVehicleScenario.objects.get_or_create(usermodel=usermodel)
    if request.method == "POST":
        form = f.ElectricVehicleScenarioForm(request.POST, instance=scenario)
        if form.is_valid():
            scenario = form.save(commit=False)
            scenario.save()
            return redirect('my_project_settings', id=id)
    else:
        form = f.ElectricVehicleScenarioForm(instance=scenario)
    return render(request, 'my_project_scenarios.html', {'usermodel_id': id, 'form': form})


@login_required
def my_project_review(request, id):
    result_dict = {}
    result_dict['usermodel_id'] = id
    usermodel = get_object_or_404(m.UserModel, id=id)
    model = get_object_or_404(m.Model, id=usermodel.model_id)
    result_dict['model'] = s.DetailModelSerializer(model).data
    return render(request, 'my_project_review.html', result_dict)


@login_required
def my_project_general_settings(request, id):
    instance = get_object_or_404(m.UserModel, id=id)
    form = f.UserModelDescriptionForm(request.POST or None, instance=instance)
    if form.is_valid():
        form.save()
        messages.add_message(request, messages.SUCCESS, 'The description was updated!')

    return render(request, 'my_project_general_settings.html', {'form': form, 'usermodel_id': id, 'model_id': form.instance.model.id})


@login_required
def my_project_add_devices(request, id):
    user_model = get_object_or_404(m.UserModel, id=id)
    return render(request, 'my_project_add_devices.html', {'usermodel_id': id, 'model_id': user_model.model.id})


@login_required
def show_upmu_data(request):
    return render(request, 'upmu_visualization.html', {})


@login_required
def show_node_result(request, id):
    return render(request, 'node_result_visualization.html', {'simulation_id': id})
