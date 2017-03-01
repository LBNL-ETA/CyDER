from __future__ import division
import argparse
import sys
import datetime
import cympy
from ... import cymdist


# Retrieve model name
try:
    parser = argparse.ArgumentParser(description='Option to pick a model')
    parser.add_argument('filename')
    args = parser.parse_args()
    model_filename = str(args.filename)
except:
    sys.exit('Error: could not retrieve argument')

# Open a study
filename = "C:\\Users\\Jonathan\\Documents\\GitHub\\PGE_Models_DO_NOT_SHARE\\" + model_filename
cympy.study.Open(filename)

# Get all the node informations
devices = cymdist.list_devices()
devices = cymdist.get_distance(devices)
devices = cymdist.get_coordinates(devices)

# Output to the console each line is a node
lenght = len(devices)
for index in range(0, lenght):
    print(devices.ix[index][['device_number', 'device_type', 'device_type_id',
                             'distance', 'section_id',
                             'latitude', 'longitude']].to_dict())
