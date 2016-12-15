from __future__ import division
from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import Model


def home(request):
    return render(request, 'home.html', {})


def model(request, id):
    return_dict = list(Model.objects.filter(id=id).values())[0]
    return render(request, 'model.html', return_dict)
