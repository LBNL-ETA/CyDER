# This script uses JModelica to export
# models and tools as FMUs.
# If Dymola is used as an export tool
# It must be added to the system path so it
# can be started from the command line with dymola
##################################################

"""
The Python script requires following arguments:
1. Export tool= dymola or jModelica
2. Export tool path
2. Path to the controls library
3. Controls class name to be exported
4. Path to simulatortofmu/parser folder
5. Path to xml input file for upmu
6. Path to upmu script file
7. Path to xml input file for opal-rt
8  Path to script file for opal-rt
9. Path to configuration file for opal-rt
fixme: A number of input variables of the
volt-var controller need to be changed to
parameters as they do not change during simulation.

C:\ProgramData\Anaconda2\python.exe exportFMUs.py "jmodelica" "C:\JModelica.org-2.0" "C:\Users\emma\Documents\GitHub\CyDER\hil\controls\CyDER.mo" "CyDER.HIL.Controls.voltVar2" "C:\Users\emma\Documents\GitHub\SimulatorToFMU\simulatortofmu\parser" "C:\Users\emma\Documents\GitHub\CyDER\hil\sensors\uPMU.xml.ignore" "C:\Users\emma\Documents\GitHub\CyDER\hil\sensors\uPMU_wrapper.py" "C:\Users\emma\Documents\GitHub\CyDER\hil\realtime\models\BU0001_timeserie_pv\opalrt.xml" "C:\Users\emma\Documents\GitHub\CyDER\hil\realtime\scripts\opalrt_wrapper.py" "C:\Users\emma\Documents\GitHub\CyDER\hil\realtime\models\BU0001_timeserie_pv\lbnl_test1.llp"
#python exportFMUs.py "dymola" "C:\JModelica.org-2.0" "C:\Users\emma\Documents\GitHub\CyDER\hil\controls\CyDER.mo" "CyDER.HIL.Controls.voltVar2" "C:\Users\emma\Documents\GitHub\SimulatorToFMU\simulatortofmu\parser" "C:\Users\emma\Documents\GitHub\CyDER\hil\sensors\uPMU.xml" "C:\Users\emma\Documents\GitHub\CyDER\hil\realtime\upmu_wrapper.py"

"""
import sys
import os
import subprocess as sp
from datetime import datetime
from jinja2 import Template
#script_path = os.path.dirname(os.path.realpath(__file__))
#controls_lib_base_path = os.path.join("..", "controls")
api="me"
MOS_Template="""
openModel("{{path_lib}}");
Advanced.FMI.xmlIgnoreProtected=true;
Advanced.AllowStringParametersForFMU=true;
translateModelFMU(
  modelToOpen="{{model_name}}",
  storeResult=false,
  modelName="",
  fmiVersion="2",
  fmiType="""+api+""",
  includeSource=false);
Advanced.FMI.xmlIgnoreProtected=false;
Advanced.AllowStringParametersForFMU=false;
exit();
"""
################################################################################
# Check the number of arguments
print ("==========Ready to export the Inverter Controls FMU")
nargs=len(sys.argv)
if (nargs < 7):
    s="The number of arguments={!s} is incorrect.".format(nargs)
    raise ValueError(s)
# Get the export tool to be used
# Dymola and JModelica are supported
tool=sys.argv[1]
if tool is None:
    s="Export tool is not defined. JModelica the default will be used."
    tool=="jmodelica"
    print(s)
if not (tool in ["dymola", "jmodelica"]):
    s="Dymola and JModelica are the only tools supported."
    raise ValueError(s)
# Get the path to the export tool
path_tool_exe=sys.argv[2]
# Handle jModelica case
if tool=="jmodelica":
    if not (os.path.isdir(path_tool_exe)):
        s="Path to JModelica installation folder is set to {!s} which does not exist.".format(path_tool_exe)
        raise ValueError(s)
    cmd_bat=os.path.join(path_tool_exe, "setenv.bat")
# Get the library path and class name of volt/var models
path_to_controls_lib=sys.argv[3]
# Get the base directory
controls_lib_base_path=os.path.dirname(path_to_controls_lib)
# Get the path to the controls library
name_controls_class=sys.argv[4]
tstart=datetime.now()
# Exporting controls as FMU using Dymola
if (tool=="dymola"):
    template = Template(MOS_Template)
    output_res = template.render(path_lib=path_to_controls_lib, model_name=name_controls_class)
    with open("controls.mos", mode="w") as mos_fil:
        mos_fil.write(output_res)
    mos_fil.close()
    retStr=sp.check_output(["dymola", "controls.mos"])
# Exporting controls as FMU using JModelica
voltvar_controls_py=os.path.join(controls_lib_base_path, "voltvar_control.py")
if(tool=="jmodelica"):
    command = cmd_bat + "&&" + "python " + voltvar_controls_py + " " + \
    path_to_controls_lib + " " + name_controls_class + " " + api
    retStr=sp.check_output(command, shell=True)
