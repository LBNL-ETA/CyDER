from __future__ import division
import os
import pandas
import random
import string
import argparse
import datetime as dt
import source.configuration as config
import source.ev_forecast.tool as ev
import source.master as m
# import source.ev_forecast.tool as pv

# Read input file
try:
    parser = argparse.ArgumentParser(description='Run CyDER | input configuration file')
    parser.add_argument('configuration_file')
    args = parser.parse_args()
    configuration_file = str(args.configuration_file)
except:
    sys.exit('Error: could not retrieve argument')
cyder_inputs = pandas.read_excel(configuration_file)

# Get token (job id)
token = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(10))
directory = 'temp/' + token + '/'
if not os.path.exists(directory):
    os.makedirs(directory)

# Get simulation time window
start = cyder_inputs.loc[0, 'start']
end = cyder_inputs.loc[0, 'end']
timestep = cyder_inputs.loc[0, 'timestep']
times = [start + dt.timedelta(seconds=x)
         for x in xrange(0, (end - start).total_seconds(), timestep)]

# Create a configuration file for each feeder
config_filenames = []
for index, row in enumerate(cyder_inputs.itertuples()):
    # Create configuration file --> configuration file
    feeder_name = cyder_inputs.loc[index, 'feeder_name']
    configuration = config.initialize_configuration(
        times, '~/Jonathan/GitHub/PGE', feeder_name)

    # Launch ev forecast if necessary --> configuration update
    if cyder_inputs.loc[index, 'ev_forecast'] is not False:
        configuration = ev.forecast(cyder_inputs, token)

    # Launch pv forecast if necessary --> configuration update
    # if pv_forecast:
    #     configuration = pv.forecast(CYDER_INPUTS, token)

    # Save configuration to the system
    filename = config.create_configuration_file(configuration, token)
    config_filenames.append(filename)

# Launch PyFmi master
master = m.Master()
master.filenames = config_filenames
master.start = start
master.times = times
master.solve()
