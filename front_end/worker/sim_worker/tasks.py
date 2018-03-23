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
import scada_profile

@app.task
def run_configuration(id, project):
    
#The following 3 lines of code are the ones to be used once testing is over
    # start = dateutil.parser.parse(project['start'])
    # end = dateutil.parser.parse(project['end'])
    # substation =  project['model']

#The following 3 lines of code are for testing
    start = '2016-06-17 00:00:00'
    end = '2016-06-18 00:00:00'
    substation =  'BU0006'
    
    add_pv = pandas.DataFrame.from_dict(project['addPv'])
    pv_nominal_capacity_kw = add_pv.iloc[:,1].sum()

    # In the following lines, the pandas Datafames and Series returned by the solarprofile and scadaprofile scripts are manipulated in such a way that they are JSON serializable (in order for the data to be stored and saved in the project settings)
    load = scp.scada_profile(start, end, substation)
    loadIndex = load.to_frame().index.strftime('%Y-%m-%d %H:%M:%S').tolist()
    load=load.tolist()
    ev = []
    pv = sop.solar_profile(start, end, pv_nominal_capacity_kw)
    pvIndex=pv.index.strftime('%Y-%m-%d %H:%M:%S').tolist()
    pv = pv.iloc[:,0].tolist()


    return { 'pv': pv, 'pvIndex': pvIndex, 'ev': ev, 'load': load, 'loadIndex': loadIndex}


@app.task
def run_simulation(id):
    project_path = os.path.join('simulation_projects', str(id))

    subprocess.call(['python', './cosimulation/runsimulation.py', os.path.join('..', project_path)])

    cyder_inputs = pandas.read_excel(os.path.join(project_path, 'cyder_inputs.xlsx'))
    start = cyder_inputs.loc[0, 'start']
    end = cyder_inputs.loc[0, 'end']
    timestep = cyder_inputs.loc[0, 'timestep']
    times = [x for x in range(0, int((end - start).total_seconds()), int(timestep))]

    properties = ['DwHighVoltWorstA', 'DwHighVoltWorstB', 'DwHighVoltWorstC', 'DwLowVoltWorstA', 'DwLowVoltWorstB', 'DwLowVoltWorstC']

    results = {}
    for prop in properties:
        results[prop] = []
    for time in times:
        result_file = open(os.path.join(project_path, 'sim', '0', str(time) + '.json'))
        result = json.load(result_file)
        for prop in properties:
            results[prop].append(float(result[prop]))
        result_file.close()
    return results
