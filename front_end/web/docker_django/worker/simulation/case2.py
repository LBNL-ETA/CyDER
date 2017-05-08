from __future__ import division
import argparse
import sys
from functions import *
import pdb
import pandas
import numpy as np
import datetime

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

# Read vehicle beahvior
df = pandas.read_csv('~/project_cyder/web/docker_django/worker/simulation/evs/vehicle_charging.csv', parse_dates=[0])
df['time'] = df['datetime'].apply(lambda x: x.time())

# Get the corresponding value
now = datetime.datetime.now()
start = start.split(':')
start = now.replace(hour=int(start[0]), minute=int(start[1]), second=int(start[2]), microsecond=0)
end = end.split(':')
end = now.replace(hour=int(end[0]), minute=int(end[1]), second=int(end[2]), microsecond=0)
times = [start]
while times[-1] < end:
    times.append(times[-1] + datetime.timedelta(minutes=5))
times = [value.time() for value in times]
time_labels = times
vehicle_charging_coefs = df[df.time.isin(times)].Home.tolist()
input_profiles = [{'x': time_labels, 'y': vehicle_charging_coefs, 'label': 'vehicle profile'}]

# Create time and model name vectors
sec_per_sim = 5 * 60
times = np.linspace(0, len(vehicle_charging_coefs) * sec_per_sim, len(vehicle_charging_coefs)).tolist()
model_names = [model_filename] * len(times)

# Generate the load profile
ev_profile = [int(coef * nb_evs) for coef in vehicle_charging_coefs]

# Initiate the configuration file
print('Creating a configuration file...')
parent_folder = 'D://Users//Jonathan//Documents//GitHub//PGE_Models_DO_NOT_SHARE//'
configuration = initialize_configuration(times, parent_folder, model_names)

# Shift load for ev consumers
configuration = ev_consumption(ev_profile, configuration)

# Create the configuration file
output_folder = 'D://Users//Jonathan//Documents//GitHub//configuration_files//'
configuration_filename = create_configuration_file(configuration, output_folder)
print('Configuration file created: ' + configuration_filename.split('//')[-1])

start_time = times[0]
end_time = times[-1]
save_to_file = 0
result = simulate_cymdist_gridyn_fmus(
    configuration_filename, start_time, end_time, sec_per_sim, save_to_file, input_profiles, time_labels)
