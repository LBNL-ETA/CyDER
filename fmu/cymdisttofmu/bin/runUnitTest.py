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
        if platform.system().lower() == 'windows':
            for tool in ['dymola', 'jmodelica', 'omc']:
                if tool == 'omc':
                    modPat = 'OPENMODELICALIBRARY'
                    mosT = MOS_TEMPLATE_PATH_OPENMODELICA
                elif tool == 'dymola':
                    modPat = 'MODELICAPATH'
                    mosT = MOS_TEMPLATE_PATH_DYMOLA
                elif tool == 'jmodelica':
                    modPat = None
                    mosT = MOS_TEMPLATE_PATH_JMODELICA
                for version in ['1', '2']:
                    if (tool == 'omc' or tool == 'jmodelica'):
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
        else:
            print('The unit tests for exporting FMUs only run on Windows')

    #@unittest.skip("Run the FMU using PyFMI")
    def test_run_cymdist_fmu(self):
        '''
        Test the execution of one CYMDIST FMU.

        '''
        if platform.system().lower() == 'windows':
            for tool in ['OpenModelica', 'JModelica', 'Dymola']:
                fmu_path = os.path.join(
                        script_path, '..', 'fmus', tool, 'windows', 'CYMDIST.fmu')
                # Parameters which will be arguments of the function
                start_time = 0.0
                stop_time = 5.0
    
            print ('Starting the simulation')
            start = datetime.now()
            # Path to configuration file
            cymdistr_con_val_str = os.path.abspath('config.json')
            if sys.version_info.major > 2:
                cymdistr_con_val_str = bytes(cymdistr_con_val_str, 'utf-8')

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
                cymdist_con_val_ref = cymdist.get_variable_valueref('_configurationFileName')
    
                # Set the configuration file
                # Setting strings failed in JModelica. This seems to be a bug
                # since JModelica sets the variability of models which contain
                # a string parameter to constant. Consequently the FMU cannot
                # be modified at runtime. The workaround will be to pass the
                # path to the configuration file when invoking SimulatorToFMU so
                # it has the configuration file in its resource folders.
                if not (tool=='JModelica'):
                    simulator.set_string(
                        [simulator_con_val_ref],
                        [simulator_con_val_str])
    
                # Initialize the FMUs
                cymdist.initialize()
    
                # Call event update prior to entering continuous mode.
                cymdist.event_update()
    
                # Enter continuous time mode
                cymdist.enter_continuous_time_mode()
    
                # set inputs
                cymdist.set_real(cymdist_input_valref, cymdist_input_values)
                print("This is the result of the angle IAngleA: "
                      + str(cymdist.get_real(cymdist.get_variable_valueref('IAngleA'))))
    
                # Terminate FMUs
                cymdist.terminate()
                end = datetime.now()
    
                print(
                    'Ran a single CYMDIST simulation with {!s} FMU={!s} in {!s} seconds.'.format(
                        tool, fmu_path, (end - start).total_seconds()))
                if not(tool == 'OpenModelica'):
                    # PyFMI fails to get the output of an OpenModelica FMU.
                    self.assertEqual(
                        cymdist.get_real(
                            cymdist.get_variable_valueref('IAngleA')),
                        -13.7,
                        'Values are not matching.')
        else:
            print('The unit tests for simulating FMUs only run on Windows')
                    


if __name__ == "__main__":
    unittest.main()
