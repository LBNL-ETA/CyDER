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
devices = functions.list_devices()
power_demand = 6.6  # [kW]
ids = list(set(devices[devices.device_type_id == 14].device_number.values))
phase_dict = {'A': cympy.enums.Phase.A,
              'B': cympy.enums.Phase.B,
              'C': cympy.enums.Phase.C}

vehicle_count = 0
while vehicle_count <= nb_vehicles:
    # Pick a random spot load
    index = randint(0, len(ids))
    
    config = cympy.study.QueryInfoDevice("LoadConfig", ids[index], 14)
    phase_type = cympy.study.QueryInfoDevice("PhaseType", ids[index], 14)
    if config in 'Yg' and phase_type in 'ByPhase':
        phases = list(cympy.study.QueryInfoDevice("Phase", ids[index], 14))
        power = power_demand / len(phases)
        print(ids[index])
        print(phases)
        for phase in range(0, len(phases)):
            cympy.study.SetValueDevice(
                power,
                'CustomerLoads[0].CustomerLoadModels[0].CustomerLoadValues[' + str(phase) + '].LoadValue.KW',
                ids[index], 14)
        vehicle_count += 1

    else:
        # Pick another node
        Flag = False

# Run the power flow
lf = cympy.sim.LoadFlow()
lf.Run()

# Get the results
nodes = functions.list_nodes()
nodes = functions.get_voltage(nodes, is_node=True)

# Replace nan value by None
nodes = nodes.fillna("None")

# Print the results
for index in range(0, len(nodes)):
    print(nodes.ix[index][['node_id', 'voltage_A', 'voltage_B', 'voltage_C', 'latitude', 'longitude', 'distance']].to_dict())
