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
import datetime
import dateutil.parser

@app.task
def run_configuration(id, project):
    project_path = os.path.join("simulation_projects", str(id))
    if os.path.exists(project_path):
        shutil.rmtree(project_path)
    os.makedirs(project_path)

    cyder_inputs = pandas.DataFrame(columns=["feeder_name", "transmission_model", "bus_id", "start", "end", "timestep", "ev_forecast", "pv_forecast", "load_forecast", "add_load", "add_pv"])
    cyder_inputs.loc[0, "feeder_name"] = project["model"] + ".sxst"
    cyder_inputs.loc[0, "transmission_model"] = "IEEE_14_bus"
    cyder_inputs.loc[0, "bus_id"] = 11
    cyder_inputs.loc[0, "start"] = dateutil.parser.parse(project["start"])
    cyder_inputs.loc[0, "end"] = dateutil.parser.parse(project["end"])
    cyder_inputs.loc[0, "timestep"] = project["timestep"]
    cyder_inputs.loc[0, "ev_forecast"] = "FALSE"
    cyder_inputs.loc[0, "pv_forecast"] = "../simulation_projects/pv_forecast.xlsx"
    cyder_inputs.loc[0, "load_forecast"] = "../simulation_projects/load_forecast.xlsx"
    if len(project['addPv']) > 0:
        add_pv = pandas.DataFrame(project["addPv"])
        add_pv.to_excel(os.path.join(project_path, "add_pv.xlsx"), index=False, header=["device_number", "added_power_kw"])
        cyder_inputs.loc[0, "add_pv"] = os.path.join("..", project_path, "add_pv.xlsx")
    else:
        cyder_inputs.loc[0, "add_pv"] = "FALSE"
    if len(project["addLoad"]) > 0:
        add_load = pandas.DataFrame(project["addLoad"])
        add_load.to_excel(os.path.join(project_path, "add_load.xlsx"), index=False, header=["device_number", "added_power_kw"])
        cyder_inputs.loc[0, "add_load"] = os.path.join("..", project_path, "add_load.xlsx")
    else:
        cyder_inputs.loc[0, "add_load"] = "FALSE"
    cyder_inputs.to_excel(os.path.join(project_path, "cyder_inputs.xlsx"), index=False)

    subprocess.call(["python", "./cosimulation/runconfiguration.py", os.path.join("..", project_path)])

    return { "detail": "Configuration done" }

@app.task
def run_simulation(id):
    project_path = os.path.join("simulation_projects", str(id))

    subprocess.call(["python", "./cosimulation/runsimulation.py", os.path.join("..", project_path)])

    cyder_inputs = pandas.read_excel(os.path.join(project_path, 'cyder_inputs.xlsx'))
    start = cyder_inputs.loc[0, 'start']
    end = cyder_inputs.loc[0, 'end']
    timestep = cyder_inputs.loc[0, 'timestep']
    times = [x for x in range(0, int((end - start).total_seconds()), int(timestep))]

    results = []
    for time in times:
        result_file = open(os.path.join(project_path, "sim", "0", str(time) + ".json"))
        result = json.load(result_file)
        result["time"] = time
        results.append(result)
        result_file.close()
    return results
