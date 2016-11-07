'''
Created on Oct 7, 2016

@author: Thierry S. Nouidui
@requires: Python 3.4 and higher
@contact: TSNouidui@lbl.gov
@note: CYMDIST 7.2 to FMU

'''

from lxml import etree
import xml.etree.ElementTree as ET
import jinja2 as jja2
import logging as log
import subprocess as sp
import os
import sys
import platform
import shutil
import zipfile
import re

log.basicConfig(filename='CYMDIST.log', filemode='w',
                level=log.DEBUG, format='%(asctime)s %(message)s',
                datefmt='%m/%d/%Y %I:%M:%S %p')
stderrLogger = log.StreamHandler()
stderrLogger.setFormatter(log.Formatter(log.BASIC_FORMAT))
log.getLogger().addHandler(stderrLogger)

# These files are required by the utility to run.
# They must be at the top level of the current working
# directory.
# XSD_SCHEMA: Schema used to validate the XML input
# CYMDISTModelicaTemplate_MO: Template used to write Modelica model
# CYMDISTModelicaTemplate_MOS: Template used to write mos script
XSD_SCHEMA = 'CYMDISTModelDescription.xsd'
NEEDSEXECUTIONTOOL = 'needsExecutionTool'
MODELDESCRIPTION = 'modelDescription.xml'
CYMDISTModelicaTemplate_MO = 'CYMDISTModelicaTemplate.mo'
CYMDISTModelicaTemplate_MOS = 'CYMDISTModelicaTemplate.mos'
#########################################
# # TEST FILES TO BE PROVIDED BY THE USER
if platform.system() == 'Linux':
    # Buildings path on the Linux Desktop
    BUILDINGS_PATH = '/home/thierry/Desktop/vmWareLinux/proj/buildings_library/models/modelica/git/buildings/modelica-buildings'
else:
    # Buildings path on the Windows Notebook
    BUILDINGS_PATH = 'Z:\\thierry\\proj\\buildings_library\\models\\modelica\\git\master\\modelica-buildings'
    # Buildings path on the Windows Desktop
    # BUILDINGS_PATH='Z:\\Ubuntu\proj\\buildings_library\\models\\modelica\\git\\buildings\\modelica-buildings'
XML_INPUT_PATH = 'HL0004.xml'
INPUT_FILE_PATH = 'HL0004.sxst'
FMUS_PATH = os.path.join('..', 'fmus', 'win32', 'Dymola', 'CYMDIST')
#########################################


