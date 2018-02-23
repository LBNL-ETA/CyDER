from __future__ import division
import os
CURRENT_PATH = os.path.dirname(os.path.abspath(__file__))
import pandas
import random
import string
import argparse
import datetime as dt
import matplotlib.pyplot as plt
import source.configuration as c
import source.master as m
import source.monitor
import os

# Read input file
try:
    parser = argparse.ArgumentParser(description='Run CyDER configuration | input project folder')
    parser.add_argument('project_folder')
    args = parser.parse_args()
    project_folder = str(args.project_folder)
except:
    sys.exit('Error: could not retrieve argument')

os.chdir(CURRENT_PATH)

cyder_inputs = pandas.read_excel(os.path.join(project_folder, 'cyder_inputs.xlsx'))
start = cyder_inputs.loc[0, 'start']
end = cyder_inputs.loc[0, 'end']
timestep = cyder_inputs.loc[0, 'timestep']
times = [x for x in range(0, int((end - start).total_seconds()), int(timestep))]

# Get token (job id)
directory = os.path.join(project_folder, 'sim/')
if not os.path.exists(directory):
    os.makedirs(directory)

# Create a configuration file for each feeder
feeder_path_to_configurations = []
configurations = []
for index, row in enumerate(cyder_inputs.itertuples()):
    # Create a feeder configuration
    config = c.FeederConfiguration()
    config.pk = index
    config.directory = directory
    config.times = times
    config.cyder_input_row = row

    # Configure based on inputs
    config.configure()
    feeder_path_to_configurations.append(config.save())
    configurations.append(config)
