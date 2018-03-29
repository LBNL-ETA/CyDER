from __future__ import division
import matplotlib.pyplot as plt
import pandas
import datetime as dt

def scada_profile(start, end, substation):
    # Open SCADA data
    scada = pandas.read_csv('C:/Users/DRRC/Desktop/raw_SCADA/'+ substation + '.csv', parse_dates=[0])
    scada = scada.set_index('TIME')

    # filter, sum, and interpolate
    total_mw = scada[start:end].filter(regex=(".*MW"))
    total_mw = total_mw.sum(axis=1) * 1000.0  # convertion from MW to kW
    total_mw = total_mw.resample('15T').interpolate('time')
    return total_mw
