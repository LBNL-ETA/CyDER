from __future__ import division
from django.shortcuts import render, redirect
from django.shortcuts import get_list_or_404, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
import models as m
import api
import ast
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import detail_route
import serializers as s

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
    return render(request, 'calibration.html', api.calibration_info_dict(request, id))


@login_required
def my_models(request):
    return render(request, 'my_models.html', api.my_models_info_dict(request))


@login_required
def my_models_settings(request, id):
    return render(request, 'my_models_settings.html', {'usermodel_id': id})


@login_required
def my_models_review(request, id):
    return render(request, 'my_models_review.html', {'usermodel_id': id})


@login_required
def my_models_general_settings(request, id):
    status, form = api._my_model_update_description(request, id)
    if status:
        messages.add_message(request, messages.SUCCESS, 'The description was updated!')

    return render(request, 'my_models_general_settings.html', {'form': form, 'usermodel_id': id, 'model_id': form.instance.model.id})


@login_required
def my_models_add_devices(request, id):
    user_model = get_object_or_404(m.UserModel, id=id)
    return render(request, 'my_models_add_devices.html', {'usermodel_id': id, 'model_id': user_model.model.id})


class ModelViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = m.Model.objects.all()

    def list(self, request):
        queryset = m.Model.objects.all()
        serializer = s.ModelSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        model = get_object_or_404(m.Model, id=pk)
        serializer = s.DetailModelSerializer(model)
        return Response(serializer.data)
