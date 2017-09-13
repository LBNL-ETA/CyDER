from django.shortcuts import render, redirect
import pandas
import sim_worker.tasks
from celery.result import AsyncResult
from .models import Device

# Create your views here.
def index(request):
	return render(request, 'cyder/index.html')

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
