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
    arg_names = ['filename1', 'filename2', 'nb_evs1', 'nb_evs2', 'start', 'end']
    for arg_name in arg_names:
        parser.add_argument(arg_name)
    args = parser.parse_args()
    model_filename1 = str(args.filename1)
    model_filename2 = str(args.filename2)
    nb_evs1 = int(args.nb_evs1)
    nb_evs2 = int(args.nb_evs2)
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
model_names1 = [model_filename1] * len(times)
model_names2 = [model_filename2] * len(times)

# Generate the load profile
ev_profile1 = [int(coef * nb_evs1) for coef in vehicle_charging_coefs]
ev_profile2 = [int(coef * nb_evs2) for coef in vehicle_charging_coefs]

# Initiate the configuration file
print('Creating a configuration file...')
parent_folder = 'D://Users//Jonathan//Documents//GitHub//PGE_Models_DO_NOT_SHARE//'
configuration = initialize_configuration(times, parent_folder, model_names1)

# Shift load for ev consumers
configuration = ev_consumption(ev_profile1, configuration)

# Create the configuration file
output_folder = 'D://Users//Jonathan//Documents//GitHub//configuration_files//'
configuration_filename1 = create_configuration_file(configuration, output_folder)
print('Configuration file created: ' + configuration_filename1.split('//')[-1])

# Initiate the configuration file
print('Creating a configuration file...')
parent_folder = 'D://Users//Jonathan//Documents//GitHub//PGE_Models_DO_NOT_SHARE//'
configuration = initialize_configuration(times, parent_folder, model_names2)

# Shift load for ev consumers
configuration = ev_consumption(ev_profile2, configuration)

# Create the configuration file
output_folder = 'D://Users//Jonathan//Documents//GitHub//configuration_files//'
configuration_filename2 = create_configuration_file(configuration, output_folder)
print('Configuration file created: ' + configuration_filename2.split('//')[-1])

start_time = times[0]
end_time = times[-1]
save_to_file = 0
result = simulate_2cymdist_gridyn_fmus(
    configuration_filename1, configuration_filename2, start_time, end_time, sec_per_sim, save_to_file, input_profiles, time_labels)
