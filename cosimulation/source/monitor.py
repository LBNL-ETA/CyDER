from __future__ import division
import matplotlib
from matplotlib.ticker import FormatStrFormatter
import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter
import numpy
import datetime
import json
plt.switch_backend('Qt4Agg')


class Monitor(object):
    """Monitor simulation progress"""

    def __init__(self):
        self.fig = None
        self.ax1 = None
        self.ax2 = None
        self.current_a = None
        self.current_b = None
        self.current_c = None
        self.voltage_abc = None

        # Initialize monitor
        self.initialize()

    def initialize(self):
        """Initialize graphs"""
        # Interactive mode on
        plt.ion()

        # Create the plot
        self.fig = plt.figure()
        self.fig.suptitle('Feeder voltage and current on phase A')
        self.ax1 = self.fig.add_subplot(211)
        self.ax2 = self.fig.add_subplot(212)
        self.ax1.set_ylabel('CymDIST currents [A]')
        self.ax2.set_ylabel('GridDyn voltages [V]')
        self.ax2.yaxis.set_major_formatter(FormatStrFormatter('%.2f'))
        self.ax2.set_xlabel('Time (minutes)')

        # Create lines
        self.current_a, = self.ax1.plot([], [], label='Phase A')
        # self.current_b, = self.ax1.plot([], [], label='Phase B')
        # self.current_c, = self.ax1.plot([], [], label='Phase C')
        self.voltage_abc, = self.ax2.plot([], [], label='Balanced accross phases')

        # Add legends and tight layout
        self.ax1.legend(loc=1)
        self.ax2.legend(loc=1)
        self.fig.tight_layout()

        # Adjust plot to leave some space for the title
        self.fig.subplots_adjust(top=0.88)

    def update(self, master):
        """Visualize simulation progress"""
        # Find current index
        index = len(master.feeder_result[0]['IA'])
        x = numpy.array(master.times[0:index]) / 60

        # Update plot values
        self.current_a.set_xdata(x)
        self.current_a.set_ydata(master.feeder_result[0]['IA'])
        # self.current_b.set_xdata(x)
        # self.current_b.set_ydata(master.feeder_result[0]['IB'])
        # self.current_c.set_xdata(x)
        # self.current_c.set_ydata(master.feeder_result[0]['IC'])
        self.voltage_abc.set_xdata(x)
        self.voltage_abc.set_ydata(master.transmission_result['Bus11_VA'])

        # Redefine graph scale
        self.ax1.relim()
        self.ax1.autoscale_view(True,True,True)
        self.ax2.relim()
        self.ax2.autoscale_view(True,True,True)

        # Update plot
        self.fig.canvas.draw()
        plt.pause(0.01)


def format_configuration_to_plot(start, configuration):
    """Return x and y vectors to plot the configuration"""
    # Create y and x vectors
    pv = [0] * len(configuration['times'])
    ev = [0] * len(configuration['times'])
    load = [0] * len(configuration['times'])
    dates = [start + datetime.timedelta(seconds=value)
             for value in configuration['times']]

    # Get the y values (generation and load versus time)
    for index, model in enumerate(configuration['models']):
        for set_load in model['set_loads']:
            if set_load['description'] in 'load forecast':
                for phase in set_load['active_power']:
                    load[index] += phase['active_power']
            else:
                for phase in set_load['active_power']:
                    ev[index] += phase['active_power']

        for set_pv in model['set_pvs']:
            pv[index] += set_pv['generation']

    return (dates, [{'y': load, 'label': 'Load demand'},
                    {'y': pv, 'label': 'PV generation'},
                    {'y': ev, 'label': 'EV demand'}])


