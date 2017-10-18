# Every task defined in this file should be declared in /front-end/django-project/sim_worker/task.py

from .celery import app
import pandas

@app.task
def get_model(modelname):
    # Import cympy from the function to prevent multiple import caused by celery importing this module at launch
    from . import cymdist

    cymdist.open_study(modelname + '.sxst')
    cymdist.compute_loadflow()

    model = cymdist.model_info()
    devices = cymdist.list_devices()
    nodes = cymdist.list_nodes()
    nodes = cymdist.get_voltages(nodes)
    sections = cymdist.list_sections()

    # Remove cympy objects to be able to serialize
    devices = devices.drop('device_object', axis=1)
    nodes = nodes.drop('node_object', axis=1)
    sections = sections.drop('section_object', axis=1)

    # Return result and exit the worker to "free" cympy
    app.backend.mark_as_done(get_model.request.id, (model, nodes,sections,devices))
    exit(0)


import subprocess
import os
import json
import shutil

@app.task
def run_simulation(project):
    subprocess.call(["python", "./cosimulation/runsimulation.py", "../simulation_project"])
    result_file = open('./simulation_project/sim/0/0.json')
    result = json.load(result_file)
    result_file.close()
    shutil.rmtree("./simulation_project/sim")
    return result
