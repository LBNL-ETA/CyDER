# Every task declared in this file should be defined in /worker/sim_worker/task.py

from .celery import app

@app.task
def get_model(modelname):
    return

@app.task
def run_configuration(project):
    return

@app.task
def run_simulation(project):
    return