def plot_post_simulation(start, configuration, directory, pk):
    """Plot configuration and some inside data from the feeder models"""
    # Get data for the configuration plot
    x, ys = format_configuration_to_plot(start, configuration)

    # Get data for the post simulation plot
    keys = ['DwLowVoltWorstA', 'DwLowVoltWorstB', 'DwLowVoltWorstC']
    timeseries = {key: [] for key in keys}

    # Loop over all the files
    for time in configuration['times']:
        with open(directory + str(pk) + '/' + str(time) + '.json') as f:
            data = json.load(f)
        for key in keys:
            timeseries[key].append(data[key])

    # Create plot
    fig = plt.figure(figsize=(10, 10), dpi=95)
    fig.suptitle('Under Voltage on the feeder')
    ax1 = fig.add_subplot(211)
    ax2 = fig.add_subplot(212)
    formatter = DateFormatter('%H:%M')
    ax1.xaxis.set_major_formatter(formatter)
    ax2.xaxis.set_major_formatter(formatter)
    ax1.set_ylabel('Input scenario [kW]')
    ax2.set_ylabel('Worst Under-voltage [%]')
    ax2.set_xlabel('Time')

    # Create lines
    for y in ys:
        ax1.plot(x, y['y'], label=y['label'])

    for key in keys:
        ax2.plot(x, timeseries[key], label=key)

    # Add legends and tight layout
    ax1.legend(loc=0)
    ax2.legend(loc=0)
    fig.tight_layout()

    # Adjust plot to leave some space for the title
    fig.subplots_adjust(top=0.95)

    # Show
    plt.show()
    plt.pause(1)
    import pdb; pdb.set_trace()


class Monitor2Feeder(object):
    """Monitor simulation progress"""

    def __init__(self):
        self.fig = None
        self.ax1 = None
        self.ax2 = None
        self.ax3 = None
        self.current_a_bus11 = None
        self.current_a_bus10 = None
        self.voltage_abc_bus11 = None
        self.voltage_abc_bus10 = None

        # Initialize monitor
        self.initialize()

    def initialize(self):
        """Initialize graphs"""
        # Interactive mode on
        plt.ion()

        # Create the plot
        self.fig = plt.figure(figsize=(10, 10), dpi=95)
        self.fig.suptitle('Feeder voltages and currents on phase B')
        self.ax1 = self.fig.add_subplot(311)
        self.ax2 = self.fig.add_subplot(312)
        self.ax3 = self.fig.add_subplot(313)
        self.ax1.set_ylabel('Feeder A currents [A]')
        self.ax2.set_ylabel('Feeder B currents [A]')
        self.ax3.set_ylabel('Feeder voltages [V]')
        self.ax3.yaxis.set_major_formatter(FormatStrFormatter('%.2f'))
        self.ax3.set_xlabel('Time (minutes)')

        # Create lines
        self.current_a_bus11, = self.ax1.plot([], [], label='Phase B')
        self.current_a_bus10, = self.ax2.plot([], [], label='Phase B')
        # self.current_b, = self.ax1.plot([], [], label='Phase B')
        # self.current_c, = self.ax1.plot([], [], label='Phase C')
        self.voltage_abc_bus11, = self.ax3.plot([], [], label='bus 11')
        self.voltage_abc_bus10, = self.ax3.plot([], [], label='bus 10')

        # Add legends and tight layout
        self.ax1.legend(loc=1)
        self.ax2.legend(loc=1)
        self.ax3.legend(loc=1)
        self.fig.tight_layout()

        # Adjust plot to leave some space for the title
        self.fig.subplots_adjust(top=0.88)

    def update(self, master):
        """Visualize simulation progress"""
        # Find current index
        index = len(master.feeder_result[0]['IA'])
        x = numpy.array(master.times[0:index]) / 60

        # Update plot values
        self.current_a_bus11.set_xdata(x)
        self.current_a_bus11.set_ydata(master.feeder_result[1]['IB'])
        self.current_a_bus10.set_xdata(x)
        self.current_a_bus10.set_ydata(master.feeder_result[0]['IB'])
        self.voltage_abc_bus11.set_xdata(x)
        # Replaced Bus10_VA by the reference value
        # self.voltage_abc_bus10.set_ydata(master.transmission_result['Bus10_VA'])
        self.voltage_abc_bus11.set_ydata([2672] * len(x))
        self.voltage_abc_bus10.set_xdata(x)
        # Replaced Bus11_VA by the reference value
        # self.voltage_abc_bus10.set_ydata(master.transmission_result['Bus10_VA'])
        self.voltage_abc_bus10.set_ydata([7270] * len(x))

        # Redefine graph scale
        self.ax1.relim()
        self.ax1.autoscale_view(True,True,True)
        self.ax2.relim()
        self.ax2.autoscale_view(True,True,True)
        self.ax3.relim()
        self.ax3.autoscale_view(True,True,True)

        # Update plot
        self.fig.canvas.draw()
        plt.pause(0.01)
