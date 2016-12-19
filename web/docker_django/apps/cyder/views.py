from __future__ import division
from django.shortcuts import render, redirect
from django.http import JsonResponse
import api
import ast


def home(request):
    return render(request, 'home.html', {})


def model(request, id):
    return render(request, 'model.html', api.model_info_dict(request, id))


def calibration(request, id):
    return render(request, 'calibration.html', api.calibration_info_dict(request, id))
