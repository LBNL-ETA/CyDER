from __future__ import division
import argparse
import sys
import datetime
import cympy
import functions


# # Retrieve model name
# try:
#     parser = argparse.ArgumentParser(description='Needs model and upmu data')
#
#     # Create args and parse them
#     arg_names = ['filename', 'P_A', 'P_B', 'P_C', 'Q_A', 'Q_B', 'Q_C', 'VMAG_A', 'VMAG_B', 'VMAG_C']
#     for arg_name in arg_names:
#         parser.add_argument(arg_name)
#     args = parser.parse_args()
#
#     # Assign args to variable and cast right format
#     udata = {}
#     udata['P_A'] = float(args.P_A)
#     udata['P_B'] = float(args.P_B)
#     udata['P_C'] = float(args.P_C)
#
#     udata['Q_A'] = float(args.Q_A)
#     udata['Q_B'] = float(args.Q_B)
#     udata['Q_C'] = float(args.Q_C)
#
#     udata['VMAG_A'] = float(args.VMAG_A)
#     udata['VMAG_B'] = float(args.VMAG_B)
#     udata['VMAG_C'] = float(args.VMAG_C)
#
#     model_filename = str(args.filename)
#
# except:
#     sys.exit('Error: could not retrieve argument')

# Open the model
model_filename = 'AT0001.sxst'
parent_path = 'D://Users//Jonathan//Documents//GitHub//PGE_Models_DO_NOT_SHARE//'
cympy.study.Open(parent_path + model_filename)

# Get data from upmu
udata = {'VMAG_A': 7287.4208984375,
         'VMAG_B': 7299.921875,
         'VMAG_C': 7318.2822265625,
         'P_A': 7272.5364248477308,
         'P_B': 2118.3817519608633,
         'P_C': 6719.1867010705246,
         'Q_A': -284.19075651498088,
         'Q_B': -7184.1189935099919,
         'Q_C': 3564.4269660296022,
         'units': ('kW', 'kVAR', 'V')}

# Run load allocation function to set input values
functions.load_allocation(udata)

# Run the power flow
lf = cympy.sim.LoadFlow()
lf.Run()

# Get the results
nodes = functions.list_nodes()
nodes = functions.get_voltage(nodes, is_node=True)

# Print the results
for index in range(0, len(nodes)):
    print(nodes.ix[index][['node_id', 'voltage_A', 'voltage_B', 'voltage_C']].to_dict())
