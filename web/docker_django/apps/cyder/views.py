from django.shortcuts import render, redirect
from .models import Model
from redis import Redis


redis = Redis(host='redis', port=6379)


def home(request):
    model = Model.objects.all()
    nb_model = len(model)
    model_filenames = [m.filename for m in model]
    return render(request, 'home.html', {'nb_model': nb_model, 'filename': model_filenames})
