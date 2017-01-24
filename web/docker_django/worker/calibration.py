from __future__ import division
import argparse
import sys
import datetime
# import cympy
# import functions


# Retrieve model name
try:
    parser = argparse.ArgumentParser(description='Needs model and upmu data')

    # Create args and parse them
    arg_names = ['filename', 'breaker_name', 'breaker_type', 'P_A', 'P_B', 'P_C', 'Q_A', 'Q_B', 'Q_C', 'VMAG_A', 'VMAG_B', 'VMAG_C']
    for arg_name in arg_names:
        parser.add_argument(arg_name)
    args = parser.parse_args()

    # Assign args to variable and cast right format
    udata = {}
    for arg_name in ['P_A', 'P_B', 'P_C', 'Q_A', 'Q_B', 'Q_C', 'VMAG_A', 'VMAG_B', 'VMAG_C']:
        udate[arg_name] = float(args[arg_name])
    model_filename = str(args.filename)
    breaker_name = str(args.breaker_name)
    breaker_type = str(args.breaker_type)

except:
    sys.exit('Error: could not retrieve argument')

# Open the model
parent_path = 'some path'
cympy.study.Open(parent_path + model_filename)

# # Get data from upmu
# udata = {'VMAG_A': 7287.4208984375,
#          'VMAG_B': 7299.921875,
#          'VMAG_C': 7318.2822265625,
#          'P_A': 7272.5364248477308,
#          'P_B': 2118.3817519608633,
#          'P_C': 6719.1867010705246,
#          'Q_A': -284.19075651498088,
#          'Q_B': -7184.1189935099919,
#          'Q_C': 3564.4269660296022,
#          'units': ('kW', 'kVAR', 'V')}

# Run load allocation function to set input values
functions.load_allocation(udata)

# Run the power flow
lf = cympy.sim.LoadFlow()
lf.Run()

# Get the voltages at breaker
v_A = cympy.study.QueryInfoDevice("VpuA", breaker_name, int(breaker_type))
v_B = cympy.study.QueryInfoDevice("VpuB", breaker_name, int(breaker_type))
v_C = cympy.study.QueryInfoDevice("VpuC", breaker_name, int(breaker_type))

i_A = cympy.study.QueryInfoDevice("VpuA", breaker_name, int(breaker_type))
i_B = cympy.study.QueryInfoDevice("VpuB", breaker_name, int(breaker_type))
i_C = cympy.study.QueryInfoDevice("VpuC", breaker_name, int(breaker_type))

# # Print the results
print(udata)  # upmu data
print({'A': v_A, 'B': v_B, 'C': v_C})  # voltage results
print({'A': i_A, 'B': i_B, 'C': i_C})  # current results
