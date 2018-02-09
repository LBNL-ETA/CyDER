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

# Create a configuration file for each feeder
feeder_path_to_configurations = []
configurations = []
for index, row in enumerate(cyder_inputs.itertuples()):
    # Create a feeder configuration
    config = c.FeederConfiguration()
    config.pk = index
    config.token = token
    config.directory = directory
    config.times = times
    config.cyder_input_row = row
    import pdb; pdb.set_trace()

    # Configure based on inputs
    config.configure()
    feeder_path_to_configurations.append(config.save())
    config.visualize()
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

# Lines that changes with 2 feeders
if len(feeder_path_to_configurations) == 2:
    master.monitoring_class = source.monitor.Monitor2Feeder
    master.feeder_voltage_reference = [[2520, 2520, 2520, 0, -120, 120],
                                       [7270, 7270, 7270, 0, -120, 120]]
    master.griddyn_fmu_path = './static/fmus/14bus2input.fmu'
master.solve()

# Plot under voltage and over loading
for pk in range(0, len(feeder_path_to_configurations)):
    source.monitor.plot_post_simulation(
        start, configurations[pk].configuration, directory, pk)
