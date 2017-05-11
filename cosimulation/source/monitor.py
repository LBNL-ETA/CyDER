from __future__ import division
import matplotlib
from matplotlib.ticker import FormatStrFormatter
import matplotlib.pyplot as plt
plt.switch_backend('Qt4Agg')
seaborn.set_style("whitegrid")
seaborn.despine()
plt.close()


class Monitor(object):
    """Monitor simulation progress"""

    def __init__(self):
        pass

    def initialize(self, master):
        """Initialize graphs"""
        # Interactive mode on
        plt.ion()

        # Create the plot
        fig = plt.figure()
        ax1 = fig.add_subplot(211)
        ax2 = fig.add_subplot(212)
        ax1.set_ylabel('Feeder voltages\n(GridDyn) [V]')
        ax2.set_ylabel('Feeder currents\n(cymDist) [A]')
        ax2.yaxis.set_major_formatter(FormatStrFormatter('%.3f'))
        ax2.set_xlabel('Time (minutes)')

        # Create lines
        current_a, = ax1.plot(simTim, CYMDIST_IA, label='Phase A')
        current_b, = ax1.plot(simTim, CYMDIST_IB, label='Phase B')
        current_c, = ax1.plot(simTim, CYMDIST_IC, label='Phase C')
        voltage_abc, = ax2.plot(simTim, GRIDDYN_VA, label='Balanced accross phases')

        # Add legends and tight layout
        ax1.legend(loc=1)
        ax2.legend(loc=1)
        fig.tight_layout()


    def visualize(self, master):
        """Visualize simulation progress"""


CYMDIST_IA.append(cymdist.get_real(cymdist.get_variable_valueref('IA'))[0])
CYMDIST_IB.append(cymdist.get_real(cymdist.get_variable_valueref('IB'))[0])
CYMDIST_IC.append(cymdist.get_real(cymdist.get_variable_valueref('IC'))[0])
GRIDDYN_VA.append(griddyn.get_real(griddyn.get_variable_valueref('Bus11_VA'))[0])
GRIDDYN_VB.append(griddyn.get_real(griddyn.get_variable_valueref('Bus11_VB'))[0])
GRIDDYN_VC.append(griddyn.get_real(griddyn.get_variable_valueref('Bus11_VC'))[0])
simTim.append(tim / 60)

# for name in cymdist_column_names:
#     df.loc[simTim[-1], name] = cymdist.get_real(cymdist.get_variable_valueref(name))[0]
#
# for name in griddyn_column_names:
#     df.loc[simTim[-1], name] = griddyn.get_real(griddyn.get_variable_valueref(name))[0]

line1A.set_xdata(simTim)
line1A.set_ydata(CYMDIST_IA)
line1B.set_xdata(simTim)
line1B.set_ydata(CYMDIST_IB)
line1C.set_xdata(simTim)
line1C.set_ydata(CYMDIST_IC)

line2A.set_xdata(simTim)
line2A.set_ydata(GRIDDYN_VA)
line2B.set_xdata(simTim)
line2B.set_ydata(GRIDDYN_VB)
line2C.set_xdata(simTim)
line2C.set_ydata(GRIDDYN_VC)

ax1.relim()
ax1.autoscale_view(True,True,True)
ax2.relim()
ax2.autoscale_view(True,True,True)
fig.canvas.draw()
plt.pause(0.01)
