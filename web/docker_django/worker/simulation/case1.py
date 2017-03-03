from __future__ import division
import argparse
import sys
import functions as func
import cymdist
import pdb

# Retrieve model name
try:
    parser = argparse.ArgumentParser(description='Need model filename')
    # Create args and parse them
    arg_names = ['filename']
    for arg_name in arg_names:
        parser.add_argument(arg_name)
    args = parser.parse_args()
    model_filename = str(args.filename)
except:
    sys.exit('Error: could not retrieve argument')

# Create time and model name vectors
times = [0.0, 0.1]
model_names = [model_filename] * len(times)

# Generate the load profile
load_profile = [1.0, 0.5]

# Generate the pv profile
pv_profile = [1.0, 0.5]

# Initiate the configuration file
configuration = func.initialize_configuration(times, model_names)

# Shift load and pv in the configuration file
configuration = func.shift_load_and_pv(load_profile, pv_profile, configuration)

# Create the configuration file
configuration_filename = func.create_configuration_file(configuration)

# start_time = times[0]
# end_time = times[-1]
# save_to_file = 0
# result = simulate_cymdist_gridyn_fmus(configuration_filename, start_time, end_time, save_to_file)
# print(result)
# pdb.set_trace()
