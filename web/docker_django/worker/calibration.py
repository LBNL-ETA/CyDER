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
udata = functions.get_upmu_data(query_date, '/LBNL/grizzly_bus1/')
print(udata)

# # Run load allocation function to set input values
# functions.load_allocation(udata)
#
# # Run the power flow
# lf = cympy.sim.LoadFlow()
# lf.Run()
#
# # Print the results
