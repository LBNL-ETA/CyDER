from django.shortcuts import render, redirect

import celery_test.tasks
from celery.result import AsyncResult

import pandas

# Create your views here.
def index(request):
	return render(request, 'testapp/index.html')

def ask_model(request):
	try:
		modelfile = request.POST['modelfile']
	except (KeyError):
		return render(request, 'testapp/error.html', { 'errormsg':"Missing parameter(s)" })
	else:
		result = celery_test.tasks.get_model_devices.delay(modelfile)
		return redirect(update_db, taskid=result.id)
	
def update_db(request, taskid):
	result = AsyncResult(taskid)
	if result.status ==  'SUCCESS':
		devices = result.get()
		lenght = len(devices)
		for index in range(0, lenght):
			device = devices.iloc[0]
			#device['device_number']
			#device['device_type']
			#device['device_type_id']
			#device['distance']
			#device['section_id']
			#device['latitude']
			#device['longitude']
		return redirect(db_updated)
	else:
		return render(request, 'testapp/wait.html', { 'taskid':taskid , 'status':result.status })

def db_updated(request):
	return render(request, 'testapp/db_updated.html')
