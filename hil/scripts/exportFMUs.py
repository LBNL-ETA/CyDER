# This script uses JModelica to export
# models and tools as FMUs.
import sys
import os
import subprocess as sp
from datetime import datetime
################################################################################
# Check the number of arguments
print ("==========Ready to export the Inverter Controls FMU")
nargs=len(sys.argv)
if (nargs < 5):
    s="The number of arguments={!s} is incorrect".format(nargs)
    raise ValueError(s)
# Get the path to JModelica
tool="jmodelica"
path_jmodelica=sys.argv[1]
if not (os.path.isdir(path_jmodelica)):
    s="Path to JModelica installation folder is set to {!s} which does not exist.".format(path_jmodelica)
    raise ValueError(s)
path_jmodelica_env= os.path.join(path_jmodelica, "setenv.bat")
command="call " + path_jmodelica_env
# Execute this command to set the envirnment variable for JModelica
retStr=os.system(command)
# Get the library path and class name of volt/var models
path_to_controls_lib=sys.argv[2]
if not (os.path.isdir(path_to_controls_lib)):
    s="Path to controls library is set to {!s} which does not exist.".format(path_to_controls_lib)
    raise ValueError(s)
name_controls_class=sys.argv[3]
tstart=datetime.now()
retStr=sp.check_output(["python", "voltvar_control.py",
    path_to_controls_lib, name_controls_class])
tend=datetime.now()
print ("==========Export of Inverter Controls FMU was successful.")
print ("==========Exporting Inverter Controls FMU in {!s}s.".format((tend-tstart).seconds))
# Get the path to SimulatorToFMU for remanining FMUs
path_simulatortofmu=sys.argv[4]
if not (os.path.isdir(path_simulatortofmu)):
    s="Path to SimulatorToFMU is set to {!s} which does not exist.".format(path_simulatortofmu)
    raise ValueError(s)
path_simulatortofmu=os.path.join(path_simulatortofmu, "SimulatorToFMU.py")
################################################################################
print ("==========Ready to export the uPMU Sensor FMU")
print ("==========The uPMU Sensor FMU only works with Python27")
#"Z:\Ubuntu\proj\cyder_repo\git\hil\SimulatorModelDescription.xml"
path_to_upmu_inputfile=sys.argv[5]
if not (os.path.exists(path_to_upmu_inputfile)):
    s="Path to uPMU input file is set to {!s} which does not exist.".format(path_to_upmu_inputfile)
    raise ValueError(s)
#"Z:\Ubuntu\proj\cyder_repo\git\hil\simulator_wrapper.py"
path_to_upmu_script=sys.argv[6]
if not (os.path.exists(path_to_upmu_script)):
    s="Path to uPMU script file is set to {!s} which does not exist.".format(path_to_upmu_script)
    raise ValueError(s)
# Export uPMU as an FMU
tstart=datetime.now()
retStr=sp.check_output(["python", path_simulatortofmu, "-i",
    path_to_upmu_inputfile, "-s", path_to_upmu_script, "-t", tool, "-pt", path_jmodelica])
tend=datetime.now()
print ("==========Export of the uPMU Sensor FMU was successful")
print ("==========Exporting uPMU FMU in {!s}s.".format((tend-tstart).seconds))
#python master.py "C:\JModelica.org-2.0" "Z:\Ubuntu\proj\cyder_repo\git\hil"
# "CyDER.HIL.Examples.Validate_VoltVarControl" "Z:\Ubuntu\proj\simulatortofmu\SimulatorToFMU\simulatortofmu\parser"
# "Z:\Ubuntu\proj\cyder_repo\git\hil\SimulatorModelDescription.xml" "Z:\Ubuntu\proj\cyder_repo\git\hil\simulator_wrapper.py"
################################################################################
print ("==========Ready to export the OPAL-RT FMU")
print ("==========The OPAL-RT FMU only works with Python27")
#"xxx\SimulatorModelDescription.xml"
path_to_opalrt_inputfile=sys.argv[7]
if not (os.path.exists(path_to_opalrt_inputfile)):
    s="Path to OPAL-RT input file is set to {!s} which does not exist.".format(path_to_opalrt_inputfile)
    raise ValueError(s)
