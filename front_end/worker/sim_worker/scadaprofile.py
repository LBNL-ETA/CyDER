from __future__ import division
import matplotlib.pyplot as plt
import pandas
import datetime as dt

def scada_profile(start, end, substation):
    """Output scada data at substation level in kW"""
    # Open SCADA data
    scada = pandas.read_csv('raw_SCADA/'+ substation + '.csv', parse_dates=[0])
    scada = scada.set_index('TIME')

    # filter, sum, and interpolate
    total_mw = scada[start:end].filter(regex=(".*MW"))
    total_mw = total_mw.sum(axis=1) * 1000.0  # convertion from MW to kW
    total_mw = total_mw.resample('15T').interpolate('time')
    return total_mw

# ###############################
# HOW TO USE
start = '2016-06-17 00:00:00'
end = '2016-06-18 00:00:00'
substation = 'BU0006'
profile = scada_profile(start, end, substation)

# Plot profile
plt.figure(figsize=(11, 5))
plt.plot(profile)
plt.ylabel('Active power [kW]')
plt.show()
