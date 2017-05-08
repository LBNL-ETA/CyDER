from __future__ import division
import argparse
import sys
from functions import *
import pdb
import numpy as np
import datetime

# Retrieve model name
try:
    parser = argparse.ArgumentParser(description='Need model filename')
    # Create args and parse them
    arg_names = ['filename1', 'filename2', 'section_id1', 'nb_houses1', 'section_id2', 'nb_houses2']
    for arg_name in arg_names:
        parser.add_argument(arg_name)
    args = parser.parse_args()
    model_filename1 = str(args.filename1)
    section_id1 = str(args.section_id1)
    nb_houses1 = int(args.nb_houses1)
    model_filename2 = str(args.filename2)
    section_id2 = str(args.section_id2)
    nb_houses2 = int(args.nb_houses2)
except:
    sys.exit('Error: could not retrieve argument')

# Create time and model name vectors
nb_simulation = 30
sec_per_sim = 5
rad = np.linspace(0, 2*np.pi, num=nb_simulation)
times = np.linspace(0, len(rad) * sec_per_sim, len(rad)).tolist()
model_names1 = [model_filename1] * len(times)
model_names2 = [model_filename2] * len(times)

# Get time x label
now = datetime.datetime.now()
start = now.replace(hour=19, minute=00, second=00, microsecond=0)
time_labels = [start + datetime.timedelta(seconds=5 * index) for index in range(0, len(times))]
time_labels = [value.time() for value in time_labels]

# Generate the load profile
load_profile = [value if value < 1.3 else 1.3 for value in np.sin(rad) / 2 + 1]

# Generate the pv profile
pv_profile = np.array([value for value in np.sin(np.flipud(rad)) + 1])
pv_profile = np.array([value if value < 1 else 1 for value in pv_profile])
noise = np.random.normal(0, 0.05, len(pv_profile))
pv_profile += noise
pv_profile = np.array([value if value > 0 else 0 for value in pv_profile])
pv_profile = np.array([value if value < 1 else 1 for value in pv_profile])
input_profiles = [{'x': time_labels, 'y': load_profile, 'label': 'load profile'},
                  {'x': time_labels, 'y': pv_profile, 'label': 'pv profile'}]

# Initiate the configuration file
print('Creating a configuration file...')
parent_folder = 'D://Users//Jonathan//Documents//GitHub//PGE_Models_DO_NOT_SHARE//'
configuration = initialize_configuration(times, parent_folder, model_names1)

# Shift load and pv in the configuration file
configuration = shift_load_and_pv(load_profile, pv_profile, configuration)

# Add load and pv at the right section id
power_demand = 3 * nb_houses1
pv_generation = 4 * nb_houses1
for index, time in enumerate(configuration['times']):
    configuration['models'][index]['new_pvs'].append({'section_id': section_id1,
                                                      'generation': pv_generation * pv_profile[index]})
    configuration['models'][index]['new_loads'].append({'section_id': section_id1,
                                                        'active_power': power_demand * load_profile[index]})
# Create the configuration file
output_folder = 'D://Users//Jonathan//Documents//GitHub//configuration_files//'
configuration_filename1 = create_configuration_file(configuration, output_folder)
print('Configuration file created: ' + configuration_filename1.split('//')[-1])


# Initiate the configuration file
print('Creating a configuration file...')
parent_folder = 'D://Users//Jonathan//Documents//GitHub//PGE_Models_DO_NOT_SHARE//'
configuration = initialize_configuration(times, parent_folder, model_names2)

# Shift load and pv in the configuration file
configuration = shift_load_and_pv(load_profile, pv_profile, configuration)

# Add load and pv at the right section id
power_demand = 3 * nb_houses2
pv_generation = 4 * nb_houses2
for index, time in enumerate(configuration['times']):
    configuration['models'][index]['new_pvs'].append({'section_id': section_id2,
                                                      'generation': pv_generation * pv_profile[index]})
    configuration['models'][index]['new_loads'].append({'section_id': section_id2,
                                                        'active_power': power_demand * load_profile[index]})
# Create the configuration file
output_folder = 'D://Users//Jonathan//Documents//GitHub//configuration_files//'
configuration_filename2 = create_configuration_file(configuration, output_folder)
print('Configuration file created: ' + configuration_filename2.split('//')[-1])


start_time = times[0]
end_time = times[-1]
save_to_file = 0
result = simulate_2cymdist_gridyn_fmus(
    configuration_filename1, configuration_filename2, start_time, end_time, sec_per_sim, save_to_file, input_profiles, time_labels)
