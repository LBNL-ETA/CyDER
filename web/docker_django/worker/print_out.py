import argparse
import pandas

# Retrieve model name
try:
    parser = argparse.ArgumentParser(description='Option to pick a model')
    parser.add_argument('filename')
    parser.add_argument('header')
    args = parser.parse_args()
    filename = str(args.filename)
    header = str(args.header)
except:
    sys.exit('Error: could not retrieve argument')

# Save
frame = pandas.read_csv(filename)

if header in ['nodes']:
    header = ['node_id', 'section_id', 'latitude', 'longitude']
elif header in ['devices']:
    header = ['device_number', 'device_type', 'device_type_id',
              'distance', 'section_id', 'latitude', 'longitude']

# Output to the console each line is a node
for index in range(0, len(frame)):
    print(frame.ix[index][header].to_dict())
