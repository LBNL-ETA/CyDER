from __future__ import division
import argparse
import sys
import datetime
import cympy
import functions
from random import randint


# Retrieve model name
try:
    parser = argparse.ArgumentParser(description='Needs model and upmu data')
    # Create args and parse them
    arg_names = ['filename', 'nb_vehicles']
    for arg_name in arg_names:
        parser.add_argument(arg_name)
    args = parser.parse_args()
    model_filename = str(args.filename)
    nb_vehicles = int(args.nb_vehicles)
except:
    sys.exit('Error: could not retrieve argument')

# Open the model
# model_filename = 'AT0001.sxst'
parent_path = 'D://Users//Jonathan//Documents//GitHub//PGE_Models_DO_NOT_SHARE//'
cympy.study.Open(parent_path + model_filename)

# Select the section id
nodes = functions.list_nodes()
ids = list(set(nodes.section_id.values()))
power_demand = [0] * len(ids)

# For each vehicle plugged
for index in range(0, nb_vehicles):
    # Pick a random number from 0 to len(ids)
    x = randint(0, len(ids))
    # Assign power demand
    power_demand[x] += 6600

# Add a load on the section with a non null power demand
for pk, power in zip(ids, power_demand):
    if power != 0:
        device = functions.add_device(device_name, cympy.enums.DeviceType.Photovoltaic, pk)
        SetInfoDevice(device, "load", power)

# Run the power flow
lf = cympy.sim.LoadFlow()
lf.Run()

# Get the results
# nodes = functions.list_nodes()
nodes = functions.get_voltage(nodes, is_node=True)

# Replace nan value by None
nodes = nodes.fillna("None")

# Print the results
for index in range(0, len(nodes)):
    print(nodes.ix[index][['node_id', 'voltage_A', 'voltage_B', 'voltage_C', 'latitude', 'longitude', 'distance']].to_dict())
