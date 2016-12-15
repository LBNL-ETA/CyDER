from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import Model
from redis import Redis


redis = Redis(host='redis', port=6379)


def home(request):
    return render(request, 'home.html', {})

def home_info(request):
    return_dict = {}
    return_dict['models'] = list(Model.objects.all().values())
    return_dict['nb_model'] = len(return_dict['models'])
    return JsonResponse(return_dict)

def model_info(request, id):
    return_dict = {}
    return_dict['models'] = list(Model.objects.filter(id=id).values())[0]
    return JsonResponse(return_dict)

def model(request, id):
    return_dict = list(Model.objects.filter(id=id).values())[0]
    return render(request, 'model.html', return_dict)
