from __future__ import division
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
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
