from __future__ import division
import argparse
import sys
import datetime
import cympy
import functions
from random import randint
import pandas

# Retrieve model name
try:
    parser = argparse.ArgumentParser(description='Needs model and upmu data')
    # Create args and parse them
    arg_names = ['filename', 'nb_vehicles', 'time_of_day']
    for arg_name in arg_names:
        parser.add_argument(arg_name)
    args = parser.parse_args()
    model_filename = str(args.filename)
    nb_vehicles = int(args.nb_vehicles)
    time_of_day = str(args.time_of_day)
except:
    sys.exit('Error: could not retrieve argument')

# Open the model
# model_filename = 'AT0001.sxst'
parent_path = 'D://Users//Jonathan//Documents//GitHub//PGE_Models_DO_NOT_SHARE//'
cympy.study.Open(parent_path + model_filename)

# Read vehicle beahvior
df = pandas.read_csv('vehicle_charging.csv', parse_dates=[0])
df['time'] = df['datetime'].apply(lambda x: x.time())

# Get the corresponding value
time_of_day = time_of_day.split(':')
now = datetime.datetime.now()
time = now.replace(hour=int(time_of_day[0]), minute=int(time_of_day[1]), second=int(time_of_day[2]), microsecond=0).time()
vehicle_charging_coef = df[df.time == time].Home.iloc[0]

# Get all the load
devices = functions.list_devices()
power_demand = 6.6  # [kW]
ids = list(set(devices[devices.device_type_id == 14].device_number.values))
phase_dict = {'A': cympy.enums.Phase.A,
              'B': cympy.enums.Phase.B,
              'C': cympy.enums.Phase.C}

# Actual number of vehicle charging
actual_vehicle_charging = int(nb_vehicles * vehicle_charging_coef)


# Run a customize "load allocation"
vehicle_count = 0
while vehicle_count <= actual_vehicle_charging:
    # Pick a random spot load
    index = randint(0, len(ids) - 1)

    config = cympy.study.QueryInfoDevice("LoadConfig", ids[index], 14)
    phase_type = cympy.study.QueryInfoDevice("PhaseType", ids[index], 14)
    if config in 'Yg' and phase_type in 'ByPhase':
        phases = list(cympy.study.QueryInfoDevice("Phase", ids[index], 14))
        power = power_demand / len(phases)
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
