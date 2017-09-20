from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request, 'cyder/index.html')

def model_viewer(request, modelfile):
    #if modelfile == "":
    #    modelfile == None
    return render(request, 'cyder/model_viewer.html', {'modelfile': modelfile})


