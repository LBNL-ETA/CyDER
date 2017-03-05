import time
import pdb
import matplotlib.pyplot as plt
plt.switch_backend('Qt4Agg')
import numpy as np
import seaborn
import argparse
import sys
import datetime
import pandas

# Retrieve model name
try:
    parser = argparse.ArgumentParser(description='Need model filename')
    # Create args and parse them
    arg_names = ['filename', 'nb_evs', 'start', 'end']
    for arg_name in arg_names:
        parser.add_argument(arg_name)
    args = parser.parse_args()
    model_filename = str(args.filename)
    nb_evs = int(args.nb_evs)
    start = str(args.start)
    end = str(args.end)
except:
    sys.exit('Error: could not retrieve argument')

# Read vehicle beahvior
df = pandas.read_csv('evs/vehicle_charging.csv', parse_dates=[0])
df['time'] = df['datetime'].apply(lambda x: x.time())

# Get the corresponding value
now = datetime.datetime.now()
start = start.split(':')
start = now.replace(hour=int(start[0]), minute=int(start[1]), second=int(start[2]), microsecond=0)
end = end.split(':')
end = now.replace(hour=int(end[0]), minute=int(end[1]), second=int(end[2]), microsecond=0)
times = [start]
while times[-1] < end:
    times.append(times[-1] + datetime.timedelta(minutes=10))
times = [value.time() for value in times]
vehicle_charging_coefs = df[df.time.isin(times)].Home.tolist()

# seaborn.set_style("whitegrid")
# seaborn.despine()
# plt.close()
#
# # Plot reference
# nb_simulation = 30
# sec_per_sim = 5
# rad = np.linspace(0, 2*np.pi, num=nb_simulation)
# x = np.linspace(0, len(rad) * sec_per_sim, len(rad)) / 60
# y = [value if value < 1.3 else 1.3 for value in np.sin(rad) / 2 + 1]
# y2 = np.array([value for value in np.sin(np.flipud(rad)) + 1])
# y2 = np.array([value if value < 1 else 1 for value in y2])
# noise = np.random.normal(0, 0.05, len(y2))
# y2 += noise
# y2 = np.array([value if value > 0 else 0 for value in y2])
# y2 = np.array([value if value < 1 else 1 for value in y2])
#
#
#
# # Create the vectors
# times = np.linspace(0, len(rad) * sec_per_sim, len(rad)) / 60
# currents = np.random.normal(0, 0.1, len(times))
# voltages = np.random.normal(0, 0.1, len(times))
#
# # Interactive mode on
# plt.ion()
#
# # Create the plot
# fig = plt.figure()
# ax = fig.add_subplot(311)
# ax1 = fig.add_subplot(312)
# ax2 = fig.add_subplot(313)
# ax.set_ylabel('Coefficient')
# ax1.set_ylabel('Currents [A]')
# ax2.set_ylabel('Voltages [V]')
# ax2.set_xlabel('Time (minutes)')
# line, = ax.plot(x, y, 'b-')
# line, = ax.plot(x, y2, 'r-')
# line1, = ax1.plot([], [], 'b-')
# line2, = ax2.plot([], [], 'r-')
#
# for index, t in enumerate(times):
#     time.sleep(1)
#     line1.set_xdata(times[:index + 1])
#     line1.set_ydata(currents[:index + 1])
#     line2.set_xdata(times[:index + 1])
#     line2.set_ydata(voltages[:index + 1])
#     ax1.relim()
#     ax1.autoscale_view(True,True,True)
#     ax2.relim()
#     ax2.autoscale_view(True,True,True)
#     fig.canvas.draw()
#     plt.pause(0.01)
