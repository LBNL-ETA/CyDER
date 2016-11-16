'''
Created on Oct 7, 2016

@author: Thierry S. Nouidui
@requires: Python 3.4 and higher
@contact: TSNouidui@lbl.gov
@note: CYMDIST 7.2 to FMU

'''

from lxml import etree
from datetime import datetime
import xml.etree.ElementTree as ET
import jinja2 as jja2
import logging as log
import subprocess as sp
import os
import sys
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

# Get the path to the templates files
script_path = os.path.dirname(os.path.realpath(__file__))
utilities_path=os.path.join(script_path, 'utilities')
MO_TEMPLATE_PATH = os.path.join(utilities_path, CYMDISTModelicaTemplate_MO)
MOS_TEMPLATE_PATH = os.path.join(utilities_path, CYMDISTModelicaTemplate_MOS)
XSD_FILE_PATH = os.path.join(utilities_path, XSD_SCHEMA)

#########################################
# # TEST FILES TO BE PROVIDED BY THE USER
XML_INPUT_PATH = 'HL0004.xml'
INPUT_FILE_PATH = 'HL0004.sxst'
#########################################


def main():
    """Illustrate how to export CYMDIST as an FMU.

    """
    import argparse
    
    # Configure the argument parser
    parser = argparse.ArgumentParser(description='Export CYMDIST as a Functional Mock-up Unit'\
                                      ' (FMU) for model exchange 2.0.')
    cymdist_group = parser.add_argument_group("Required arguments to export CYMDIST as an FMU")

    cymdist_group.add_argument("-g", "--grid-model-path", required=True,
                        help="Path to the Grid model")
    cymdist_group.add_argument('-i', "--input-file-path", required=True,
                        help="Path to the input file")
    cymdist_group.add_argument("-b", "--buildings-lib-path",
                        help='Path to the Buildings library, e.g. c:\\test\\xxx\\modelica-buildings')
    cymdist_group.add_argument("-r", "--write-results",
                        type=int,
                        help='Flag for writing results. 1 for writing, 0 else. Default is 0.')

    # Parse the arguments
    args = parser.parse_args()
        
    # Set defaults for command-line options.
    grid_model_path = args.grid_model_path
    input_file_path = args.input_file_path

    buildings_lib_path = args.buildings_lib_path
    if (buildings_lib_path is None):
        log.info('The path to the Buildings library was not provided.')
        log.info('Start searching the MODELICAPATH to see if it is defined.')
        buildings_lib_path = os.environ.get('MODELICAPATH')
        if (buildings_lib_path is None):
            log.error('The path to the Buildings library was neither'
                      +' provided nor found on the MODELICAPATH.')
    write_results = 0
    
    # Check if any errors
    if(grid_model_path is None):
        log.error('Missing required input, <path-to-grid-model>')
        parser.print_help()
        sys.exit(1)
    if(buildings_lib_path is None):
        log.error('Missing required input, <path-to-buildings-lib>')
        parser.print_help()
        sys.exit(1)
    if(input_file_path is None):
        log.error('Missing required input, <path-to-input-file>')
        parser.print_help()
        sys.exit(1)
    CYMDIST = CYMDISTWritter(grid_model_path,
                             input_file_path,
                             buildings_lib_path,
                             MO_TEMPLATE_PATH,
                             MOS_TEMPLATE_PATH, 
                             XSD_FILE_PATH,
                             write_results)
    start = datetime.now()
    retVal = -1
    ret_val = CYMDIST.print_mo()
    if(ret_val!= 0):
        log.error(
            'Could not print the CYMDIST Modelica model. Error in print_mo()')
        parser.print_help()
        sys.exit(1)
    ret_val = -1
    ret_val = CYMDIST.generate_fmu()
    if(ret_val != 0):
        log.error(
            'Could not generate the CYMDIST FMU. Error in generate_fmu()')
        parser.print_help()
        sys.exit(1)
    ret_val = -1
    ret_val = CYMDIST.clean_temporary()
    if(ret_val != 0):
        log.error(
            'Could not clean temporary files. Error in clean_temporary()')
        parser.print_help()
        sys.exit(1)
    ret_val = -1
    ret_val = CYMDIST.rewrite_fmu()
    if(ret_val != 0):
        log.error('Could not rewrite CYMDIST FMU. Error in rewrite_fmu()')
        parser.print_help()
        sys.exit(1)
    end = datetime.now()
    
    log.info('Export CYMDIST as an FMU in ' +
          str((end - start).total_seconds()) + ' seconds.')

