from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required
def model_viewer(request, modelname = ''):
    return render(request, 'cyder/model_viewer.html', {'modelname': modelname})
