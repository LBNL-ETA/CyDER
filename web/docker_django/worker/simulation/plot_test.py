import time
import pdb
import matplotlib.pyplot as plt
plt.switch_backend('Qt4Agg')
import numpy as np
import seaborn
seaborn.set_style("whitegrid")
seaborn.despine()
plt.close()

# Plot reference
nb_simulation = 30
sec_per_sim = 5
rad = np.linspace(0, 2*np.pi, num=nb_simulation)
x = np.linspace(0, len(rad) * sec_per_sim, len(rad)) / 60
y = [value if value < 1.3 else 1.3 for value in np.sin(rad) / 2 + 1]
y2 = np.array([value for value in np.sin(np.flipud(rad)) + 1])
y2 = np.array([value if value < 1 else 1 for value in y2])
noise = np.random.normal(0, 0.05, len(y2))
y2 += noise
y2 = np.array([value if value > 0 else 0 for value in y2])
y2 = np.array([value if value < 1 else 1 for value in y2])



# Create the vectors
times = np.linspace(0, len(rad) * sec_per_sim, len(rad)) / 60
currents = np.random.normal(0, 0.1, len(times))
voltages = np.random.normal(0, 0.1, len(times))

# Interactive mode on
plt.ion()

# Create the plot
fig = plt.figure()
ax = fig.add_subplot(311)
ax1 = fig.add_subplot(312)
ax2 = fig.add_subplot(313)
ax.set_ylabel('Coefficient')
ax1.set_ylabel('Currents [A]')
ax2.set_ylabel('Voltages [V]')
ax2.set_xlabel('Time (minutes)')
line, = ax.plot(x, y, 'b-')
line, = ax.plot(x, y2, 'r-')
line1, = ax1.plot([], [], 'b-')
line2, = ax2.plot([], [], 'r-')

for index, t in enumerate(times):
    time.sleep(1)
    line1.set_xdata(times[:index + 1])
    line1.set_ydata(currents[:index + 1])
    line2.set_xdata(times[:index + 1])
    line2.set_ydata(voltages[:index + 1])
    ax1.relim()
    ax1.autoscale_view(True,True,True)
    ax2.relim()
    ax2.autoscale_view(True,True,True)
    fig.canvas.draw()
    plt.pause(0.01)
