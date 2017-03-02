from __future__ import division
import argparse
import sys
from functions import *
import pdb

# Retrieve model name
try:
    parser = argparse.ArgumentParser(description='Need model filename')
    # Create args and parse them
    arg_names = ['filename', 'nb_evs', 'start', 'end']
    for arg_name in arg_names:
        parser.add_argument(arg_name)
    args = parser.parse_args()
    model_filename = str(args.filename)
    nb_evs = int(args.nb_evs)
    start = str(args.start)
    end = str(args.end)
except:
    sys.exit('Error: could not retrieve argument')

# Generate the ev profile
ev_profile = []

# Create the configuration file
configuration_filename = ''
model_names = []
times = []
configurations = []
create_configuration_file(configuration_filename, model_names, times, configurations)

# start_time = times[0]
# end_time = times[-1]
# save_to_file = 0
# result = simulate_cymdist_gridyn_fmus(configuration_filename, start_time, end_time, save_to_file)
# print(result)
# pdb.set_trace()
