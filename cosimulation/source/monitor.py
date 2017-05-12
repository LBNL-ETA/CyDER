from __future__ import division
import matplotlib
from matplotlib.ticker import FormatStrFormatter
import matplotlib.pyplot as plt
import seaborn
import numpy
plt.switch_backend('Qt4Agg')
seaborn.set_style("whitegrid")
seaborn.despine()
plt.close()


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