def main():
    """Illustrate how to export CYMDIST as an FMU.

    """

    # Set defaults for command-line options.
    ret_val = -1
    grid_file_path = None
    input_file_path = None
    buildings_path = None
    mo_template_path = CYMDISTModelicaTemplate_MO
    mos_template_path = CYMDISTModelicaTemplate_MOS
    xsd_file_path = XSD_SCHEMA
    write_results = 0
    #
    # Get command-line options.
    lastIdx = len(sys.argv) - 1
    currIdx = 1
    while(currIdx < lastIdx):
        currArg = sys.argv[currIdx]
        if(currArg.startswith('-g')):
            currIdx += 1
            grid_file_path = sys.argv[currIdx]
            log.info(
                'Setting CYMDIST grid model path to {' + grid_file_path + '}')
        elif(currArg.startswith('-i')):
            currIdx += 1
            input_file_path = sys.argv[currIdx]
            log.info(
                'Setting CYMDIST XML input path to {' + input_file_path + '}')
        elif(currArg.startswith('-b')):
            currIdx += 1
            buildings_path = sys.argv[currIdx]
            log.info(
                'Setting Modelica Buildings path to {' + buildings_path + '}')
        elif(currArg.startswith('-m')):
            currIdx += 1
            mo_template_path = sys.argv[currIdx]
            log.info(
                'Setting Modelica template path to {' + mo_template_path + '}')
        elif(currArg.startswith('-s')):
            currIdx += 1
            mos_template_path = sys.argv[currIdx]
            log.info(
                'Setting Modelica script template path to {' + mos_template_path + '}')
        elif(currArg.startswith('-x')):
            currIdx += 1
            xsd_file_path = sys.argv[currIdx]
            log.info('Setting XSD validator path to {' + xsd_file_path + '}')
        elif(currArg.startswith('-r')):
            currIdx += 1
            write_results = int(sys.argv[currIdx])
            log.info(
                'Setting Flag for writing results to {' + str(write_results) + '}')
        else:
            quit_with_error('Bad command-line option {' + currArg + '}', True)
            # Here, processed option at {currIdx}.
        currIdx += 1

    if(grid_file_path is None):
        quit_with_error('Missing required input, <path-to-grid-file>', True)
    if(buildings_path is None):
        quit_with_error(
            'Missing required input, <path-to-Buildings-file>', True)
    if(input_file_path is None):
        quit_with_error('Missing required input, <path-to-input-file>', True)

    CYMDIST = CYMDISTWritter(grid_file_path,
                             input_file_path,
                             buildings_path,
                             mo_template_path,
                             mos_template_path,
                             xsd_file_path,
                             write_results)
    ret_val = CYMDIST.print_mo()
    if(ret_val != 0):
        quit_with_error(
            'Could not print the CYMDIST Modelica model. Error in print_mo()', True)
    ret_val = -1
    ret_val = CYMDIST.generate_fmu()
    if(ret_val != 0):
        quit_with_error(
            'Could not generate the CYMDIST FMU. Error in generate_fmu()', True)
    ret_val = -1
    ret_val = CYMDIST.clean_temporary()
    if(ret_val != 0):
        quit_with_error(
            'Could not clean temporary files. Error in clean_temporary()', True)
    ret_val = -1
    ret_val = CYMDIST.rewrite_fmu()
    if(ret_val != 0):
        quit_with_error('Could not rewrite CYMDIST FMU. Error in fmu()', True)


def print_cmd_line_usage():
    """ Print command line usage.

    """

    print('USAGE:', os.path.basename(__file__),
          '-g <path-to-grid-file>  [-i <path-to-input-file>]'
          ' [-b] <path-to-Buildings-file> [-x] <path-to-xsd-file>')
    print('-- Export a CYMDIST model as a Functional Mockup Unit (FMU) for Model Exchange 2.0')
    print('-- Input -g, Path to the grid model (required).')
    print('-- Input -i, Path to the input file (required).')
    print('-- Input -b, Path to the Buildings library (required).')
    print('-- Option -m, Path to the Modelica template file. Optional if run from the parser installation folder.')
    print('-- Option -s, Path to the Modelica script template file. Optional if run from the parser installation folder.')
    print('-- Option -x, Path to the XSD file. Optional if run from the parser installation folder.')
    print('-- Option -r, Flag to write results. 0 if results should not be written, 1 else. Default is 0.')


def quit_with_error(messageStr, showCmdLine):
    """ Terminate with an error.

        Args:
            messageStr(str): error message.
            showCmdLine(bool): if True show message.

    """

    print('ERROR from script file {' + os.path.basename(__file__) + '}')

    if(messageStr is not None):
        print(messageStr)

    if(showCmdLine):
        print(print_cmd_line_usage())

    sys.exit(1)


def check_duplicates(arr):
    """ Check duplicates in a list of variables.

    This function checks duplicates in a list
    and breaks if duplicates are found. Duplicates
    names are not allowed in the list of inputs, outputs,
    and parameters.

    Args:
        arr(str): list of string variables.

    """

    dup = set([x for x in arr if arr.count(x) > 1])
    lst_dup = list(dup)
    len_lst = len(lst_dup)
    if (len_lst > 0):
        log.error('There are duplicates names in the list '
                  + str(arr) + '.')
        log.error('This is invalid. Check your XML input file.')
        for i in lst_dup:
            log.error('Variable ' + i + ' has duplicates'
                      ' in the list ' + str(arr) + '.')
        # Assert if version is different from FMI 2.0
        assert(len_lst <= 0), 'Duplicates found in the list.'

# Invalid symbols
g_rexBadIdChars = re.compile(r'[^a-zA-Z0-9_]')


