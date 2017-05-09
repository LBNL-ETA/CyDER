from __future__ import division
import os
import pandas
import random
import string
import argparse
import source.configuration as config
import source.ev_forecast.tool as ev
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

# Create configuration file --> configuration file
configuration = config.initialize_configuration(TIMES, PARENT_FOLDER, MODEL_NAMES)

# Launch ev forecast if necessary --> configuration update
if EV_FORECAST:
    configuration = ev.forecast(CYDER_INPUTS, token)

# Launch pv forecast if necessary --> configuration update
# if pv_forecast:
#     configuration = pv.forecast(CYDER_INPUTS, token)

# Save configuration to the system
filename = config.create_configuration_file(configurations, token)

# Launch PyFmi master
