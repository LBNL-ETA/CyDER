#######################################################
# Script with unit tests for CYMDISTToFMU
#
# TSNouidui@lbl.gov                          2016-09-06
#######################################################
import unittest
import os
import sys
import platform
import subprocess
import shutil
from datetime import datetime

# Appending parser_path to the system path os required to be able
# to find the CYMDISTToFMU model from this directory
script_path = os.path.dirname(os.path.realpath(__file__))
parser_path = os.path.abspath(os.path.join(script_path, '..', 'parser'))
sys.path.append(parser_path)

import CYMDISTToFMU as cymdist

XSD_SCHEMA = 'CYMDISTModelDescription.xsd'
NEEDSEXECUTIONTOOL = 'needsExecutionTool'
MODELDESCRIPTION = 'modelDescription.xml'
CYMDISTModelicaTemplate_MO = 'CYMDISTModelicaTemplate.mo'
CYMDISTModelicaTemplate_Dymola_MOS = 'CYMDISTModelicaTemplate_Dymola.mos'
CYMDISTModelicaTemplate_JModelica_MOS = 'CYMDISTModelicaTemplate_JModelica.py'
CYMDISTModelicaTemplate_OpenModelica_MOS = 'CYMDISTModelicaTemplate_OpenModelica.mos'
XML_MODELDESCRIPTION = 'CYMDISTModelDescription.xml'
# Get the path to the templates files
script_path = os.path.dirname(os.path.realpath(__file__))
utilities_path = os.path.join(script_path, '..', 'parser', 'utilities')
PYTHON_SCRIPT_PATH = os.path.join(utilities_path, 'cymdist_wrapper.py')
MO_TEMPLATE_PATH = os.path.join(utilities_path, CYMDISTModelicaTemplate_MO)
MOS_TEMPLATE_PATH_DYMOLA = os.path.join(
    utilities_path, CYMDISTModelicaTemplate_Dymola_MOS)
MOS_TEMPLATE_PATH_JMODELICA = os.path.join(
    utilities_path, CYMDISTModelicaTemplate_JModelica_MOS)
MOS_TEMPLATE_PATH_OPENMODELICA = os.path.join(
    utilities_path, CYMDISTModelicaTemplate_OpenModelica_MOS)
XSD_FILE_PATH = os.path.join(utilities_path, XSD_SCHEMA)
XML_INPUT_FILE = os.path.join(utilities_path, XML_MODELDESCRIPTION)
CYMDISTToFMU_LIB_PATH = os.path.join(
    script_path, '..', 'parser', 'libraries', 'modelica')
python_scripts_path = [PYTHON_SCRIPT_PATH]

if(platform.system().lower() == 'windows'):
    python_scripts_path = [item.replace('\\', '\\\\') for item in [
        PYTHON_SCRIPT_PATH]]

CYMDIST_T = cymdist.CYMDISTToFMU('con_path',
                                       XML_INPUT_FILE,
                                       CYMDISTToFMU_LIB_PATH,
                                       MO_TEMPLATE_PATH,
                                       MOS_TEMPLATE_PATH_DYMOLA,
                                       XSD_FILE_PATH,
                                       '34',
                                       python_scripts_path,
                                       '2.0',
                                       'me',
                                       'dymola',
                                       None,
                                       None,
                                       'false')





