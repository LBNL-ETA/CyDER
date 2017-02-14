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
def show_upmu_data(request):
    return render(request, 'upmu_visualization.html', {})


@login_required
def create_project(request):
    form = f.ProjectCreationForm(request.POST or None)
    if form.is_valid():
        obj = form.save(commit=False)
        obj.user = request.user
        obj.last_modified = datetime.datetime.now()
        obj.save()
        return redirect('my_projects')
    return render(request, 'create_project.html', {'form': form})


@login_required
def my_projects(request):
    queryset = m.Project.objects.filter(user=request.user)
    if queryset:
        serializer = s.ProjectSerializer(queryset, many=True)
        return render(request, 'my_projects.html', {'my_projects': serializer.data})
    else:
        return render(request, 'my_projects.html')


@login_required
def my_project_settings(request, id):
    instance = get_object_or_404(m.Project, id=id)
    form = f.ProjectDescriptionForm(request.POST or None, instance=instance)
    if form.is_valid():
        form.save()
        messages.add_message(request, messages.SUCCESS, 'The description was updated!')

    return render(request, 'my_project/settings.html', {'form': form, 'project_id': id})


@login_required
def my_project_review(request, id):
    result_dict = {}
    result_dict['project_id'] = id
    project = get_object_or_404(m.Project, id=id)
    project_models = get_list_or_404(m.ProjectModels, id=project_id)
    result_dict['model'] = s.DetailModelSerializer(project_models[0].model).data
    return render(request, 'my_project/review.html', result_dict)


@login_required
def my_project_node_result(request, id):
    return render(request, 'my_project/node_result_visualization.html', {'simulation_id': id})


@login_required
def my_model_settings(request):
    return redirect('my_projects')


@login_required
def my_model_scenarios(request, id):
    project_model = get_object_or_404(m.ProjectModel, pk=id)
    scenario, created = m.ElectricVehicleScenario.objects.get_or_create(project_model=project_model)
    if request.method == "POST":
        form = f.ElectricVehicleScenarioForm(request.POST, instance=scenario)
        if form.is_valid():
            scenario = form.save(commit=False)
            scenario.save()
            return redirect('my_project/settings', id=id)
    else:
        form = f.ElectricVehicleScenarioForm(instance=scenario)
    return render(request, 'my_project/my_model/scenarios.html', {'project_id': project_model.project_id, 'form': form})


@login_required
def my_model_add_devices(request, id):
    project_model = get_object_or_404(m.ProjectModels, id=id)
    return render(request, 'my_project/my_model/add_devices.html', {'project_model_id': id, 'model_id': project_model.model.id})
