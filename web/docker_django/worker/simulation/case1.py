from __future__ import division
import argparse
import sys
import functions as func
from ... import cymdist
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

# Create a time vector
times = []

# Generate the load profile
load_profile = []

# Generate the pv profile
pv_profile = []

def initialize_configuration(times, model_names):
    configuration = {'times': times,
                     'interpolation_method': 'closest_time',
                     'models': []
                     }

    for time, model_name in zip(times, model_names):
        model = {
           'filename': 'D://Users//Jonathan//Documents//GitHub//PGE_Models_DO_NOT_SHARE//' + model_name,
           'new_loads': [],
           'set_loads': [],
           'new_pvs': [],
           'set_pvs': [],
           }
        configuration['models'].append(model)
    return configuration

def shift_load_and_pv(load_profile, pv_profile, configuration):
    """Extend the configuration file with load and pv shift"""
    # Open model and get the devices from the first model
    cympy.study.Open(configuration['models'][0]['filename'])
    loads = cymdist.get_all_loads()
    pvs = cymdist.get_all_pvs()

    for index, time in enumerate(configuration['times']):
        # Set new pv generation
        for pv in pvs:
            configuration['models'][index]['set_pvs'].append({'device_name': pv['device_name'],
                                                              'generation': pv['generation'] * pv_profile[index]})
        # Set new load demand
        for pv in pvs:
            configuration['models'][index]['set_loads'].append({'device_name': pv['device_name'],
                                                                'active_power': pv['active_power'] * load_profile[index]})
    return configuration

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
