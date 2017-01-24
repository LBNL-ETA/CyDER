from __future__ import division
import argparse
import sys
import datetime
import cympy
import functions


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
    udata['P_A'] = float(args.P_A)
    udata['P_B'] = float(args.P_B)
    udata['P_C'] = float(args.P_C)

    udata['Q_A'] = float(args.Q_A)
    udata['Q_B'] = float(args.Q_B)
    udata['Q_C'] = float(args.Q_C)

    udata['VMAG_A'] = float(args.VMAG_A)
    udata['VMAG_B'] = float(args.VMAG_B)
    udata['VMAG_C'] = float(args.VMAG_C)

    model_filename = str(args.filename)
    breaker_name = str(args.breaker_name)
    breaker_type = str(args.breaker_type)

except:
    sys.exit('Error: could not retrieve argument')

# Open the model
parent_path = 'D://Users//Jonathan//Documents//GitHub//PGE_Models_DO_NOT_SHARE//'
cympy.study.Open(parent_path + model_filename)

# Run load allocation function to set input values
functions.load_allocation(udata)

# Run the power flow
lf = cympy.sim.LoadFlow()
lf.Run()

# Get the positive sequence current
current_positive_sequence = cympy.study.QueryInfoDevice("I1", breaker_name, int(breaker_type))

# # Print the results
print(udata)  # upmu data
print({'i1': current_positive_sequence})  # voltage results