def sanitize_name(name):
    """ Make a Modelica valid name.

    In Modelica, a variable name:
    Can contain any of the characters {a-z,A-Z,0-9,_}.
    Cannot start with a number.

    Args:
        name(str): Variable name to be sanitized.

    """

    # Check if variable has a length > 0
    if(len(name) <= 0):
        log.error('Require a non-null variable name.')
        assert(len(name) > 0), 'Require a non-null variable name.'
    #
    # Check if variable starts with a number.
    if(name[0].isdigit()):
        log.warning('Variable Name ' + name + ' starts with 0.')
        log.warning('This is invalid.')
        log.warning('The name will be changed to start with f_.')
        name = 'f_' + name
    #
    # Replace all illegal characters with an underscore.
    name = g_rexBadIdChars.sub('_', name)
    #
    return(name)


def zip_fmu(dirPath=None, zipFilePath=None, includeDirInZip=True):
    """Create a zip archive from a directory.

    Note that this function is designed to put files in the zip archive with
    either no parent directory or just one parent directory, so it will trim any
    leading directories in the filesystem paths and not include them inside the
    zip archive paths. This is generally the case when you want to just take a
    directory and make it into a zip file that can be extracted in different
    locations.

    Args:
        dirPath(str): String path to the directory to archive. This is the only
        required argument. It can be absolute or relative, but only one or zero
        leading directories will be included in the zip archive.

        zipFilePath(str): String path to the output zip file. This can be an absolute
        or relative path. If the zip file already exists, it will be updated. If
        not, it will be created. If you want to replace it from scratch, delete it
        prior to calling this function. (default is computed as dirPath + ".zip")

        includeDirInZip(bool): Boolean indicating whether the top level directory
        should be included in the archive or omitted. (default True)

    Author: http://peterlyons.com/problog/2009/04/zip-dir-python

    """
    if not zipFilePath:
        zipFilePath = dirPath + '.zip'
    if not os.path.isdir(dirPath):
        raise OSError('dirPath argument must point to a directory. '
                      "'%s' does not." % dirPath)
    parentDir, dirToZip = os.path.split(dirPath)
    # Little nested function to prepare the proper archive path

    def trimPath(path):
        archivePath = path.replace(parentDir, "", 1)
        if parentDir:
            archivePath = archivePath.replace(os.path.sep, "", 1)
        if not includeDirInZip:
            archivePath = archivePath.replace(dirToZip + os.path.sep, "", 1)
        return os.path.normcase(archivePath)

    outFile = zipfile.ZipFile(zipFilePath, "w",
                              compression=zipfile.ZIP_DEFLATED)
    for (archiveDirPath, dirNames, fileNames) in os.walk(dirPath):
        for fileName in fileNames:
            filePath = os.path.join(archiveDirPath, fileName)
            outFile.write(filePath, trimPath(filePath))
        # Make sure we get empty directories as well
        if not fileNames and not dirNames:
            zipInfo = zipfile.ZipInfo(trimPath(archiveDirPath) + "/")
            outFile.writestr(zipInfo, "")
    outFile.close()


