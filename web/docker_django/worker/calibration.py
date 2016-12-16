from __future__ import division
# import argparse
import sys
# import cympy
import functions
import datetime


# # Retrieve model name
# try:
#     parser = argparse.ArgumentParser(description='Option to pick a model')
#     parser.add_argument('filename')
#     parser.add_argument('upmu_location')
#     model_filename = str(args.filename)
#     upmu_location = str(args.upmu_location)
# except:
#     sys.exit('Error: could not retrieve argument')
#
#
# # Open the model
# cympy.study.Open(model_filename)

# Get data from upmu
query_date = datetime.datetime.now() + datetime.timedelta(hours=1)
# udata = functions.get_upmu_data(query_date, '/LBNL/grizzly_bus1/')
# Retrieve microPMU data at t
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
print(udata)

# # Run load allocation function to set input values
# functions.load_allocation(udata)
#
# # Run the power flow
# lf = cympy.sim.LoadFlow()
# lf.Run()
#
# # Print the results
