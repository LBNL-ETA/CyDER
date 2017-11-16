# Every task defined in this file should be declared in /front-end/django-project/sim_worker/task.py

from .celery import app

def drop_column(table, column):
    for row in table:
        del row[column]

@app.task
def get_model(modelname):
    # Import cympy from the function to prevent multiple import caused by celery importing this module at launch
    from . import cymdist

    cymdist.open_study(modelname + '.sxst')
    cymdist.compute_loadflow()

    model = cymdist.model_info()
    devices = cymdist.list_devices()
    cymdist.get_devices_details(devices)
    nodes = cymdist.list_nodes()
    cymdist.get_voltages(nodes)
    sections = cymdist.list_sections()

    # Remove cympy objects to be able to serialize
    drop_column(devices, 'device_object')
    drop_column(nodes, 'node_object')
    drop_column(sections, 'section_object')

    # Return result and exit the worker to "free" cympy
    app.backend.mark_as_done(get_model.request.id, (model, nodes,sections,devices))
    exit(0)


import subprocess
import os
import json
import shutil
import pandas

@app.task
def run_simulation(project):
    if os.path.exists("./simulation_project/sim"):
        shutil.rmtree("./simulation_project/sim")

    cyder_inputs = pandas.read_excel("./simulation_project/cyder_inputs.xlsx")
    cyder_inputs.loc[0, 'feeder_name'] = project['model'] + ".sxst"

    if len(project['addPv']) > 0:
        add_pv = pandas.DataFrame(project['addPv'])
        add_pv.to_excel("./simulation_project/add_pv.xlsx", index=False, header=["device_number", "added_power_kw"])
        cyder_inputs.loc[0, 'add_pv'] = '../simulation_project/add_pv.xlsx'
    else:
        cyder_inputs.loc[0, 'add_pv'] = 'FALSE'

    if len(project['addLoad']) > 0:
        add_load = pandas.DataFrame(project['addLoad'])
        add_load.to_excel("./simulation_project/add_load.xlsx", index=False, header=["device_number", "added_power_kw"])
        cyder_inputs.loc[0, 'add_load'] = '../simulation_project/add_load.xlsx'
    else:
        cyder_inputs.loc[0, 'add_load'] = 'FALSE'

    cyder_inputs.to_excel("./simulation_project/cyder_inputs.xlsx", index=False)

    subprocess.call(["python", "./cosimulation/runsimulation.py", "../simulation_project"])
    result_file = open('./simulation_project/sim/0/0.json')
    result = json.load(result_file)
    result_file.close()
    return result
