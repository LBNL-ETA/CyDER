import btrdb
import datetime
import numpy as np
import uuid
import pytz
import pandas
import argparse
import pdb
import sys


def convert_datetime_to_epoch_ns(dt):
    #converts the datetime object to epoch time in nanoseconds
    return (int(dt.strftime('%s')) * 1e6 + dt.microsecond) * 1e3


def get_upmu_data(dates, PMU_name):
    """Retrieves instantaneous P, Q, and voltage magnitude for specified datetime.

    Args:
        dates (datetime): list of datetime objects
        PMU_name (str): e.g., 'grizzly_bus1'
    Returns:
        {'P_A': , 'Q_A': , 'P_B': , 'Q_B': , 'P_C': , 'Q_C': ,
         'units': ('kW', 'kVAR'),
         'VMag_A': , 'VMag_B': , 'VMag_C': }
    """

    # Change all the dates into epoch time in nanoseconds
    event_times = [convert_datetime_to_epoch_ns(value) for value in dates]

    # Get the ids of the parameters to retrieve (each id is location and measure type unique)
    path = "CyDER/web/docker_django/worker/upmu/"
    ids = str(np.genfromtxt(path + PMU_name + '_uuids.txt', dtype='str')).split(',')
    ids = [uuid.UUID(value) for value in ids]
    names = ["L1Mag", "L2Mag", "L3Mag", "C1Mag", "C2Mag", "C3Mag",
            "L1Ang", "L2Ang", "L3Ang", "C1Ang", "C2Ang", "C3Ang"]
    result_names = ['P_A', 'Q_A', 'P_B', 'Q_B', 'P_C', 'Q_C', 'VMAG_A',
                    'VMAG_B', 'VMAG_C', 'datetime', 'epoch_time', 'units']

    # Create the frame holding the measured data and the results
    column_names = []
    column_names.extend(names)
    column_names.extend(result_names)
    frame = pandas.DataFrame(index=event_times, columns=column_names)

    # Query the values
    for value_epoch_time, value_date in zip(event_times, dates):
        for value_id, value_name in zip(ids, names):
            query = connection.queryNearestValue(value_id, value_epoch_time, True, version=0)
            frame.loc[value_epoch_time, value_name] = query[0][0][1]

    # Calculate the results
    frame['P_A'] = (frame['L1Mag']*frame['C1Mag']*np.cos(np.radians(list(frame['L1Ang'] - frame['C1Ang']))))*1e-3
    frame['Q_A'] = (frame['L1Mag']*frame['C1Mag']*np.sin(np.radians(list(frame['L1Ang'] - frame['C1Ang']))))*1e-3

    frame['P_B'] = (frame['L2Mag']*frame['C2Mag']*np.cos(np.radians(list(frame['L2Ang'] - frame['C2Ang']))))*1e-3
    frame['Q_B'] = (frame['L2Mag']*frame['C2Mag']*np.sin(np.radians(list(frame['L2Ang'] - frame['C2Ang']))))*1e-3

    frame['P_C'] = (frame['L3Mag']*frame['C3Mag']*np.cos(np.radians(list(frame['L3Ang'] - frame['C3Ang']))))*1e-3
    frame['Q_C'] = (frame['L3Mag']*frame['C3Mag']*np.sin(np.radians(list(frame['L3Ang'] - frame['C3Ang']))))*1e-3
    frame['units'] = [('kW', 'kVAR', 'V', 'A', 'deg') for index in range(0, len(frame))]
    frame['datetime'] = [value.strftime("%Y-%m-%d %H:%M:%S") for value in dates]

    # Added for simplicity
    frame['epoch_time'] = event_times
    frame['VMAG_A'] = frame['L1Mag']
    frame['VMAG_B'] = frame['L2Mag']
    frame['VMAG_C'] = frame['L3Mag']

    return frame


# Retrieve input
try:
    parser = argparse.ArgumentParser(description='Select dates and location')
    parser.add_argument('date_from')
    parser.add_argument('date_to')
    parser.add_argument('location')
    args = parser.parse_args()
    date_from = str(args.date_from)
    date_to = str(args.date_to)
    location = str(args.location)
except:
    sys.exit('Error: could not retrieve argument')

# Connect to the database
connection = btrdb.BTrDBConnection("miranda.cs.berkeley.edu", 4410)
context = connection.newContext()

# Create datetimes every minutes with "date_from" and "date_to"
western = pytz.timezone('America/Los_Angeles')
date_from = datetime.datetime.strptime(date_from, "%Y-%m-%d_%H:%M:%S")
if not date_to in "False":
    date_to = datetime.datetime.strptime(date_to, "%Y-%m-%d_%H:%M:%S")
    delta_minutes = int((date_to - date_from).total_seconds() / 60)

    # Check that the delta minute is reasonable
    if delta_minutes < 1:
        raise Exception('Need at least a minute between date_to and date_from')
    elif delta_minutes > 20000:
        raise Exception('Limited to 20000 minutes (less than 2 weeks)')

    # Create the list of dates with the appropriate time zone
    dates = [western.localize(date_from + datetime.timedelta(minutes=x)) for x in range(0, delta_minutes)]
else:
    dates = [western.localize(date_from)]

# Get the data from the database for each datetime at location
frame = get_upmu_data(dates, location)

# Print the output
for index in range(0, len(frame)):
    print(frame.iloc[index].to_dict())
