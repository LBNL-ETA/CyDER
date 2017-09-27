from django.shortcuts import render

# Create your views here.
def model_viewer(request, modelfile):
    return render(request, 'cyder/model_viewer.html', {'modelfile': modelfile})
