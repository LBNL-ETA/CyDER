# Every task declared in this file should be defined in /worker/sim_worker/task.py

from .celery import app

@app.task
def get_model_devices(modelfile):
	return

@app.task
def get_model_nodes(modelfile):
	return
