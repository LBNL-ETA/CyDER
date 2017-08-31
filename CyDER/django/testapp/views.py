from django.shortcuts import render, redirect

import celery_test.tasks
from celery.result import AsyncResult

# Create your views here.
def index(request):
	return render(request, 'testapp/index.html')

def start_sim(request):
	try:
		param_1 = int(request.POST['param_1'])
		param_2 = int(request.POST['param_2'])
	except (KeyError):
		return render(request, 'testapp/error.html', { 'errormsg':"Missing parameter(s)" })
	except (ValueError):
		return render(request, 'testapp/error.html', { 'errormsg':"Bad parameter(s)" })
	else:
		result = celery_test.tasks.start_sim.delay(param_1, param_2)
		return redirect(sim_started, taskid=result.id)
		
def sim_started(request, taskid):
	return render(request, 'testapp/sim_started.html', { 'taskid':taskid })
	
def result(request, taskid):
	result = AsyncResult(taskid)
	return render(request, 'testapp/result.html', { 'taskid':taskid , 'result':result })