class CYMDISTWritter(object):

    """CYMDIST FMU writer.

    This class contains various methods to
    read and XML file, validate it against
    a pre-defined XML schema, extracting the
    variables attributes, writing a Modelica
    model of a CYMDIST model and exporting
    the model as an FMU for model exchange 2.0.

    """

    def __init__(self, input_file_path, xml_path, buildings_path,
                 moT_path, mosT_path, xsd_path, write_results):
        """Initialize the class.

        Args:
            input_file_path (str): The path to the CYMDIST grid model file.
            xml_path (str): The path to the XML file.
            buildings_path (str): The path to the folder
            which contains the Buildings library excluding
            the ending FILE SEPARATOR.
            moT_path (str): Modelica model template.
            mosT_path (str): Modelica script template.
            xsd_path (str): The path to the XML schema.
            write_results (int): Flag for results writing.

        """

        self.input_file_path = input_file_path
        self.xml_path = xml_path
        self.buildings_path = buildings_path + os.sep
        self.moT_path = moT_path
        self.mosT_path = mosT_path
        self.xsd_path = xsd_path
        self.write_results = write_results

    def xml_validator(self):
        """Validate the XML file.

        This function validates the XML file
        against CYMDISTModelDescription.xsd.

        """

        try:
            # Get the XML schema to validate against
            xml_schema = etree.XMLSchema(file=self.xsd_path)
            # Parse string of XML
            xml_doc = etree.parse(self.xml_path)
            # Validate parsed XML against schema
            xml_schema.assertValid(xml_doc)
            # Validate parsed XML against schema returning
            # boolean value indicating success/failure
            result = xml_schema.validate(xml_doc)
            if result:
                log.info(self.xml_path + ' is a valid XML document.')
            return result
        except etree.XMLSchemaParseError as xspe:
            # Something wrong with the schema (getting from URL/parsing)
            print('XMLSchemaParseError occurred!')
            print(xspe)
        except etree.XMLSyntaxError as xse:
            # XML not well formed
            print('XMLSyntaxError occurred!')
            print(xse)
        except etree.DocumentInvalid:
            # XML failed to validate against schema
            print('DocumentInvalid occurred!')
            error = xml_schema.error_log.last_error
            if error:
                # All the error properties (from libxml2) describing what went
                # wrong
                print('domain_name: ' + error.domain_name)
                print('domain: ' + str(error.domain))
                print('filename: ' + error.filename)
                print('level: ' + str(error.level))
                print('level_name: ' + error.level_name)  # an integer
                # a unicode string that identifies the line where the error
                # occurred.
                print('line: ' + str(error.line))
                # a unicode string that lists the message.
                print('message: ' + error.message)
                print('type: ' + str(error.type))  # an integer
                print('type_name: ' + error.type_name)

    def xml_parser(self):
        """Parse the XML file.

        This function parses the XML file which contains
        the input, output,  and parameters of a CYMDIST
        model. It extracts the variables attributes
        needed to write the CYMDIST Modelica model.

        """

        # Get the XML file
        tree = ET.parse(self.xml_path)
        # Get the root of the tree
        root = tree.getroot()

        # Get the FMI Version for checking
        fmi_version = root.attrib.get('fmiVersion')
        # Get the model name to write the .mo file
        self.model_name = root.attrib.get('modelName')

        # Assert if version is different from FMI 2.0
        assert (not(fmi_version is '2.0')), 'The FMI version 2.0 \
            is the only version currently supported.'

        # Iterate through the XML file and get the ModelVariables.
        input_variable_names = []
        # modelicaInputVariableNames = []
        output_variable_names = []
        output_device_names = []
        concat_output_variable_names = []
        parameter_variable_values = []
        parameter_variable_names = []
        # modelicaParameterVariableNames = []
        # Parameters used to write annotations.
        inpY1 = 88
        inpY2 = 110
        outY1 = 88
        outY2 = 108
        indel = 20
        outdel = 18

        scalar_variables = []
        for child in root.iter('ModelVariables'):
            for element in child:
                scalar_variable = {}
                # Iterate through ScalarVariables and get attributes
                (name, description, causality) = element.attrib.get('name'), \
                    element.attrib.get('description'), \
                    element.attrib.get('causality').lower()
                # Iterate through children of ScalarVariables and get
                # attributes
                scalar_variable['name'] = name
                for subelement in element:
                    vartype = subelement.tag
                    vartype_low = vartype.lower()
                    # Modelica types are case sensitive.
                    # This code makes sure that we get correct
                    # Modelica types if the user mistypes them.
                    if (vartype_low == 'real'):
                        # Make sure that we have
                        # a valid Modelica type.
                        vartype = 'Real'
                        unit = subelement.attrib.get('unit')
                        start = subelement.attrib.get('start')
                    # Get the device name of an output variable
                    if (vartype_low == 'device' and causality == 'output'):
                        devName = subelement.attrib.get('name')
                        # Create list of output variables
                        output_variable_names.append(name)
                        # Create list with device name of output variable
                        output_device_names.append(devName)
