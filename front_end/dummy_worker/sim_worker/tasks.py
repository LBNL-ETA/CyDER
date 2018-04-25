from .celery import app
import os
import json
import shutil
import datetime
import random
import math
from time import sleep
import pandas
import dateutil.parser
import glob
import re

from sim_worker.scada import Scada
import sim_worker.scadaprofile as scp
import sim_worker.solarprofile as sop

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



@app.task
def run_configuration(id, project):
# run_configuration will exploit the solar.csv sunlight data aswell as the scada baseload data through the solarprofile.py and scadaprofile.py modules
# run_configuration returns the estimated PV production in time and estimated load in time


#The following 3 lines of code are the ones to be used once testing is over
    # start = dateutil.parser.parse(project['start'])
    # end = dateutil.parser.parse(project['end'])
    # substation =  project['model']

#The following 3 lines of code are for testing
    # start = '2016-06-17 00:00:00'
    # end = '2016-06-18 00:00:00'
    # substation =  'BU0006'



    load = []
    loadIndex = []
    pv=[]
    pvIndex=[]
    ev = []



    return { 'pv': pv, 'pvIndex': pvIndex, 'ev': ev, 'load': load, 'loadIndex': loadIndex}

#Currently under development 


@app.task
def run_simulation(id, project, day):
# run_simulation in the dummy-work reads and formats sample reuslts saved in .csv in the dummy-worker directory
# returns the results in json format to be saved in the results field of the project as it would be done in the real worker

    # path = "./sim_worker/resultsLongSim"
    # filenames = glob.glob(path + "/*.csv")
    # filenames.sort()

    # dfs = pandas.Series()
    # indexes = []
    result={'test': 101, 'date': day}

    # for filename in filenames:

    #     df=pandas.read_csv(filename)
    #     filename=re.sub(r'./sim_worker/resultsLongSim/', '', filename)
    #     filename=re.sub(r'.csv', '', filename)
    #     dfs[datetime.datetime.strptime(filename, "%Y_%m_%d_%H_%M_%S")]=df.to_dict()
    # days=dfs.groupby(by=[dfs.index.day, dfs.index.month, dfs.index.year])
    # for day in days:
    #     result[day[1].index[0].date()]=day[1].to_dict()
            
            
    return result

   