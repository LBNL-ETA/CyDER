from __future__ import division
from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import Model, CalibrationHistory


def home(request):
    return render(request, 'home.html', {})


def model(request, id):
    return_dict = {}
    model = Model.objects.filter(id=id)
    return_dict['model'] = list(model.values())[0]
    return_dict['history'] = list(CalibrationHistory.objects.filter(model=model[0]).values())
    return render(request, 'model.html', return_dict)
