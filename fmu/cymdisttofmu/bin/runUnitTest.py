#######################################################
# Script with unit tests for CyDER
#
# TSNouidui@lbl.gov                            2016-09-06
#######################################################
import unittest
import os
import sys
import platform
import subprocess
try:
    from pyfmi import load_fmu
except BaseException:
    pass
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
CYMDISTModelicaTemplate_OpenModelica_MOS = 'CYMDISTModelicaTemplate_OpenModelica.mos'
XML_MODELDESCRIPTION = 'CYMDISTModelDescription.xml'
# Get the path to the templates files
script_path = os.path.dirname(os.path.realpath(__file__))
utilities_path = os.path.join(script_path, '..', 'parser', 'utilities')
PYTHON_SCRIPT_PATH = os.path.join(utilities_path, 'cymdist_wrapper.py')
MO_TEMPLATE_PATH = os.path.join(utilities_path, CYMDISTModelicaTemplate_MO)
MOS_TEMPLATE_PATH_DYMOLA = os.path.join(
    utilities_path, CYMDISTModelicaTemplate_Dymola_MOS)
MOS_TEMPLATE_PATH_OPENMODELICA = os.path.join(
    utilities_path, CYMDISTModelicaTemplate_OpenModelica_MOS)
XSD_FILE_PATH = os.path.join(utilities_path, XSD_SCHEMA)
XML_INPUT_FILE = os.path.join(utilities_path, XML_MODELDESCRIPTION)
CYMDISTToFMU_LIB_PATH = os.path.join(
    script_path, '..', 'parser', 'libraries', 'modelica')
python_scripts_path = [PYTHON_SCRIPT_PATH]

if(platform.system().lower() == 'windows'):
    print ("Convert path to Python script={!s} to valid Windows path".format(
        PYTHON_SCRIPT_PATH))
    python_scripts_path = [item.replace('\\', '\\\\') for item in [
        PYTHON_SCRIPT_PATH]]
    print ("The valid Python script path is {!s}.".format(python_scripts_path))

CYMDIST_T = cymdist.CYMDISTToFMU('con_path',
                                       XML_INPUT_FILE,
                                       CYMDISTToFMU_LIB_PATH,
                                       MO_TEMPLATE_PATH,
                                       MOS_TEMPLATE_PATH_DYMOLA,
                                       XSD_FILE_PATH,
                                       '34',
                                       python_scripts_path,
                                       '2',
                                       'me',
                                       'dymola',
                                       'MODELICAPATH',
                                       'false')


class Tester(unittest.TestCase):
    '''
    Class that runs all regression tests.

    '''

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

    @unittest.skip("Export CYMDIST using multiple options.")
    def test_cymdist_to_fmu(self):
        '''
        Test the export of an FMU with various options.

        '''

        for tool in ['dymola', 'omc']:
            if (platform.system().lower() == 'linux' and tool == 'omc'):
                print ('tool={!s} is not supported on Linux.'.format(tool))
                continue
            if tool == 'omc':
                modPat = 'OPENMODELICALIBRARY'
                mosT = MOS_TEMPLATE_PATH_OPENMODELICA
            else:
                modPat = 'MODELICAPATH'
                mosT = MOS_TEMPLATE_PATH_DYMOLA
            for version in ['1', '2']:
                if (tool == 'omc'):
                    version = str(float(version))
                for api in ['me']:
                    if (tool == 'omc' and version == '1.0' and api == 'cs'):
                        print (
                            'tool={!s} with FMI version={!s} and FMI API={!s} is not supported.'.format(
                                tool, version, api))
                        continue
                    for cs_xml in ['false', 'true']:
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

    #@unittest.skip("Run the FMU using PyFMI")
    def test_run_cymdist_fmu(self):
        '''
        Test the execution of one CYMDIST FMU.

        '''

        if not(platform.system().lower() == 'windows'):
            print('CYMDISTToFMU is only supported on Windows.')
            return
        for tool in ['Dymola']:
            if platform.system().lower() == 'windows':
                fmu_path = os.path.join(
                    script_path, '..', 'fmus', tool, 'windows', 'CYMDIST.fmu')
            elif platform.system().lower() == 'linux':
                fmu_path = os.path.join(
                    script_path, '..', 'fmus', tool, 'linux', 'CYMDIST.fmu')
            if (tool == 'OpenModelica' and platform.system().lower() == 'linux'):
                continue
            # Parameters which will be arguments of the function
            start_time = 0.0
            stop_time = 5.0

