# Every task defined in this file should be declared in /front-end/django-project/sim_worker/task.py

from .celery import app
import os
import json
import shutil
import datetime
import random
import math
import pandas
import dateutil.parser
import re


def drop_column(table, column):
    for row in table:
        del row[column]

@app.task
def get_model(modelname):
    # Import cympy from the function to prevent multiple import caused by celery importing this module at launch
    from . import cymdist

    cymdist.open_study(modelname + '.sxst')
    cymdist.compute_loadflow()

    model = cymdist.model_info(modelname)
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



@app.task
def run_configuration(id, project):
# run_configuration will exploit the solar.csv sunlight data aswell as the scada baseload data through the solarprofile.py and scadaprofile.py modules
# run_configuration returns the estimated PV production in time and estimated load in time

    import sim_worker.pv
    # import sim_worker.substation
    import sim_worker.scada
    import sim_worker.scadaprofile as scp
    import sim_worker.solarprofile as sop

    simDays = project['simulation_dates']
    l=[]
    for key in simDays:
        l.append(min(simDays[key].items(), key=lambda x: x[1]))
    day=min(l,key=lambda x: x[1])[0]
    start=day + ' 07:00:00'
    end=day + ' 19:00:00'
    substation =  project['model']

    add_pv = pandas.DataFrame.from_dict(project['addPv'])

    if (add_pv.empty):
        pv=[]
        pvIndex=[]
    else :
        pv_nominal_capacity_kw = add_pv['power'].sum()
        pv = sop.solar_profile(start, end, pv_nominal_capacity_kw)
        pvIndex=pv.index.strftime('%Y-%m-%d %H:%M:%S').tolist()
        pv = pv.iloc[:,0].tolist()

    load = scp.scada_profile(start, end, substation)
    loadIndex = load.to_frame().index.strftime('%Y-%m-%d %H:%M:%S').tolist()
    load=load.tolist()
    ev = []


    return { 'pv': pv, 'pvIndex': pvIndex, 'ev': ev, 'load': load, 'loadIndex': loadIndex, 'date': day }

@app.task
def run_detailed_configuration(id, project):
# run_configuration will exploit the solar.csv sunlight data aswell as the scada baseload data through the solarprofile.py and scadaprofile.py modules
# run_configuration returns the estimated PV production in time and estimated load in time

    import sim_worker.pv
    # import sim_worker.substation
    import sim_worker.scada
    import sim_worker.scadaprofile as scp
    import sim_worker.solarprofile as sop

    simDays = project['simulation_dates']
    x=pandas.Series()
    for key in simDays:
        x=x.append(pandas.Series(list(simDays[key].keys())))
    x=x.drop_duplicates().sort_values()
    result={}
    for day in x:
        start=day + ' 07:00:00'
        end=day + ' 19:00:00'
        substation =  project['model']

        add_pv = pandas.DataFrame.from_dict(project['addPv'])

        if (add_pv.empty):
            pv=[]
            pvIndex=[]
        else :
            pv_nominal_capacity_kw = add_pv['power'].sum()
            pv = sop.solar_profile(start, end, pv_nominal_capacity_kw)
            pvIndex=pv.index.strftime('%Y-%m-%d %H:%M:%S').tolist()
            pv = pv.iloc[:,0].tolist()

        load = scp.scada_profile(start, end, substation)
        loadIndex = load.to_frame().index.strftime('%Y-%m-%d %H:%M:%S').tolist()
        load=load.tolist()
        ev = []

        temp={}
        temp['pv']=pv
        temp['pvIndex']=pvIndex
        temp['ev']=ev
        temp['load']=load
        temp['loadIndex']=loadIndex
        temp['date']=day
        result[day]=temp


    return result