#                         log.info('Output with name ' + name
#                                  + ' will be sanitized'
#                                  ' to remove invalid Modelica characters.')
#                         newOutputName = sanitize_name(name)
#                         log.info('The Modelica output name is '
#                                  + newOutputName + '.')
#                         log.info('Device with name ' + devName
#                                  + ' will be sanitized to remove'
#                                  ' invalid Modelica characters.')
#                         newDeviceName = sanitize_name(devName)
#                         log.info('The Modelica device name is '
#                                  + newDeviceName + '.')
#                         log.info('The output name will be concatenated '
#                                  'with the sanitized device name to be unique.')
#                         newOutputName = newOutputName + '_' + newDeviceName
#                         log.info('The Modelica output name is '
#                                  + newOutputName + '.')
#                         modelicaOutputVariableNames.append(newOutputName)
#                         # Assign variable name to the dictionary
#                         scalar_variable['name'] = newOutputName
                        log.info('The output name ' + name + ' will be concatenated '
                                 'with the device name ' + devName + ' to be unique.')
                        scalar_variable['name'] = name + '_' + devName
                        concat_output_variable_names.append(
                            scalar_variable['name'])
                        log.info('The new output name is ' +
                                 scalar_variable['name'] + '.')
                    if ((start is None) and ((causality == 'input')
                                             or causality == 'parameter')):
                        # Set the start value of input and parameter to zero.
                        # This assumes that we are only dealing with Integers
                        # This is because of the start value which is set to
                        # 0.0.
                        log.warning('Start value of variable '
                                    + name + ' with causality '
                                    + causality + ' is not defined.'
                                    + 'The start value will be set to 0.0 by default.')
                        start = 0.0
                    elif not(start is None):
                        start = float(start)
                    # Create a dictionary
                    # scalar_variable['name'] = name
                    if not (description is None):
                        scalar_variable['description'] = description
                    # If there is no description set this to
                    # be an empty string.
                    else:
                        scalar_variable['description'] = ''
                    scalar_variable['causality'] = causality
                    if (causality == 'input'):
                        input_variable_names.append(name)
#                         log.info('Input with name ' + name
#                                  + ' will be sanitized to remove'
#                                  ' invalid Modelica characters.')
#                         newName = sanitize_name(name)
#                         log.info('The Modelica input name is ' + newName + '.')
#                         modelicaInputVariableNames.append(newName)
#                         # Assign variable name to the dictionary
#                         scalar_variable['name'] = newName
                        inpY1 = inpY1 - indel
                        inpY2 = inpY2 - indel
                        scalar_variable['annotation'] = (' annotation'
                                                         '(Placement'
                                                         '(transformation'
                                                         '(extent={{-122,'
                                                         + str(inpY1) + '},'
                                                         '{-100,' + str(inpY2)
                                                         + '}})))')
                    if (causality == 'output'):
                        outY1 = outY1 - outdel
                        outY2 = outY2 - outdel
                        scalar_variable['annotation'] = (' annotation'
                                                         '(Placement'
                                                         '(transformation'
                                                         '(extent={{100,'
                                                         + str(outY1) + '},'
                                                         '{120,' + str(outY2)
                                                         + '}})))')
                    if (causality == 'parameter'):
                        parameter_variable_names.append(name)
#                         log.info('Parameter with name ' + name
#                                  + ' will be sanitized to remove'
#                                  ' invalid Modelica characters.')
#                         newName = sanitize_name(name)
#                         log.info('The Modelica parameter name is '
#                                  + newName + '.')
#                         modelicaParameterVariableNames.append(newName)
#                         # Assign variable name to the dictionary
#
#                         scalar_variable['name'] = newName
                        parameter_variable_values.append(start)
                    scalar_variable['vartype'] = vartype
                    scalar_variable['unit'] = unit
                    if not (start is None):
                        scalar_variable['start'] = start
                scalar_variables.append(scalar_variable)
            # perform some checks on variables to avoid name clashes
            # before returning the variables to Modelica
