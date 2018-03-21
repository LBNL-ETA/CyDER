from .celery import app
import os
import json
import shutil
import datetime
import dateutil.parser
import random
import math
from time import sleep

def dist_node(node1, node2):
    return math.sqrt((node1['latitude']-node2['latitude'])**2 + (node1['longitude']-node2['longitude'])**2)

def load_model_from(file_path):
    model_file = open(file_path)
    model_data = json.load(model_file)
    model_file.close()
    return (model_data['model'], model_data['nodes'], model_data['sections'],model_data['devices'])

def gen_rnd_model(size = 1):
    longitude = -122.416667 + random.uniform(-0.5, 0.5)
    latitude = 37.783333 + random.uniform(-0.5, 0.5)

    model = {'longitude': longitude, 'latitude': latitude}
    nodes = [None] * int(random.randint(450, 550)*size)
    devices = []
    sections = [None] * (len(nodes)-1)

    print("\rNodes: ...", end="")
    for i in range(len(nodes)):
        node = {'node_id': str(i), 'longitude': longitude + random.uniform(-0.01, 0.01)*math.sqrt(size), 'latitude': latitude + random.uniform(-0.008, 0.008)*math.sqrt(size)}
        for prop in ['VA', 'VB', 'VC']:
            node[prop] = random.uniform(0, 100)
        nodes[i] = node
    print("\rNodes: OK")


    print("\rSections: ...", end="")
    for i in range(len(sections)):
        from_node = nodes[i]
        prox_node = nodes[i+1]
        prox_node_dist = dist_node(from_node, prox_node)
        for j in range(i+2, len(nodes)):
            dist = dist_node(from_node, nodes[j])
            if dist < prox_node_dist:
                prox_node = nodes[j]
                prox_node_dist = dist
        to_node = prox_node
        section = {'section_id': str(i), 'from_node_id': from_node['node_id'], 'to_node_id': to_node['node_id']}
        sections[i] = section
        line = {'device_number': str(i), 'device_type': 10, 'section_id': section['section_id'], 'longitude': from_node['longitude'], 'latitude': from_node['latitude'], 'distance': 0}
        devices.append(line)
    print("\rSections: OK")

    print("\rPVs: ...", end="")
    for i in range(random.randint(int(len(sections)/4), int(len(sections)/2))):
        section = sections[random.randint(0, len(sections)-1)]
        node = nodes[int(section['from_node_id'])]
        pv = {'device_number': str(i), 'device_type': 39, 'section_id': section['section_id'], 'longitude': node['longitude'], 'latitude': node['latitude'], 'distance': 0}
        pv['detail'] = {'PVActiveGeneration': random.uniform(0, 10)}
        devices.append(pv)
    print("\rPVs: OK")

    print("\rLoads: ...")
    for i in range(random.randint(int(len(sections)/2), len(sections))):
        section = sections[random.randint(0, len(sections)-1)]
        node = nodes[int(section['from_node_id'])]
        load = {'device_number': str(i), 'device_type': 14, 'section_id': section['section_id'], 'longitude': node['longitude'], 'latitude': node['latitude'], 'distance': 0}
        load['detail'] = {}
        for prop in ['SpotKWA', 'SpotKWB', 'SpotKWC']:
            load['detail'][prop] = random.uniform(0, 50)
        devices.append(load)
    print("\rLoads: OK")

    return (model, nodes, sections, devices)

@app.task
def get_model(modelname):
    if modelname == "HUGE_DUMMY":
        return gen_rnd_model(13)
    if modelname == "BIG_DUMMY":
        return gen_rnd_model(5)
    if modelname == "SMALL_DUMMY":
        return gen_rnd_model(0.1)
    return gen_rnd_model()

projects = {}


import sim_worker.scadaprofile as scp
import sim_worker.solarprofile as sop
import pandas

@app.task
def run_configuration(id, project):

#The following 3 lines of code are the ones to be used once testing is over
    start = dateutil.parser.parse(project['start'])
    end = dateutil.parser.parse(project['end'])
    substation =  project['model']

#The following 3 lines of code are for testing
    # start = '2016-06-17 00:00:00'
    # end = '2016-06-18 00:00:00'
    # substation =  'BU0006'
    
    # In the following lines, the pandas Datafames and Series returned by the solarprofile and scadaprofile scripts are manipulated in such a way that they are JSON serializable (in order for the data to be stored and saved in the project settings)
    add_pv = pandas.DataFrame.from_dict(project['addPv'])

    if (add_pv.empty):
        pv=[]
        pvIndex=[]
    else : 
        pv_nominal_capacity_kw = add_pv.iloc[:,1].sum()
        pv = sop.solar_profile(start, end, pv_nominal_capacity_kw)
        pvIndex=pv.index.strftime('%Y-%m-%d %H:%M:%S').tolist()
        pv = pv.iloc[:,0].tolist()

    load = scp.scada_profile(start, end, substation)
    loadIndex = load.to_frame().index.strftime('%Y-%m-%d %H:%M:%S').tolist()
    load=load.tolist()
    ev = []



    return { 'pv': pv, 'pvIndex': pvIndex, 'ev': ev, 'load': load, 'loadIndex': loadIndex}

#Currently under development 
import glob
import re
import json

@app.task
def run_simulation(id):

    path = "sim_worker/results"
    filenames = glob.glob(path + "/*.csv")
    filenames.sort()

    dfs = []
    indexes = []

    for filename in filenames:
        keys=[]
        values=[]
        df=pandas.read_csv(filenames[0])
        df=df.drop(df.columns[0],axis=1)
        df=df.drop(columns=['node_object'])
        df=df.set_index('node_id')
        df = df.where((pandas.notnull(df)), None)
        if (filename==filenames[0]):
            df.loc[df['voltage_A'] > 0 , 'voltage_A'] = 0
        keys=df.index.tolist()
        print("\n")
        for index, row in df.iterrows():
            values.append(row.to_dict())
        df=dict(zip(keys, values))
        dfs.append(df)
        filename=re.sub(r'sim_worker/results/', '', filename)
        filename=re.sub(r'.csv', '', filename)
        indexes.append(filename)

    d = dict(zip(indexes, dfs))
    return json.dumps(d, indent=4)





























