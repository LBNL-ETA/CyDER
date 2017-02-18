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
    arg_names = ['filename', 'pv_section', 'pv_gen', 'load_section', 'load_demand']
    for arg_name in arg_names:
        parser.add_argument(arg_name)
    args = parser.parse_args()
    model_filename = str(args.filename)
    pv_section = str(args.pv_section)
    pv_gen = int(args.pv_gen)  # kW
    load_section = str(args.load_section)
    load_demand = int(args.load_demand)  # kW
except:
    sys.exit('Error: could not retrieve argument')

# Open the model
# model_filename = 'AT0001.sxst'
parent_path = 'D://Users//Jonathan//Documents//GitHub//PGE_Models_DO_NOT_SHARE//'
cympy.study.Open(parent_path + model_filename)

# Add PVs
pv = cympy.study.AddDevice("my_pv", cympy.enums.DeviceType.Photovoltaic, pv_section)

# Set PV size (add + 30 to make sure rated power is above generated power)
pv.SetValue(int((pv_gen + 30) / (23 * 0.08)), "Np")  # (ns=23 * np * 0.08 to find kW) --> kw / (23 * 0.08)
pv.SetValue(pv_gen, 'GenerationModels[0].ActiveGeneration')

# Set inverter size
pv.SetValue(pv_gen, "Inverter.ActivePowerRating")
pv.SetValue(pv_gen, "Inverter.ReactivePowerRating")

# Add load and overwrite (load demand need to be sum of previous load and new)
load = cympy.study.AddDevice("my_load", 14, load_section, 'DEFAULT', cympy.enums.Location.FirstAvailable , True)

# Set power demand
phases = list(cympy.study.QueryInfoDevice("Phase", "MY_LOAD", 14))
power = load_demand / len(phases)
for phase in range(0, len(phases)):
    cympy.study.SetValueDevice(
        power,
        'CustomerLoads[0].CustomerLoadModels[0].CustomerLoadValues[' + str(phase) + '].LoadValue.KW',
        "MY_LOAD", 14)
# Note: customer is still 0 as well as energy values, does it matters?

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
