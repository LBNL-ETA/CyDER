from __future__ import division
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.http import Http404
from .models import Model, CalibrationHistory, CurrentCalibration, CalibrationResult
from .models import CalibrationData
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
    return JsonResponse(model_info_dict(request, id))


def model_info_dict(request, id):
    return_dict = {}

    # Add the model description
    model = Model.objects.filter(id=id)
    if not model:
        raise Http404('No corresponding model in the database')
    return_dict['model'] = list(model.values())[0]

    # Add the current calibration values
    return_dict['current_calibration'] = list(CurrentCalibration.objects.filter(model=model[0]).values())

    # Add the history of calibrations
    return_dict['history'] = list(CalibrationHistory.objects.filter(model=model[0]).values())

    # Along with the history of calibrations add the values found
    for index, row in enumerate(return_dict['history']):
        temp_calibration = CalibrationResult.objects.get(calibration=row['id'])
        return_dict['history'][index]['z_a'] = temp_calibration.impedance_a
        return_dict['history'][index]['z_b'] = temp_calibration.impedance_b
        return_dict['history'][index]['z_c'] = temp_calibration.impedance_c
    return return_dict


def calibration_info(request, id):
    return JsonResponse(calibration_info_dict(request, id))


def calibration_info_dict(request, id):
    return_dict = {}

    # Add the full calibration data used
    return_dict['calibration_data'] = list(CalibrationData.objects.filter(calibration=id).values())[0]
    return return_dict


def model_update(request, id):
    # Launch a calibration and save to the DB
    tool.calibration_process(id)
    return render(request, 'model.html', model_info_dict(request, id))
