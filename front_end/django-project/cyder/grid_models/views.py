from django.shortcuts import render

# Create your views here.
def model_viewer(request, modelname):
    return render(request, 'cyder/model_viewer.html', {'modelname': modelname})