@app.task
def run_simulation(id, project):
# run_simulation prepares and formats the data from the project settings and launches the simulation through the cymdist python api
 # run_simulation returns  in json format the simulation results that will be saved in the results field of the project

    from . import cymdist
    from sim_worker.pv import PVFactory
    from sim_worker.substation import Substation
    from sim_worker.scada import Scada

    simDays = project['simulation_dates']
    l=[]
    for key in simDays:
        l.append(min(simDays[key].items(), key=lambda x: x[1]))
    day=min(l,key=lambda x: x[1])[0]


    pv_node_ids = []
    pv_network_ids = []
    pv_device_ids = []
    pv_nominal_capacities = []

    load_node_ids = []
    load_network_ids = []
    load_device_ids = []
    load_nominal_capacities = []

    substation = Substation('C:/Users/DRRC/Desktop/PGE_Models_DO_NOT_SHARE/' + project['model'] + '.sxst')

    i=0
    for p in project['addPv']:
        pv_node_ids.append(p['node_id'])
        pv_network_ids.append(p['feeder'])
        pv_nominal_capacities.append(-1*p['power'])
        pv_device_ids.append('PV' + str(i) )
        i=i+1

    # assuming load_nominal capacities is equivalent to the opposite of pv_nominal_capacities
    i=0
    for p in project['addLoad']:
        load_node_ids.append(p['node_id'])
        load_network_ids.append(p['feeder'])
        load_nominal_capacities.append(p['power'])
        load_device_ids.append('Load' + str(i) )
        i=i+1


    substation.add_power_devices(node_ids=pv_node_ids, network_ids=pv_network_ids, device_ids=pv_device_ids)

    pvfactory = PVFactory('sim_worker/solar.csv')
    pvs = pvfactory.create(pv_nominal_capacities, pv_device_ids)

    scada = Scada('C:/Users/DRRC/Desktop/raw_SCADA/' + project['model'] + '.csv')

    # simDays = project['simulation_dates']
    # l=[]
    # for key in simDays:
    #     l.append(min(simDays[key].items(), key=lambda x: x[1]))
    # day=min(l,key=lambda x: x[1])[0]

    start=day + ' 07:00:00'
    end=day + ' 19:00:00'
    timestep = '60T'

    datetimes = pandas.date_range(start, end, freq= timestep).tolist()

    results = []
    for t in datetimes:
        print("Run substation at " + t.strftime("%Y-%m-%d %H:%M:%S"))
        feeder_baseloads = scada.get(t)
        substation.baseload_allocation(feeder_loads=feeder_baseloads)
        substation.set_power_devices(device_ids=[pv.id for pv in pvs],
                                     values=[pv.get(t) for pv in pvs])
        substation.run_powerflow(feeders=feeder_baseloads.keys())
        nodes = substation.list_nodes()
        nodes = substation.get_voltage(nodes)
        results.append(nodes)

    dfs = []
    indexes = []
    i=0

    for result in results:
        keys=[]
        values=[]
        df=result
        columnNumbers = [x for x in range(df.shape[1])]
        columnNumbers.remove(0)
        df=df.iloc[:,columnNumbers]
        df=df.set_index('node_id')
        df = df.where((pandas.notnull(df)), None)
        df['max']=df[['voltage_A','voltage_B','voltage_C']].max(axis=1)
        df['min']=df[['voltage_A','voltage_B','voltage_C']].min(axis=1)
        worstHighVoltage=df.loc[df['max'].idxmax()]
        wostLowVoltage=df.loc[df['min'].idxmin()]
        df=df.drop('min', axis=1)
        df=df.drop('max', axis=1)
        keys=df.index.tolist()
        for index, row in df.iterrows():
            values.append(row.to_dict())
        df=dict(zip(keys, values))
        df['worstHighVoltage']=worstHighVoltage.to_dict()
        df['wostLowVoltage']=wostLowVoltage.to_dict()
        dfs.append(df)
        indexes.append(datetimes[i].strftime("%Y_%m_%d_%H_%M_%S"))
        i=i+1

        d = dict(zip(indexes, dfs))
    
    return json.dumps(d)
