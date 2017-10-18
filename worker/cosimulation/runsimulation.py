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
    parser = argparse.ArgumentParser(description='Run CyDER | input project folder')
    parser.add_argument('project_folder')
    args = parser.parse_args()
    project_folder = str(args.project_folder)
except:
    sys.exit('Error: could not retrieve argument')

os.chdir(CURRENT_PATH)

cyder_inputs = pandas.read_excel(os.path.join(project_folder, 'cyder_inputs.xlsx'))
timestep = cyder_inputs.loc[0, 'timestep']
times = [0]

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

# Create a configuration file for the transmission network
# -->

# Create a configuration to link distribution and transmission network
# -->

# Create a GridDyn FMU
# -->

# Launch PyFmi master
master = m.Master(number_of_feeder=len(feeder_path_to_configurations))
master.feeder_path_to_configurations = feeder_path_to_configurations
master.times = times
master.timestep = timestep
master.feeder_voltage_reference = [[2520, 2520, 2520, 0, -120, 120]]
master.monitoring_class = source.monitor.Monitor
master.monitoring = False

# Lines that changes with 2 feeders
if len(feeder_path_to_configurations) == 2:
    master.monitoring_class = source.monitor.Monitor2Feeder
    master.feeder_voltage_reference = [[2520, 2520, 2520, 0, -120, 120],
                                       [7270, 7270, 7270, 0, -120, 120]]
    master.griddyn_fmu_path = './static/fmus/14bus2input.fmu'
master.solve()
