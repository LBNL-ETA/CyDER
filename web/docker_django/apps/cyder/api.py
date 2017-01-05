from __future__ import division
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.http import Http404
from django.contrib.auth.models import User
from .models import Model, CalibrationHistory, CurrentCalibration, CalibrationResult, UserModel
from .models import CalibrationData
from . import tool
from redis import Redis


redis = Redis(host='redis', port=6379)


@login_required
def home_info(request):
    return_dict = {}

    # Get all information about the models
    return_dict['models'] = list(Model.objects.all().values())

    # Get the last calibration datetime
    for index, model in enumerate(return_dict['models']):
        dates = CalibrationHistory.objects.filter(model=model['id']).order_by('-date')
        try:
            return_dict['models'][index]['last_calibrated'] = dates[0].date
        except:
            # The model where never calibrated
            return_dict['models'][index]['last_calibrated'] = 'Never'

    # Get the number of model
    return_dict['nb_model'] = len(return_dict['models'])
    return JsonResponse(return_dict)


@login_required
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


@login_required
def calibration_info(request, id):
    return JsonResponse(calibration_info_dict(request, id))


def calibration_info_dict(request, id):
    return_dict = {}

    # Add the full calibration data used
    return_dict['calibration_data'] = list(CalibrationData.objects.filter(calibration=id).values())[0]
    return return_dict


@login_required
def model_update(request, id):
    """API but still return webpage"""
    # Launch a calibration and save to the DB
    tool.calibration_process(id)
    return render(request, 'model.html', model_info_dict(request, id))


@login_required
def add_model(request, id):
    """API but still return webpage"""
    # Get the user and the model
    try:
        user = User.objects.get(username=request.user)
        model = Model.objects.get(id=id)
    except:
        # Model was invalid
        raise Exception('Model id is not valid')

    # Create a new entry in UserModel
    new_model = UserModel(user=user, model=model,
                          name='no name', description='no description')
    new_model.save()
    return render(request, 'my_models.html', my_models_info_dict(request))


@login_required
def remove_model(request, id):
    """API but still return webpage"""
    # Get the user and the model
    try:
        user_model = UserModel.objects.get(id=id)
        user_model.delete()
    except:
        # Model was invalid
        raise Exception('UserModel id is not valid')

    return render(request, 'my_models.html', my_models_info_dict(request))


@login_required
def my_models_info(request):
    return JsonResponse(my_models_info_dict(request))


def my_models_info_dict(request):
    return_dict = {}
    user = User.objects.get(username=request.user)
    return_dict['my_models'] = list(UserModel.objects.filter(user=user).values())

    # Add info about each model
    for index, row in enumerate(return_dict['my_models']):
        model = Model.objects.get(id=row['model_id'])
        if not model:
            raise Exception('Model does not exist anymore')
        return_dict['my_models'][index]['region'] = model.region
    return return_dict