class Tester(unittest.TestCase):
    '''
    Class that runs all regression tests.

    '''

    def find_executable(self, tool):

        '''
        Function for checking if Dymola, JModelica, or OpenModelica is installed.

        '''

        if tool == 'jmodelica' and platform.system().lower() == "windows":
            tool = 'pylab'
        if tool == 'jmodelica' and platform.system().lower() == "linux":
            tool = 'jm_python.sh'

        if tool == 'openmodelica' and platform.system().lower() == "windows":
            tool = 'omc'

        cmd = "where" if platform.system() == "Windows" else "which"
        try:
            return subprocess.call([cmd, tool])
        except:
            print ("No executable for tool={!s}".format(tool))
            return 1

    def run_cymdist (self, tool):

        '''
        Function for running FMUs exported from Dymola, JModelica, and OpenModelica with PyFMI.

        '''

        try:
            from pyfmi import load_fmu
        except BaseException:
            print ('PyFMI not installed. Test will not be be run.')
            return
        if (tool=='openmodelica' and platform.system().lower() == 'linux'):
                print ('tool={!s} is not supported on Linux'.format(tool))
                return

        else:
        # Export FMUs which are needed to run the cases.
            if tool == 'openmodelica':
                modPat = 'OPENMODELICALIBRARY'
                mosT = MOS_TEMPLATE_PATH_OPENMODELICA
            elif tool == 'dymola':
                modPat = 'MODELICAPATH'
                mosT = MOS_TEMPLATE_PATH_DYMOLA
            elif tool == 'jmodelica':
                # Unset environment variable
                if (os.environ.get('MODELICAPATH') is not None):
                    del os.environ['MODELICAPATH']
                modPat = None
                mosT = MOS_TEMPLATE_PATH_JMODELICA
            for version in ['2']:
                if (tool == 'openmodelica' or tool == 'jmodelica'):
                    version = str(float(version))
                for api in ['me']:
                    if (tool == 'openmodelica' and version == '1.0' and api == 'cs'):
                        print (
                            'tool={!s} with FMI version={!s} and FMI API={!s} is not supported.'.format(
                                tool, version, api))
                        continue
                    for cs_xml in ['true']:
                        if (version == '1'):
                            continue
                        CYMDIST_Test = cymdist.CYMDISTToFMU(
                            'con_path',
                            XML_INPUT_FILE,
                            CYMDISTToFMU_LIB_PATH,
                            MO_TEMPLATE_PATH,
                            mosT,
                            XSD_FILE_PATH,
                            '34',
                            python_scripts_path,
                            version,
                            api,
                            tool,
                            None,
                            modPat,
                            cs_xml)

                        print (
                            'Export the cymdist with tool={!s}, FMI version={!s}, FMI API={!s}'.format(
                                tool, version, api))
                        start = datetime.now()
                        # CYMDIST_Test.print_mo()
                        # CYMDIST_Test.generate_fmu()
                        # CYMDIST_Test.clean_temporary()
                        # CYMDIST_Test.rewrite_fmu()
                        end = datetime.now()
                        print(
                            'Export CYMDIST as an FMU in {!s} seconds.'.format(
                                (end - start).total_seconds()))

                        fmu_path = os.path.join(
                        script_path, '..', 'fmus', tool, platform.system().lower())
                        print(
                            'Copy CYMDIST.fmu to {!s}.'.format(fmu_path))
                        shutil.copy2('CYMDIST.fmu', fmu_path)

        fmu_path = os.path.join(
                script_path, '..', 'fmus', tool, platform.system().lower(), 'CYMDIST.fmu')
        # Parameters which will be arguments of the function
        start_time = 0.0
        stop_time = 0.1

        print ('Starting the simulation with {!s}'.format(tool))
        start = datetime.now()

        cymdist_input_valref = []
        cymdist_output_valref = []

        sim_mod = load_fmu(fmu_path, log_level=7)
        sim_mod.setup_experiment(
            start_time=start_time, stop_time=stop_time)

        cymdist_con_val_str=os.path.abspath('Z:\\thierry\\proj\\cyder_repo\\NO_SHARING\\CYMDIST\\config.json')
        if sys.version_info.major>2:
            cymdist_con_val_str=bytes(cymdist_con_val_str,'utf-8')
        cymdist_con_val_ref=sim_mod.get_variable_valueref('_configurationFileName')

        # Define the inputs
        cymdist_input_names = ['VMAG_A', 'VMAG_B', 'VMAG_C', 'VANG_A', 'VANG_B', 'VANG_C']
        cymdist_input_values = [2520, 2520, 2520, 0, -120, 120]
        cymdist_output_names = ['IA', 'IAngleA', 'IB', 'IAngleB', 'IC', 'IAngleC']

        # Get the value references of cymdist inputs
        for elem in cymdist_input_names:
            cymdist_input_valref.append(
                sim_mod.get_variable_valueref(elem))

        # Get the value references of cymdist outputs
        for elem in cymdist_output_names:
            cymdist_output_valref.append(
                sim_mod.get_variable_valueref(elem))

        # Set the flag to save the results
        sim_mod.set('_saveToFile', 0)

        if not (tool=="jmodelica"):
            sim_mod.set_string([cymdist_con_val_ref], [cymdist_con_val_str])

        # Initialize the FMUs
        sim_mod.initialize()

        # Call event update prior to entering continuous mode.
        sim_mod.event_update()

        # Enter continuous time mode
        sim_mod.enter_continuous_time_mode()

        sim_mod.set_real(cymdist_input_valref, cymdist_input_values)

        end = datetime.now()

        print(
            'Ran a single CYMDIST simulation with {!s} FMU={!s} in {!s} seconds.'.format(
                tool, fmu_path, (end - start).total_seconds()))
        if not (tool=='openmodelica'):
            #print(sim_mod.get_real(cymdist_output_valref))
            # PyFMI fails to get the output of an OpenModelica FMU
            if(abs(sum(sim_mod.get_real(cymdist_output_valref))-618.57)>1e-3):
                raise ValueError('Values are not matching.')
        # Terminate FMUs
        sim_mod.terminate()

    def test_check_duplicates(self):
        '''
        Test the function check_duplicates().

        '''

        # Array does not contain duplicates variables.
        cymdist.check_duplicates(['x1', 'x2', 'x3', 'x4'])

        # Array contain duplicates variables.
        with self.assertRaises(AssertionError):
            cymdist.check_duplicates(['x1', 'x1', 'x3', 'x4'])

    def test_sanitize_name(self):
        '''
        Test the function sanitize_name().

        '''

        # Testing name conversions.
        name = cymdist.sanitize_name('test+name')
        self.assertEqual(name, 'test_name', 'Names are not matching.')

        name = cymdist.sanitize_name('0test+*.name')
        self.assertEqual(name, 'f_0test___name', 'Names are not matching.')

    def test_xml_validator(self):
        '''
        Test the function xml_validator().

        '''

        # Testing validation of xml file
        CYMDIST_T.xml_validator()

    def test_xml_parser(self):
        '''
        Test the function xml_validator().

        '''

        # Testing validation of xml file
        CYMDIST_T.xml_parser()

    def test_print_mo(self):
        '''
        Test the function print_mo().

        '''

        # Testing function to print Modelica model.
        CYMDIST_T.print_mo()

    def test_cymdist_to_fmu(self):
        '''
        Test the export of an FMU with various options.

        '''

        for tool in  ['dymola', 'jmodelica', 'openmodelica']:
            retVal=self.find_executable(tool)
            if ((retVal is not None) and retVal!=1):
                print("======tool={!s} was found. Unit Test will be run".format(tool))
            else:
                continue

            if (platform.system().lower() == 'linux' and tool == 'openmodelica'):
                print ('tool={!s} is not supported on Linux.'.format(tool))
                continue
            if tool == 'openmodelica':
                modPat = 'OPENMODELICALIBRARY'
                mosT = MOS_TEMPLATE_PATH_OPENMODELICA
            elif tool == 'dymola':
                modPat = 'MODELICAPATH'
                mosT = MOS_TEMPLATE_PATH_DYMOLA
            elif tool == 'jmodelica':
                if (os.environ.get('MODELICAPATH') is not None):
                    del os.environ['MODELICAPATH']
                modPat = None
                mosT = MOS_TEMPLATE_PATH_JMODELICA
            for version in ['1', '2']:
                if (tool == 'openmodelica' or tool == 'jmodelica'):
                    version = str(float(version))
                for api in ['me', 'cs']:
                    if (tool == 'openmodelica' and version == '1.0' and api == 'cs'):
                        print (
                            'tool={!s} with FMI version={!s} and FMI API={!s} is not supported.'.format(
                                tool, version, api))
                        continue
                    for cs_xml in ['true']:
                        if (version == '1'):
                            continue
                        CYMDIST_Test = cymdist.CYMDISTToFMU(
                            'con_path',
                            XML_INPUT_FILE,
                            CYMDISTToFMU_LIB_PATH,
                            MO_TEMPLATE_PATH,
                            mosT,
                            XSD_FILE_PATH,
                            '34',
                            python_scripts_path,
                            version,
                            api,
                            tool,
                            None,
                            modPat,
                            cs_xml)

                        print (
                            'Export the cymdist with tool={!s}, FMI version={!s}, FMI API={!s}'.format(
                                tool, version, api))
                        start = datetime.now()
                        CYMDIST_Test.print_mo()
                        CYMDIST_Test.generate_fmu()
                        CYMDIST_Test.clean_temporary()
                        CYMDIST_Test.rewrite_fmu()
                        end = datetime.now()
                        print(
                            'Export CYMDIST as an FMU in {!s} seconds.'.format(
                                (end - start).total_seconds()))

    def test_updates_fmu(self):
        '''
        Test the export and updates of FMUs.

        '''

        for tool in  ['dymola', 'jmodelica', 'openmodelica']:
            retVal=self.find_executable(tool)
            if ((retVal is not None) and retVal!=1):
                print("======tool={!s} was found. Unit Test will be run".format(tool))
            else:
                continue

            if (platform.system().lower() == 'linux' and tool == 'openmodelica'):
                print ('tool={!s} is not supported on Linux.'.format(tool))
                continue
            if tool == 'openmodelica':
                modPat = 'OPENMODELICALIBRARY'
                mosT = MOS_TEMPLATE_PATH_OPENMODELICA
            elif tool == 'dymola':
                modPat = 'MODELICAPATH'
                mosT = MOS_TEMPLATE_PATH_DYMOLA
            elif tool == 'jmodelica':
                if (os.environ.get('MODELICAPATH') is not None):
                    del os.environ['MODELICAPATH']
                modPat = None
                mosT = MOS_TEMPLATE_PATH_JMODELICA
            for version in ['2']:
                if (tool == 'openmodelica' or tool == 'jmodelica'):
                    version = str(float(version))
                for api in ['me']:
                    if (tool == 'openmodelica' and version == '1.0' and api == 'cs'):
                        print (
                            'tool={!s} with FMI version={!s} and FMI API={!s} is not supported.'.format(
                                tool, version, api))
                        continue
                    for cs_xml in ['true']:
                        if (version == '1'):
                            continue
                        CYMDIST_Test = cymdist.CYMDISTToFMU(
                            'con_path',
                            XML_INPUT_FILE,
                            CYMDISTToFMU_LIB_PATH,
                            MO_TEMPLATE_PATH,
                            mosT,
                            XSD_FILE_PATH,
                            '34',
                            python_scripts_path,
                            version,
                            api,
                            tool,
                            None,
                            modPat,
                            cs_xml)

                        print (
                            'Export the cymdist with tool={!s}, FMI version={!s}, FMI API={!s}'.format(
                                tool, version, api))
                        start = datetime.now()
                        CYMDIST_Test.print_mo()
                        CYMDIST_Test.generate_fmu()
                        CYMDIST_Test.clean_temporary()
                        CYMDIST_Test.rewrite_fmu()
                        end = datetime.now()
                        print(
                            'Export CYMDIST as an FMU in {!s} seconds.'.format(
                                (end - start).total_seconds()))
                        fmu_path = os.path.join(
                        script_path, '..', 'fmus', tool, platform.system().lower())
                        print(
                            'Copy CYMDIST.fmu to {!s}.'.format(fmu_path))
                        shutil.copy2('CYMDIST.fmu', fmu_path)

    def test_run_cymdist_all(self):
        '''
        Test the execution of one CYMDIST FMU.

        '''

        # Export FMUs which are needed to run the cases.
        for tool in  ['dymola', 'jmodelica', 'openmodelica']:
            retVal=self.find_executable(tool)
            if ((retVal is not None) and retVal!=1):
                print("======tool={!s} was found. Unit Test will be run.".format(tool))
                print('=======The unit test will be run for tool={!s}.'.format(tool))
                self.run_cymdist (tool)
            else:
                continue

    def test_run_cymdist_dymola(self):
        '''
        Test the execution of one CYMDIST FMU.

        '''

        retVal=self.find_executable('dymola')
        if ((retVal is not None) and retVal!=1):
            print("======tool=dymola was found. Unit Test will be run.")
            print('=======The unit test will be run for Dymola.')
            print('=======Make sure that Dymola is on the System Path otherwise the simulation will fail.')
            # Run the cases
            self.run_cymdist ('dymola')
        else:
            return

    def test_run_cymdist_jmodelica(self):
        '''
        Test the execution of one CYMDIST FMU.

        '''

        retVal=self.find_executable('jmodelica')
        if ((retVal is not None) and retVal!=1):
            print("======tool=jmodelica was found. Unit Test will be run.")
            print('=======The unit test will be run for JModelica.')
            print('=======Make sure that JModelica is on the System Path otherwise the simulation will fail.')
            # Run the cases
            self.run_cymdist ('jmodelica')
        else:
            return

    def test_run_cymdist_openmodelica(self):
        '''
        Test the execution of one CYMDIST FMU.

        '''

        retVal=self.find_executable('openmodelica')
        if ((retVal is not None) and retVal!=1):
            print("======tool=openmodelica was found. Unit Test will be run.")
            print('=======The unit test will be run for OpenModelica.')
            print('=======Make sure that OpenModelica is on the System Path otherwise the simulation will fail.')
            # Run the cases
            self.run_cymdist ('openmodelica')
        else:
            return

if __name__ == "__main__":
        # Check command line options
    if (platform.system().lower() in ['windows']):
        unittest.main()
    else:
        print('=========CYMDISTToFMU is only supported Windows.')