tend=datetime.now()
print ("==========Export of Inverter Controls FMU was successful.")
print ("==========Exporting Inverter Controls FMU in {!s}s.".format((tend-tstart).seconds))
# Get the path to SimulatorToFMU for remanining FMUs
path_simulatortofmu=sys.argv[5]
if not (os.path.isdir(path_simulatortofmu)):
    s="Path to SimulatorToFMU is set to {!s} which does not exist.".format(path_simulatortofmu)
    raise ValueError(s)
path_simulatortofmu=os.path.join(path_simulatortofmu, "SimulatorToFMU.py")
################################################################################
print ("==========Ready to export the uPMU Sensor FMU")
print ("==========The uPMU Sensor FMU only works with Python27")
# Get the path to the microPMU input file
path_to_upmu_inputfile=sys.argv[6]
if not (os.path.exists(path_to_upmu_inputfile)):
    s="Path to uPMU input file is set to {!s} which does not exist.".format(path_to_upmu_inputfile)
    raise ValueError(s)
# Get the path to the microPMU script file
path_to_upmu_script=sys.argv[7]
if not (os.path.exists(path_to_upmu_script)):
    s="Path to uPMU script file is set to {!s} which does not exist.".format(path_to_upmu_script)
    raise ValueError(s)
# Export uPMU as an FMU
tstart=datetime.now()
if (tool=="dymola"):
    retStr=sp.check_output(["python", path_simulatortofmu, "-i",
        path_to_upmu_inputfile, "-s", path_to_upmu_script, "-t", tool])
if(tool=="jmodelica"):
    retStr=sp.check_output(["python", path_simulatortofmu, "-i",
        path_to_upmu_inputfile, "-s", path_to_upmu_script, "-t", tool,
        "-a", api, "-pt", path_tool_exe])
tend=datetime.now()
print ("==========Export of the uPMU Sensor FMU was successful.")
print ("==========Exporting uPMU FMU in {!s}s.".format((tend-tstart).seconds))
################################################################################
print ("==========Ready to export the OPAL-RT FMU")
print ("==========The OPAL-RT FMU only works with Python27")
# Get the path to OPAL_RT input file
path_to_opalrt_inputfile=sys.argv[8]
if not (os.path.exists(path_to_opalrt_inputfile)):
    s="Path to OPAL-RT input file is set to {!s} which does not exist.".format(path_to_opalrt_inputfile)
    raise ValueError(s)
# Get the path to OPAL_RT script file
path_to_opalrt_script=sys.argv[9]
#path_to_opalrt_script=os.path.join(path_to_opalrt_script_root, "opalrt_wrapper.py")
if not (os.path.exists(path_to_opalrt_script)):
    s="Path to OPAL-RT script file is set to {!s} which does not exist.".format(path_to_opalrt_script)
    raise ValueError(s)
# Get the path to OPAL_RT configuration file
path_to_opalrt_configuration=sys.argv[10]
if not (os.path.exists(path_to_opalrt_configuration)):
    s="Path to OPAL-RT configuration file is set to {!s} which does not exist.".format(path_to_opalrt_configuration)
    raise ValueError(s)
tstart=datetime.now()
# Export OPAL-RT as an FMU
if(tool=="dymola"):
    retStr=sp.check_output(["python", path_simulatortofmu, "-i",
        path_to_opalrt_inputfile, "-s", path_to_opalrt_script, "-t", tool])
if(tool=="jmodelica"):
    retStr=sp.check_output(["python", path_simulatortofmu, "-i",
        path_to_opalrt_inputfile, "-s", path_to_opalrt_script, "-t", tool,
        "-a", api, "-pt", path_tool_exe, "-c", path_to_opalrt_configuration])
tend=datetime.now()
print ("==========Export of the OPAL-RT FMU was successful.")
print ("==========Exporting OPAL-RT FMU in {!s}s.".format((tend-tstart).seconds))

# print ("==========Ready to export the CYMDIST FMU")
# print ("==========The CYMDIST FMU only works with Python34")
# #"C:\Users\emma\Documents\GitHub\SimulatorToFMU\simulatortofmu\parser"
# path_cymdisttofmu=sys.argv[3]
# path_cymdisttofmu=os.path.join(path_cymdisttofmu, "CYMDISTToFMU.py")
# #"C:\Users\emma\Documents\GitHub\CyDER\git\cosimulation\source\generate_fmu\fmu\cymdisttofmu\parser\utilities\CYMDISTModelDescription.xml"
# path_cymdist_inputfile=sys.argv[4]
#
# #"C:\Users\emma\Documents\GitHub\CyDER\git\cosimulation\source\generate_fmu\fmu\cymdisttofmu\parser\utilities"
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


#print ("==========Export of the uPMU FMU was successful")
