from __future__ import division
import argparse
import sys
import datetime
import cympy
import functions


# Retrieve model name
try:
    parser = argparse.ArgumentParser(description='Option to pick a model')
    parser.add_argument('filename')
    parser.add_argument('temp_filename')
    args = parser.parse_args()
    model_filename = str(args.filename)
    temp_filename = str(args.temp_filename)
except:
    sys.exit('Error: could not retrieve argument')

# Open a study
filename = "C:\\Users\\Jonathan\\Documents\\GitHub\\PGE_Models_DO_NOT_SHARE\\" + model_filename
cympy.study.Open(filename)

# Get all the node informations
nodes = functions.list_nodes()

# Save
nodes.to_csv(temp_filename)
