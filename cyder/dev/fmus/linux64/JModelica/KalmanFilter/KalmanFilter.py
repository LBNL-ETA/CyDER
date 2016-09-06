# This script is used to test the export of
# a Modelica block that wraps python as an FMU.
# The path to the Modelica Buildings Library needs to be specified.
# Note that the script can successfully export the FMU with a number of warnings 
# (e.g. String arguments in functions are only partially supported
)
# Reimporting the FMU in Dymola 2017 will fail with following error message:
# Note that if the FMU is exported using Dymola and the environment variables
# PYTHONPATH are correctly set, then reimporting the FMU in Dymola 2017 will work.

# dymosim started
# ... "dsin.txt" loading (dymosim input file)
# Buildings_Utilities_IO_Python27_Examples_KalmanFilter_fmu:         <JMIRuntime><value name="build_date">"Jun 27 2016"</value> <value name="build_time">"12:13:41"</value></JMIRuntime>
# Buildings_Utilities_IO_Python27_Examples_KalmanFilter_fmu:         <ModelicaError category="warning"><value name="msg">"Failed to load ""KalmanFilter"".&##10;This may occur if you did # not set the PYTHONPATH environment variable&##10;or if the Python module contains a syntax error.&##10;The error message is ""'No module named KalmanFilter'"""</value></ModelicaError>
# Buildings_Utilities_IO_Python27_Examples_KalmanFilter_fmu:         Evaluation of model equations during event iteration failed.
# The following error was detected at time: 0
# EventUpdate failed
# The stack of functions is:
# Buildings_Utilities_IO_Python27_Examples_KalmanFilter_fmu.fmi_Functions.fmiUpdateDiscreteStates
# Buildings_Utilities_IO_Python27_Examples_KalmanFilter_fmu.fmi_Functions.fmiUpdateDiscreteStates(
# buildings_Utilities_IO_Python27_Examples_KalmanFilter_fmu.fmi)
# Error: Failed to start model.
# One reason might be the warning which says that String arguments in functions are only partially supported

from pymodelica import compile_fmu

# Define the path to the Buildings library to use
Buildings_Lib_Path='/home/thierry/vmWareLinux/proj/buildings_library/models/modelica/git/buildings/modelica-buildings'

# Generate an FMU which implements FMI 2.0.
fmu = compile_fmu('Buildings.Utilities.IO.Python27.Examples.KalmanFilter', version='2.0', compiler_options = {'extra_lib_dirs':Buildings_Lib_Path})

