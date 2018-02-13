# Every task declared in this file should be defined in /front_end/worker/sim_worker/task.py

from .celery import app

@app.task
def get_model(modelname):
    return

@app.task
def run_configuration(id, project):
    return

@app.task
def run_simulation(id):
    return