<<<<<<< HEAD
            # Path to configuration file
            path_config=os.path.abspath("config.json")
            cymdist_con_val_str = bytes(path_config, 'utf-8')
=======
            print ('Starting the simulation')
            start = datetime.now()
            # Path to configuration file
            cymdistr_con_val_str = os.path.abspath('config.json')
            if sys.version_info.major > 2:
                cymdistr_con_val_str = bytes(cymdistr_con_val_str, 'utf-8')
>>>>>>> d8b4d8fb522fe127188530096584087869e9a7a0

            cymdist_input_valref=[]
            cymdist_output_valref=[]

            cymdist = load_fmu(fmu_path, log_level=7)
            cymdist.setup_experiment(start_time=start_time, stop_time=stop_time)

            # Define the inputs
            cymdist_input_names = ['VMAG_A', 'VMAG_B', 'VMAG_C', 'VANG_A', 'VANG_B', 'VANG_C']
            cymdist_input_values = [2520, 2520, 2520, 0, -120, 120]
            cymdist_output_names = ['IA', 'IB', 'IC', 'IAngleA', 'IAngleB', 'IAngleC']

            # Get the value references of cymdist inputs
            for elem in cymdist_input_names:
                cymdist_input_valref.append(cymdist.get_variable_valueref(elem))

            # Get the value references of cymdist outputs
            for elem in cymdist_output_names:
                cymdist_output_valref.append(cymdist.get_variable_valueref(elem))

            # Set the flag to save the results
            cymdist.set("_saveToFile", 0)
            # Get value reference of the configuration file
<<<<<<< HEAD
            cymdist_con_val_ref = cymdist.get_variable_valueref("_configurationFileName")

            # Set the configuration file
            cymdist.set_string([cymdist_con_val_ref], [cymdist_con_val_str])
=======
            cymdist_con_val_ref = cymdist.get_variable_valueref('_configurationFileName')

            # Set the configuration file
            cymdist.set_string([cymdist_con_val_ref], [cymdistr_con_val_str])
>>>>>>> d8b4d8fb522fe127188530096584087869e9a7a0

            # Initialize the FMUs
            cymdist.initialize()

            # Call event update prior to entering continuous mode.
            cymdist.event_update()

            # Enter continuous time mode
            cymdist.enter_continuous_time_mode()

            print("Done initializing the FMU")
            # Create vector to store time

<<<<<<< HEAD
            print ("Starting the time integration" )
            start = datetime.now()
=======
>>>>>>> d8b4d8fb522fe127188530096584087869e9a7a0
            cymdist.set_real(cymdist_input_valref, cymdist_input_values)
            print("This is the result of the angle IAngleA: "
                  + str(cymdist.get_real(cymdist.get_variable_valueref('IAngleA'))))

            # Terminate FMUs
            cymdist.terminate()
            end = datetime.now()

            print(
                'Ran a single CYMDIST simulation with {!s} FMU={!s} in {!s} seconds.'.format(
                    tool, fmu_path, (end - start).total_seconds()))
            if(tool == 'Dymola'):
                # PyFMI fails to get the output of an OpenModelica FMU whereas Dymola does.
                # Hence we only assert for Dymola FMUs
                self.assertEqual(
                    cymdist.get_real(
                        cymdist.get_variable_valueref('IAngleA')),
                    -13.7,
                    'Values are not matching.')


if __name__ == "__main__":
    # Check command line options
    unittest.main()
