from __future__ import division
from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import Model, CalibrationHistory
from . import tool
from redis import Redis


redis = Redis(host='redis', port=6379)


def home_info(request):
    return_dict = {}

    # Get all information about the models
    return_dict['models'] = list(Model.objects.all().values())

    # Get the last calibration datetime
    for index, model in enumerate(return_dict['models']):
        dates = CalibrationHistory.objects.filter(model=model['id']).order_by('-date')
        return_dict['models'][index]['last_calibrated'] = dates[0].date

    # Get the number of model
    return_dict['nb_model'] = len(return_dict['models'])
    return JsonResponse(return_dict)

def model_info(request, id):
    return_dict = {}
    model = Model.objects.filter(id=id)
    return_dict['model'] = list(model.values())[0]
    return_dict['history'] = list(CalibrationHistory.objects.filter(model=model[0]).values())
    return JsonResponse(return_dict)


def model_update(request, id):
    pass
