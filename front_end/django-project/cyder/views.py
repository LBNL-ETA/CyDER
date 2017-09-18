from django.shortcuts import render, redirect
from django.http import HttpResponse
import pandas
import sim_worker.tasks
from celery.result import AsyncResult
from .models import *
from django.db.models import Q
import json

# Create your views here.
def index(request):
    return render(request, 'cyder/index.html')

def map(request):
    models = Model.objects.all()
    
    return render(request, 'cyder/map.html', {'models': models})

def get_model(request, modelfile):
    model = Model.objects.get(filename=modelfile)
    nodes = Node.objects.filter(model=model)
    lines = Device.objects.filter(Q(model=model), Q(device_type=10) | Q(device_type=13)).select_related('section__from_node', 'section__to_node')
    
    list_nodes = []
    for node in nodes:
        list_nodes.append({ "longitude": node.longitude, "latitude": node.latitude })
    list_lines = []
    for line in lines:
        list_lines.append({ "from": [line.section.from_node.latitude, line.section.from_node.longitude], "to": [line.section.to_node.latitude, line.section.to_node.longitude] })
    json_model = json.dumps({"modelfile": modelfile, "nodes": list_nodes, "lines": list_lines }, separators=(',',':'))
    
    return HttpResponse(json_model)

def ask_model(request):
    try:
        modelfile = request.POST['modelfile']
    except (KeyError):
        return render(request, 'cyder/error.html', { 'errormsg':"Missing parameter(s)" })
    else:
        result = sym_worker.tasks.get_model_devices.delay(modelfile)
        return redirect(update_db, taskid=result.id)
    
def update_db(request, taskid):
    result = AsyncResult(taskid)
    if result.status ==  'SUCCESS':
        devices = result.get()
        lenght = len(devices)
        for index in range(0, lenght):
            device = devices.iloc[index]
            d = Device()
            d.device_number = device['device_number']
            d.device_type = device['device_type']
            d.device_type_id = device['device_type_id']
            d.device_number = device['distance']
            d.distance = device['section_id']
            d.latitude = device['latitude']
            d.longitude = device['longitude']
            d.save()
        return redirect(db_updated)
    else:
        return render(request, 'cyder/wait.html', { 'taskid':taskid , 'status':result.status })

def db_updated(request):
    return render(request, 'cyder/db_updated.html')
