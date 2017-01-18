import btrdb
import datetime as d
import numpy as np
import uuid
import pytz
from datetime import datetime
import pandas as pd

def ConvertDateTimeToEpoch_ns(dt):
    #converts the datetime object to epoch time in nanoseconds
    return (int(dt.strftime('%s'))*1e6 + dt.microsecond)*1e3

def get_upmu_data(event_time, PMU_name):
    """Retrieves instantaneous P, Q, and voltage magnitude for specified datetime.

    Args:
        inputdt (datetime): timezone aware datetime object
        upmu_path (str): e.g., '/LBNL/grizzly_bus1/'
    Returns:
        {'P_A': , 'Q_A': , 'P_B': , 'Q_B': , 'P_C': , 'Q_C': ,
         'units': ('kW', 'kVAR'),
         'VMag_A': , 'VMag_B': , 'VMag_C': }
    """

    uuid_str = str(np.genfromtxt(PMU_name + '_uuids.txt',dtype='str')).split(',')
    uuid_name = ["L1Mag", "L2Mag", "L3Mag", "C1Mag", "C2Mag", "C3Mag", \
                 "L1Ang", "L2Ang", "L3Ang", "C1Ang", "C2Ang", "C3Ang"]

    data_full = []

    u = []
    for i in range(0,len(uuid_str)):
        u.append(uuid.UUID(uuid_str[i]))

    st = ConvertDateTimeToEpoch_ns(event_time)
    et = st + 10e9

    for i in range(0,len(u)):
        results = connection.queryStandardValues(u[i], st, et, version=0)

        times_full = []
        vals_full = []

        for j in range(0,len(results[0])):
            times_full.append(results[0][j][0])
            vals_full.append(results[0][j][1])


        #check if we're pulling angle measurements

        data_full.append(vals_full)

    data_full = np.array(data_full).transpose()

#data has n entries, each is a list of measurements
    df_full = pd.DataFrame(data_full, columns=uuid_name, index=times_full)

    output_dict = {}

    df_full['P_A'] = (df_full['L1Mag']*df_full['C1Mag']*np.cos(np.radians(df_full['L1Ang'] - df_full['C1Ang'])))*1e-3
    df_full['Q_A'] = (df_full['L1Mag']*df_full['C1Mag']*np.sin(np.radians(df_full['L1Ang'] - df_full['C1Ang'])))*1e-3

    df_full['P_B'] = (df_full['L2Mag']*df_full['C2Mag']*np.cos(np.radians(df_full['L2Ang'] - df_full['C2Ang'])))*1e-3
    df_full['Q_B'] = (df_full['L2Mag']*df_full['C2Mag']*np.sin(np.radians(df_full['L2Ang'] - df_full['C2Ang'])))*1e-3

    df_full['P_C'] = (df_full['L3Mag']*df_full['C3Mag']*np.cos(np.radians(df_full['L3Ang'] - df_full['C3Ang'])))*1e-3
    df_full['Q_C'] = (df_full['L3Mag']*df_full['C3Mag']*np.sin(np.radians(df_full['L3Ang'] - df_full['C3Ang'])))*1e-3

    return df_full

connection = btrdb.BTrDBConnection("miranda.cs.berkeley.edu", 4410)
context = connection.newContext()

western = pytz.timezone('America/Los_Angeles')
time_period = western.localize(datetime(2016,11,1,12,0,0))





print("Retrieving data...")
upmudata = get_upmu_data(time_period, '/LBNL/grizzly_bus1/')
print(upmudata)
