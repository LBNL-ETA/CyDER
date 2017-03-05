from __future__ import division
import argparse
import sys
from functions import *
import pdb
import numpy as np

# Retrieve model name
try:
    parser = argparse.ArgumentParser(description='Need model filename')
    # Create args and parse them
    arg_names = ['filename', 'section_id', 'nb_houses']
    for arg_name in arg_names:
        parser.add_argument(arg_name)
    args = parser.parse_args()
    model_filename = str(args.filename)
    section_id = str(args.section_id)
    nb_houses = int(args.nb_houses)
except:
    sys.exit('Error: could not retrieve argument')

# Create time and model name vectors
nb_simulation = 30
sec_per_sim = 0.5
rad = np.linspace(0, 2*np.pi, num=nb_simulation)
times = np.linspace(0, len(rad) * sec_per_sim, len(rad)).tolist()
model_names = [model_filename] * len(times)

# Generate the load profile
load_profile = [value if value < 1.3 else 1.3 for value in np.sin(rad) / 2 + 1]

# Generate the pv profile
pv_profile = np.array([value for value in np.sin(np.flipud(rad)) + 1])
pv_profile = np.array([value if value < 1 else 1 for value in pv_profile])
noise = np.random.normal(0, 0.05, len(pv_profile))
pv_profile += noise
pv_profile = np.array([value if value > 0 else 0 for value in pv_profile])
pv_profile = np.array([value if value < 1 else 1 for value in pv_profile])

# Initiate the configuration file
configuration = initialize_configuration(times, model_names)

# Shift load and pv in the configuration file
configuration = shift_load_and_pv(load_profile, pv_profile, configuration)

# Add load and pv at the right section id
power_demand = 3 * nb_houses
pv_generation = 4 * nb_houses
for index, time in enumerate(configuration['times']):
    configuration['models'][index]['new_pvs'].append({'section_id': section_id,
                                                      'generation': pv_generation * pv_profile[index]})
    configuration['models'][index]['new_loads'].append({'section_id': section_id,
                                                        'active_power': power_demand * load_profile[index]})
# Create the configuration file
configuration_filename = create_configuration_file(configuration)

start_time = times[0]
end_time = times[-1]
save_to_file = 0
result = simulate_cymdist_gridyn_fmus(configuration_filename, start_time, end_time, sec_per_sim, save_to_file)
