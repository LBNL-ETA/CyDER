from .celery import app

@app.task
def get_model_devices(modelfile):
	return