#             for i in [modelicaInputVariableNames,
#                       modelicaOutputVariableNames,
#                       modelicaParameterVariableNames]:
#                 check_duplicates (i)
            for i in [input_variable_names,
                      concat_output_variable_names,
                      parameter_variable_names]:
                check_duplicates(i)

            # Write success.
            log.info('Parsing of ' + self.xml_path + ' was successfull.')
#             return scalar_variables, input_variable_names, modelicaInputVariableNames, \
#                 output_variable_names, modelicaOutputVariableNames, output_device_names, \
#                 parameter_variable_names, modelicaParameterVariableNames, parameter_variable_values
            return scalar_variables, input_variable_names, \
                output_variable_names, concat_output_variable_names, \
                output_device_names, parameter_variable_names, \
                parameter_variable_values

    def print_mo(self):
        """Print the Modelica model of a CYMDIST XML file.

        This function parses a CYMDIST XML file and extracts
        the variables attributes needed to write the CYMDIST
        Modelica model. It then writes the Modelica model.
        The name of the Modelica model is the model_name in the
        model description file. This is used to avoid
        name conflicts when generating multiple CYMDIST models.

        """

        self.xml_validator()
        scalar_variables, input_variable_names, \
            output_variable_names, \
            concat_output_variable_names, \
            output_device_names, \
            parameter_variable_names, \
            parameter_variable_values = self.xml_parser()

        loader = jja2.FileSystemLoader(self.moT_path)
        env = jja2.Environment(loader=loader)
        template = env.get_template('')

        # Call template with parameters
        output_res = template.render(model_name=self.model_name,
                                     input_file_path=self.input_file_path,
                                     write_results=self.write_results,
                                     scalar_variables=scalar_variables,
                                     input_variable_names=input_variable_names,
                                     #                         modelicaInputVariableNames=modelicaInputVariableNames,
                                     output_variable_names=output_variable_names,
                                     concat_output_variable_names=concat_output_variable_names,
                                     output_device_names=output_device_names,
                                     parameter_variable_names=parameter_variable_names,
                                     #                         modelicaParameterVariableNames=modelicaParameterVariableNames,
                                     parameter_variable_values=parameter_variable_values)
        # Write results in mo file which has the same name as the class name
        output_file = self.model_name + '.mo'
        if os.path.isfile(output_file):
            log.warning('The output file ' + output_file
                        + ' exists and will be overwritten.')
        with open(output_file, 'w') as fh:
            fh.write(output_res)
        fh.close()

        # Write success.
        log.info('The Modelica model ' + output_file +
                 ' of ' + self.model_name + ' is successfully created.')
        log.info('The Modelica model ' + output_file +
                 ' of ' + self.model_name + ' is in ' + os.getcwd() + '.')
        return 0

    def generate_fmu(self):
        """Generate the CYMDIST FMU.

        This function writes the mos file which is used to create the
        CYMDIST FMU. The function requires the path to the Buildings
        library which will be set to the MODELICAPATH.
        The function calls Dymola to run the mos file and
        writes a CYMDIST FMU. The CYMDIST FMU cannot be used yet
        as Dymola does not support the export of FMUs which
        has the needsExecutionTool set to true.

        """

        # Set the Modelica path to point to the Buildings Library
        os.environ['MODELICAPATH'] = self.buildings_path

        loader = jja2.FileSystemLoader(self.mosT_path)
        env = jja2.Environment(loader=loader)
        template = env.get_template('')

        output_res = template.render(model_name=self.model_name,
                                     buildings_path=self.buildings_path)
        # Write results in mo file which has the same name as the class name
        output_file = self.model_name + '.mos'
        if os.path.isfile(output_file):
            log.warning('The output file ' + output_file
                        + ' exists and will be overwritten.')
        with open(output_file, 'w') as fh:
            fh.write(str(output_res))
        fh.close()

        # Call Dymola to generate the FMUs
        sp.call(['dymola', output_file])

        # Define name of the FMU
        fmu_name = self.model_name + '.fmu'

        # Write scuccess.
        log.info('The FMU ' + fmu_name + ' is successfully created.')
        log.info('The FMU ' + fmu_name + ' is in ' + os.getcwd() + '.')

        return 0

    def clean_temporary(self):
        """Clean temporary generated files.

        """
        temporary = ['buildlog.txt', 'dsin.txt', 'dslog.txt', 'dymosim',
                     'request.', 'status.', 'dsmodel.c',
                     'dsmodel_fmuconf.h', 'fmiModelIdentifier.h']
        for fil in temporary:
            if os.path.isfile(fil):
                os.remove(fil)
        # FMU folders generated by Dymola.
        DymFMU_tmp = ['~FMUOutput', '.FMUOutput',
                      'DymosimDll32', 'DymosimDll64']
        for fol in DymFMU_tmp:
            if os.path.isdir(fol):
                shutil.rmtree(fol)

        return 0

    def rewrite_fmu(self):
        """Add needsExecutionTool to the CYMDIST FMU.

        This function unzips the FMU generated with generate_fmu(),
        reads the xml file, and add needsExecutionTool to the FMU capabilities.
        The function completes the process by re-zipping the FMU.
        The new FMU contains the modified XML file as well as the binaries.

        """

        fmutmp = self.model_name + '.tmp'
        zipdir = fmutmp + '.zip'
        fmu_name = self.model_name + '.fmu'

        if os.path.exists(fmutmp):
            shutil.rmtree(fmutmp)

        if not os.path.exists(fmutmp):
            os.makedirs(fmutmp)

        # Copy file to temporary folder
        shutil.copy2(fmu_name, fmutmp)

        # Get the current working directory
        cwd = os.getcwd()

        # Change to the temporary directory
        os.chdir(fmutmp)

        # Unzip folder which contains he FMU
        zip_ref = zipfile.ZipFile(fmu_name, 'r')
        zip_ref.extractall('.')
        zip_ref.close()

        log.info('The model description file will be rewritten' +
                 ' to include the attribute ' + NEEDSEXECUTIONTOOL +
                 ' set to true.')
        tree = ET.parse(MODELDESCRIPTION)
        # Get the root of the tree
        root = tree.getroot()
        # Add the needsExecution tool attribute
        root.attrib[NEEDSEXECUTIONTOOL] = 'true'
        tree.write(MODELDESCRIPTION, xml_declaration=True)
        if os.path.isfile(fmu_name):
            os.remove(fmu_name)

        # Switch back to the current working directory
        os.chdir(cwd)

        # Pass the directory which will be zipped
        # and call the zipper function.
        zip_fmu(fmutmp, includeDirInZip=False)

        # Check if fmu_name exists in current directory
        # If that is the case, delete it or rename to tmp?
        fmu_name_original = fmu_name + '.original'
        if os.path.isfile(fmu_name):
            log.info('The original CYMDIST FMU ' + fmu_name +
                     ' will be renamed to ' + fmu_name + '.original.')
            log.info('A modified version of the original will be created.')
            log.info('The difference between the original and the new FMU lies'
                     ' in the model description file of the new FMU which has'
                     ' the attribute ' + NEEDSEXECUTIONTOOL + ' set to true.')
            if os.path.isfile(fmu_name_original):
                os.remove(fmu_name_original)
            os.rename(fmu_name, fmu_name_original)

        # Rename the FMU name to be the name of the FMU
        # which will be used for the simulation. This FMU
        # contains the needsExecutionTool flag.
        os.rename(zipdir, fmu_name)

        # Copy FMU to unit test folder
        # log.info('Copy FMU ' + fmu_name + ' to unit test folder '
        #         + FMUS_PATH + ' so it can be run with the FMU checker.')
        #shutil.copy2(fmu_name, FMUS_PATH)

        # Delete temporary folder
        shutil.rmtree(fmutmp)

        # Write scuccess.
        log.info('The FMU ' + fmu_name + ' is successfully re-created.')
        log.info('The FMU ' + fmu_name + ' is in ' + os.getcwd() + '.')

        return 0

if __name__ == '__main__':
    # Try running this module!
    # Set defaults for command-line options.
    main()
