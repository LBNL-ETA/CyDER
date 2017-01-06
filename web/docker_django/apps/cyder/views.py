from __future__ import division
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
import api
import ast


@login_required
def home(request):
    return render(request, 'home.html', {})


@login_required
def model(request, id):
    # Reduced history data
    reduced_result = api.model_info_dict(request, id)
    reduced_result['history'] = list(reversed(reduced_result['history']))[:5]

    return render(request, 'model.html', reduced_result)


@login_required
def calibration(request, id):
    return render(request, 'calibration.html', api.calibration_info_dict(request, id))


@login_required
def my_models(request):
    return render(request, 'my_models.html', api.my_models_info_dict(request))


@login_required
def my_models_settings(request, id):
    status, form = api._my_model_update_description(request, id)
    if status:
        messages.add_message(request, messages.SUCCESS, 'The description was updated!')
    return render(request, 'my_models_settings.html', {'form': form, 'usermodel_id': id})