def print_cmd_line_usage():
    """ Print command line usage.

    """

    print('USAGE:', os.path.basename(__file__),
          '-g <path-to-grid-file>  [-i <path-to-input-file>]'
          ' [-b] <path-to-Buildings-file> [-x] <path-to-xsd-file>')
    print('-- Export a CYMDIST model as a Functional Mockup Unit' + \
          ' (FMU) for model exchange 2.0')
    print('-- Input -g, Path to the grid model (required).')
    print('-- Input -i, Path to the input file (required).')
    print('-- Input -b, Path to the Buildings library (required).')
    print('-- Option -r, Flag for writing results. 0 if results'+ \
          ' should not be written, 1 else. Default is 0.')


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
        
        # Remove Invalid characterss from the model name as this is used 
        # by the Modelica model and the FMU
        log.info('Invalid characters will be removed from the '
                 'model name  ' + self.model_name + '.')
        self.model_name = sanitize_name(self.model_name)
        log.info('The new model name is ' + self.model_name + '.')

        # Assert if version is different from FMI 2.0
        assert (not(fmi_version is '2.0')), 'The FMI version 2.0 \
            is the only version currently supported.'

        # Iterate through the XML file and get the ModelVariables.
        input_variable_names = []
        modelica_input_variable_names = []
        # modelicaInputVariableNames = []
        output_variable_names = []
        modelica_concat_output_variable_names = []
        output_device_names = []
        concat_output_variable_names = []
        parameter_variable_values = []
        parameter_variable_names = []
        modelica_parameter_variable_names = []
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
                #scalar_variable['name'] = name
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
                        log.info('The output name ' + name + ' will be concatenated '
                                 'with the device name ' + devName + ' to be unique.')
                        new_name = name + '_' + devName
                        log.info('The new output name is ' + new_name + '.')
                        
                        log.info('Invalid characters will be removed from the '
                         'concatenated output variable name ' + new_name + '.')
                        new_name = sanitize_name(new_name)
                        log.info('The new concatenated output variable name is ' \
                                 + new_name + '.')
                        modelica_concat_output_variable_names.append(new_name)
                        scalar_variable['name'] = new_name
                        #concat_output_variable_names.append(scalar_variable['name'])
                        
                    if ((start is None) and ((causality == 'input')
                                             or causality == 'parameter')):
                        # Set the start value of input and parameter to zero.
                        # This assumes that we are only dealing with Integers
                        # This is because of the start value which is set to 0.0.
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
                        log.info('Invalid characters will be removed from the '
                         'input variable name ' + name + '.')
                        new_name = sanitize_name(name)
                        log.info('The new input variable name is ' \
                                 + new_name + '.')
                        modelica_input_variable_names.append(new_name)
                        scalar_variable['name'] = new_name
                        
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
                        log.info('Invalid characters will be removed from the '
                         'parameter variable name ' + name + '.')
                        new_name = sanitize_name(name)
                        log.info('The new parameter variable name is ' \
                                 + new_name + '.')
                        modelica_parameter_variable_names.append(new_name)
                        scalar_variable['name'] = new_name
                        parameter_variable_values.append(start)
                    scalar_variable['vartype'] = vartype
                    scalar_variable['unit'] = unit
                    if not (start is None):
                        scalar_variable['start'] = start
                scalar_variables.append(scalar_variable)
            # perform some checks on variables to avoid name clashes
            # before returning the variables to Modelica            
            log.info('Check for duplicates in input, output and parameter variable names')
            for i in [modelica_input_variable_names,
                      modelica_concat_output_variable_names,
                      modelica_parameter_variable_names]:
                check_duplicates(i)

            # Write success.
            log.info('Parsing of ' + self.xml_path + ' was successfull.')
            return scalar_variables, input_variable_names, \
                output_variable_names, concat_output_variable_names, \
                output_device_names, parameter_variable_names, \
                parameter_variable_values, modelica_input_variable_names, \
                modelica_concat_output_variable_names, \
                modelica_parameter_variable_names

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
            parameter_variable_values, \
            modelica_input_variable_names, \
            modelica_concat_output_variable_names, \
            modelica_parameter_variable_names = self.xml_parser()

        loader = jja2.FileSystemLoader(self.moT_path)
        env = jja2.Environment(loader=loader)
        template = env.get_template('')

        # Call template with parameters
        output_res = template.render(model_name=self.model_name,
                                     input_file_path=self.input_file_path,
                                     write_results=self.write_results,
                                     scalar_variables=scalar_variables,
                                     input_variable_names=input_variable_names,
                                     output_variable_names=output_variable_names,
                                     concat_output_variable_names=concat_output_variable_names,
                                     output_device_names=output_device_names,
                                     parameter_variable_names=parameter_variable_names,
                                     parameter_variable_values=parameter_variable_values,
                                     modelica_input_variable_names=modelica_input_variable_names,
                                     modelica_concat_output_variable_names=modelica_concat_output_variable_names,
                                     modelica_parameter_variable_names=modelica_parameter_variable_names)
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
        sp.call(['dymola', output_file, '/nowindow'])

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