#"xxx\simulator_wrapper.py"
path_to_opalrt_script_root=sys.argv[8]
path_to_opalrt_script=os.path.join(path_to_opalrt_script_root, "simulator_wrapper.py")
if not (os.path.exists(path_to_opalrt_script)):
    s="Path to OPAL-RT script file is set to {!s} which does not exist.".format(path_to_opalrt_script)
    raise ValueError(s)
#"xxx\.llp"
path_to_opalrt_configuration=sys.argv[9]
if not (os.path.exists(path_to_opalrt_configuration)):
    s="Path to OPAL-RT configuration file is set to {!s} which does not exist.".format(path_to_opalrt_configuration)
    raise ValueError(s)
tstart=datetime.now()
# Export OPAL-RT as an FMU
retStr=sp.check_output(["python", path_simulator_fmu, "-i",
    path_to_opalrt_inputfile, "-s", path_to_opalrt_script, "-t", tool, "-pt", path_jmodelica])
tend=datetime.now()
print ("==========Export of the OPAL-RT FMU was successful")
print ("==========Exporting OPAL-RT FMU in {!s}s.".format((tend-tstart).seconds))
# print ("==========Ready to export the CYMDIST FMU")
# print ("==========The uPMU Sensor FMU only works with Python34")
# #"Z:\Ubuntu\proj\simulatortofmu\SimulatorToFMU\simulatortofmu\parser"
# path_cymdisttofmu=sys.argv[3]
# path_cymdisttofmu=os.path.join(path_cymdisttofmu, "CYMDISTToFMU.py")
# #"Z:\Ubuntu\proj\cyder_repo\git\cosimulation\source\generate_fmu\fmu\cymdisttofmu\parser\utilities\CYMDISTModelDescription.xml"
# path_cymdist_inputfile=sys.argv[4]
#
# #"Z:\Ubuntu\proj\cyder_repo\git\cosimulation\source\generate_fmu\fmu\cymdisttofmu\parser\utilities"
# path_to_cymdist_script_root=sys.argv[5]
# path_to_cymdist_script=os.path.join (path_to_cymdist_script_root, "cymdist_wrapper.py")
# #target_script=os.path.join (path_to_script_root, "simulator_wrapper.py")
# #from shutil import copyfile
# #copyfile (path_to_script, target_script)
# #path_to_script=target_script
# tool="jmodelica"
#
# # Path to JModelica
# path_jmodelica=sys.argv[6]
#
# # Path to the configuration file
# # This is required for JModelica FMU
# # which does not allow to set the path
# # at runtime
# path_cymdist_configuration=sys.argv[7]
#
# #retStr=sp.check_output(["python", path_cymdisttofmu, "-i",
# #    path_cymdist_inputfile, "-s", path_to_cymdist_script, "-t", tool, "-pt", path_jmodelica])
# print ("==========Export of the CYMDIST FMU was successful")

#C:\Users\thierry\Desktop>python master.py "Z:\Ubuntu\proj\cyder_repo\git\hil" "C
#yDER.HIL.Examples.Validate_VoltVarControl" "Z:\Ubuntu\proj\simulatortofmu\Simula
#torToFMU\simulatortofmu\parser" "Z:\Ubuntu\proj\cyder_repo\git\cosimulation\sour
#ce\generate_fmu\fmu\cymdisttofmu\parser\utilities\CYMDISTModelDescription.xml" "
#Z:\Ubuntu\proj\cyder_repo\git\cosimulation\source\generate_fmu\fmu\cymdisttofmu\
#parser\utilities" "C:\JModelica.org-2.0" "xxx" "Z:\Ubuntu\proj\cyder_repo\git\hi
#l\SimulatorModelDescription.xml" "Z:\Ubuntu\proj\cyder_repo\git\hil\simulator_wr
#apper.py"


#print ("==========Export of the uPMU FMU was successful")
