from __future__ import division
import os
CURRENT_PATH = os.path.dirname(os.path.abspath(__file__))
import pandas
import random
import string
import argparse
import datetime as dt
import source.configuration as c
import source.master as m
import os

# Read input file
try:
    parser = argparse.ArgumentParser(description='Run CyDER | input configuration file')
    parser.add_argument('configuration_file')
    args = parser.parse_args()
    configuration_file = str(args.configuration_file)
except:
    sys.exit('Error: could not retrieve argument')
os.chdir(CURRENT_PATH)
cyder_inputs = pandas.read_excel(configuration_file)
start = cyder_inputs.loc[0, 'start']
end = cyder_inputs.loc[0, 'end']
timestep = cyder_inputs.loc[0, 'timestep']
times = [x for x in range(0, int((end - start).total_seconds()), int(timestep))]

# Get token (job id)
token = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(10))
directory = 'temp/' + token + '/'
if not os.path.exists(directory):
    os.makedirs(directory)

# # Create a configuration file for each feeder
# feeder_configurations = []
# for index, row in enumerate(cyder_inputs.itertuples()):
#     # Create a feeder configuration
#     config = c.FeederConfiguration()
#     config.pk = index
#     config.token = token
#     config.directory = directory
#     config.times = times
#     config.cyder_input_row = row
#
#     # Configure based on inputs
#     config.configure()
#     feeder_configurations.append(config.save())

feeder_configurations = ["D:\\Users\\Jonathan\\Desktop\\CyDER\\cosimulation\\temp\XIA09NBBZ8"]
# Create a configuration file for the transmission network
# -->

# Create a configuration to link distribution and transmission network
# -->

# Create a GridDyn FMU
# -->

# Launch PyFmi master
master = m.Master()
master.feeder_configurations = feeder_configurations
master.times = times
master.timestep = timestep
master.feeder_voltage_reference = [[2520, 2520, 2520, 0, -120, 120]]
master.solve()

import pdb
pdb.set_trace()
