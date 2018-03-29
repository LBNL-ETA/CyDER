from __future__ import division
import matplotlib.pyplot as plt
import pandas
import datetime as dt


def solar_profile(start, end, pv_nominal_capacity_kw):
    """
    Output solar generation profile based on GHI data (timestep 15 minutes)
    GHI data is normalized based on 1 --> 1000 w/m2
    Source: NSRDB, Location ID: 146312, Lat: 39.81, Long: 123.5, Elev: 1024
    URL: https://maps.nrel.gov/nsrdb-viewer/?aL=UdPEX9%255Bv%255D%3Dt%268VW
    YIh%255Bv%255D%3Dt%268VWYIh%255Bd%255D%3D1&bL=clight&cE=0&lR=0&mC=39.91
    605629078665%2C-123.0084228515625&zL=9
    """
    # Load data from the raw CSV file
    df = pandas.read_csv('sim_worker/solar.csv', skiprows=[0, 1])
    df.drop(['Relative Humidity', 'Temperature', 'Pressure'],
            axis=1, inplace=True)
    df['Time'] = df.apply(lambda x: dt.datetime(
        x['Year'], x['Month'], x['Day'], x['Hour'], x['Minute'], 0), axis=1)
    df.set_index('Time', inplace=True)
    df.drop(['Year', 'Month', 'Day', 'Hour', 'Minute'], axis=1, inplace=True)

    # Select data, normailize, and interpolate every 15 minutes
    df = df[start:end]
    df = df / 1000.0
    df = df.resample('15T').interpolate('time')

    # Multiply by pv nominal capacity
    return df * pv_nominal_capacity_kw
