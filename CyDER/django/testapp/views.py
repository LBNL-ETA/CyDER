from django.shortcuts import render

from celery_test.tasks import do_some_work

# Create your views here.
def index(request):
	try:
		triggered = request.POST['triggered']
	except (KeyError):
		context = { 'triggered':False }
	else:
		if triggered == 'true':
			context = { 'triggered':True }
			# TODO: Send message with Celery
			do_some_work.delay(2, 5)
		else:
			context = { 'triggered':False }

	return render(request, 'testapp/index.html', context)

	
