# This script uses JModelica to export
# models and tools as FMUs.
# If Dymola is used as an export tool
# It must be added to the system path so it
# can be started from the command line with dymola
##################################################

import sys
import os
from pyfmi import load_fmu
from pyfmi.master import Master
from datetime import datetime
import matplotlib.pyplot as plt

"""
Master algorithm for exporting the FMUs
The assumption is that all FMUs are for co-simulation
so we can use the master algorithm of Modelon for running them
"""

print("=============Loading FMUs")
# Load the sensor FMU
sensor=load_fmu("uPMU.fmu")
# Load the controls FMU
controls=load_fmu("CyDER_HIL_Controls_voltvar.fmu")

# Load the OPAL-RT FMU

# Load the inverter API FMU

# Create the list of FMUs
models=[sensor, controls]

# Create the connection list between the FMUs
connections=[(sensor, "y_out", controls, "v_pu"),
             (controls, "q_control", sensor, "_dummy")]

# Pass the models to the master algorithm
coupled_simulation=Master(models, connections)
opts=coupled_simulation.simulate_options()
# Specify the time step
opts["step_size"]=0.01
# Option for stabilizing the simulation
# opts["linear_correction"]=False

print("=============Simulating FMUs")
res=coupled_simulation.simulate(options=opts)

# Get the simulation results
sensor_time=res[sensor]["time"]
sensor_out=res[sensor]["y_out"]

# Plot the simulation results
plt.plot(sensor_time,sensor_out)
plt.ylabel("Sensor output")
plt.show()
