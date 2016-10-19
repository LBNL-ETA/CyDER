'''
Created on Oct 7, 2016

@author: Thierry S. Nouidui
'''
from lxml import etree
import xml.etree.ElementTree as ET
import jinja2 as jja2
import os.path as path
import logging as log
import subprocess as sp
import os
import platform
import shutil
import zipfile

log.basicConfig(filename="CYMDIST.log",  filemode='w', 
                    level=log.DEBUG, format='%(asctime)s %(message)s', 
                    datefmt='%m/%d/%Y %I:%M:%S %p')
stderrLogger=log.StreamHandler()
stderrLogger.setFormatter(log.Formatter(log.BASIC_FORMAT))
log.getLogger().addHandler(stderrLogger)

# These files are required by the utility to run. 
# They must be at the top level of the current working 
# directory.
# XSD_SCHEMA: Schema used to validate the XML input
# CYMDISTModelicaTemplate_MO: Template used to write Modelica model
# CYMDISTModelicaTemplate_MOS: Template used to write mos script
XSD_SCHEMA = "./CYMDISTModelDescription.xsd"
NEEDSEXECUTIONTOOL = "needsExecutionTool"
MODELDESCRIPTION="modelDescription.xml"
CYMDISTModelicaTemplate_MO="CYMDISTModelicaTemplate.mo"
CYMDISTModelicaTemplate_MOS="CYMDISTModelicaTemplate.mos"
#########################################
## TEST FILES TO BE PROVIDED BY THE USER
if platform.system()=='Linux':
    BUILDINGS_PATH="/home/thierry/Desktop/vmWareLinux/proj/buildings_library/models/modelica/git/buildings/modelica-buildings"
else:
    BUILDINGS_PATH="Z:\\Ubuntu\proj\\buildings_library\\models\\modelica\\git\\buildings\\modelica-buildings"
XML_INPUT_PATH="./CYMDISTModelDescription.xml"
INPUT_FILE_PATH = "./CYMDIST.inp"
######################################### 

def main():
        
    """Illustrate how to export CYMDIST as an FMU.
    
    
    """
    
    CYMDIST = CYMDISTWritter(INPUT_FILE_PATH, XML_INPUT_PATH, BUILDINGS_PATH)
    CYMDIST.print_mo()
    #CYMDIST.generate_fmu()
    #CYMDIST.clean_temporary()
    #CYMDIST.rewrite_fmu()

def zip_fmu(dirPath=None, zipFilePath=None, includeDirInZip=True):
    """Create a zip archive from a directory.
    
    Note that this function is designed to put files in the zip archive with
    either no parent directory or just one parent directory, so it will trim any
    leading directories in the filesystem paths and not include them inside the
    zip archive paths. This is generally the case when you want to just take a
    directory and make it into a zip file that can be extracted in different
    locations. 
    
    Keyword arguments:
    
    dirPath -- string path to the directory to archive. This is the only
    required argument. It can be absolute or relative, but only one or zero
    leading directories will be included in the zip archive.

    zipFilePath -- string path to the output zip file. This can be an absolute
    or relative path. If the zip file already exists, it will be updated. If
    not, it will be created. If you want to replace it from scratch, delete it
    prior to calling this function. (default is computed as dirPath + ".zip")

    includeDirInZip -- boolean indicating whether the top level directory should
    be included in the archive or omitted. (default True)
    
    Author: http://peterlyons.com/problog/2009/04/zip-dir-python

    """
    if not zipFilePath:
        zipFilePath = dirPath + ".zip"
    if not os.path.isdir(dirPath):
        raise OSError("dirPath argument must point to a directory. "
            "'%s' does not." % dirPath)
    parentDir, dirToZip = os.path.split(dirPath)
    #Little nested function to prepare the proper archive path
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
        #Make sure we get empty directories as well
        if not fileNames and not dirNames:
            zipInfo = zipfile.ZipInfo(trimPath(archiveDirPath) + "/")
            #some web sites suggest doing
            #zipInfo.external_attr = 16
            #or
            #zipInfo.external_attr = 48
            #Here to allow for inserting an empty directory.  Still TBD/TODO.
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


    def __init__(self, input_file_path, xml_path, buildings_path):
        """Initialize the class.
        
        Args:
            inputFile_path (str): The path to the CYMDIST input file.
            xml_path (str): The path to the XML file.
            buildings_path (str): The path to the folder
            which contains the Buildings library excluding 
            the ending FILE SEPARATOR.
        
        """
        
        self.input_file_path = input_file_path
        self.xml_path = xml_path
        self.buildings_path = buildings_path + os.sep
             
    def xml_validator(self):
        """Validate the XML file.
        
        This function validates the XML file 
        against CYMDISTModelDescription.xsd.
        
        """
        
        try:
            # Get the XML schema to validate against
            xmlschema = etree.XMLSchema(file=XSD_SCHEMA)
            # Parse string of XML
            xml_doc = etree.parse(self.xml_path)
            # Validate parsed XML against schema
            xmlschema.assertValid(xml_doc)
            # Validate parsed XML against schema returning 
            # boolean value indicating success/failure
            result = xmlschema.validate(xml_doc)
            if result:
                log.info(self.xml_path + " is a valid XML document.")
            return result
        except etree.XMLSchemaParseError, xspe:
            # Something wrong with the schema (getting from URL/parsing)
            print "XMLSchemaParseError occurred!"
            print xspe
        except etree.XMLSyntaxError, xse:
            # XML not well formed
            print "XMLSyntaxError occurred!"
            print xse
        except etree.DocumentInvalid:
            # XML failed to validate against schema
            print "DocumentInvalid occurred!"
            error = xmlschema.error_log.last_error
            if error:
                # All the error properties (from libxml2) describing what went wrong
                print 'domain_name: ' + error.domain_name
                print 'domain: ' + str(error.domain)
                print 'filename: ' + error.filename
                print 'level: ' + str(error.level)
                print 'level_name: ' + error.level_name  # an integer
                print 'line: ' + str(error.line)  # a unicode string that identifies the line where the error occurred.
                print 'message: ' + error.message  # a unicode string that lists the message.
                print 'type: ' + str(error.type)  # an integer
                print 'type_name: ' + error.type_name
    
    
            
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
        fmiVersion = root.attrib.get("fmiVersion")
        # Get the model name to write the .mo file 
        self.modelName = root.attrib.get("modelName")
        
        # Assert if version is different from FMI 2.0
        assert (not(fmiVersion is "2.0")), "The FMI version 2.0 \
            is the only version currently supported."
  
        # Iterate through the XML file and get the ModelVariables.
        inputVariableNames = []
        outputVariableNames = []
        parameterVariableValues = []
        parameterVariableNames = []
        inpY1 = 88
        inpY2 = 110
        outY1 = 88
        outY2 = 108
        inCnt=0
        outCnt=0
        indel = 20
        outdel = 18

        for child in root.iter("ModelVariables"):
            scalarVariables = []
            # print(child.tag, child.attrib)
            for element in child:
                scalarVariable = {}
                # Iterate through ScalarVariables and get attributes
                (name, description, causality) = element.attrib.get("name"), \
                    element.attrib.get("description"), element.attrib.get("causality")
                # Iterate through children of ScalarVariables and get attributes
                for subelement in element:
                    vartype = subelement.tag
                    unit = subelement.attrib.get("unit")
                    start = subelement.attrib.get("start")
                    if ((start is None) and ((causality=="input") or causality=="parameter")):
                        # Set the start value of input and parameter to zero.
                        # This assumes that we are only dealing with Integers
                        # This is because of the start value which is set to 0.0.
                        log.warning( "Start value of variable " + name + 
                                     " with causality " + causality + " is not defined."+
                                     "The start value will be set to 0.0 by default.")
                        start = 0.0
                    elif not(start is None):
                        start = float(start)
                    # Create a dictionary
                    scalarVariable["name"] = name
                    if not (description is None):
                        scalarVariable["description"] = description
                    # If there is no description set this to
                    # be an empty string.
                    else:
                        scalarVariable["description"] = ""
                    scalarVariable["causality"] = causality
                    if (causality=="input"):
                        inputVariableNames.append(name)
                        inpY1 = inpY1 - inCnt*indel
                        inpY2 = inpY2 - inCnt*indel
                        inCnt+=1
                        scalarVariable["annotation"] = (" annotation"
                                                        "(Placement"
                                                        "(transformation"
                                                        "(extent={{-122," 
                                                        + str(inpY1) + "},"
                                                        "{-100,"+ str(inpY2) 
                                                        + "}})))")
                    if (causality=="output"):
                        outY1 = outY1 - outCnt*outdel
                        outY2 = outY2 - outCnt*outdel
                        outCnt+=1
                        outputVariableNames.append(name)
                        scalarVariable["annotation"] = (" annotation"
                                                        "(Placement"
                                                        "(transformation"
                                                        "(extent={{100," 
                                                        + str(outY1) + "},"
                                                        "{120," + str(outY2) 
                                                        + "}})))")
                    if (causality=="parameter"):
                        parameterVariableNames.append(name)
                        parameterVariableValues.append(start)
                    scalarVariable["vartype"] = vartype
                    scalarVariable["unit"] = unit
                    if not (start is None):
                        scalarVariable["start"] = start
                    scalarVariables.append(scalarVariable)
            # Print list with all scalar variables        
            # Write success.
            log.info("Parsing of " + self.xml_path + " was successfull.")        
            return scalarVariables, inputVariableNames, \
                outputVariableNames, parameterVariableNames, \
                parameterVariableValues
            
    
    def print_mo(self):
        """Print the Modelica model of a CYMDIST XML file.
        
        This function parses a CYMDIST XML file and extract 
        the variables attributes needed to write the CYMDIST 
        Modelica model. It then writes the Modelica model.
        The name of the Modelica model is the modelName in the 
        model description file. This is used to avoid
        name conflicts when generating multiple CYMDIST models.
        
        """
        
        self.xml_validator()
        scalarVariables, inputVariableNames, \
        outputVariableNames, parameterVariableNames, \
        parameterVariableValues = self.xml_parser()

        loader = jja2.FileSystemLoader(CYMDISTModelicaTemplate_MO)
        env = jja2.Environment(loader=loader)
        template = env.get_template('')
                
        # Call template with parameters
        output_res=template.render(modelName= self.modelName,
                        inputFilePath=self.input_file_path,
                        scalarVariables=scalarVariables, 
                        inputVariableNames=inputVariableNames,
                        outputVariableNames=outputVariableNames,
                        parameterVariableNames=parameterVariableNames,
                        parameterVariableValues=parameterVariableValues)
        # Write results in mo file which has the same name as the class name
        output_file = self.modelName + ".mo"
        if path.isfile(output_file):
            log.warning("The output file " + output_file 
                        + " exists and will be overwritten.")
        with open(output_file, "wb") as fh:
            fh.write(output_res)
        fh.close()  

        # Write success.
        log.info("The Modelica model " + output_file + 
                 " of " + self.modelName + " is successfully created.")
        log.info("The Modelica model " + output_file + 
                 " of " + self.modelName + " is in " + os.getcwd())
    
    
    def generate_fmu(self):
        """Generate the CYMDIST FMU.
        
        This function writes the mos file which is used to create the 
        CYMDIST FMU. The function requires the path to the Buildings 
        library which will be set to the MODELICAPATH.
        The function calls Dymola to run the mos file and 
        write a CYMDIST FMU. The CYMDIST FMU cannot be used yet
        as Dymola does not support the export of FMUs which 
        has the needsExecutionTool set to true. 
        
        """
        
        # Set the Modelica path to point to the Buildings Library
        os.environ["MODELICAPATH"] = self.buildings_path 
        
        # Load the mos template to create the FMU
        loader = jja2.FileSystemLoader(CYMDISTModelicaTemplate_MOS)
        env = jja2.Environment(loader=loader)
        template = env.get_template('')
        
        output_res=template.render(modelName= self.modelName, 
                                   buildingsPath=self.buildings_path)
        # Write results in mo file which has the same name as the class name
        output_file = self.modelName + ".mos"
        if path.isfile(output_file):
            log.warning("The output file " + output_file 
                        + " exists and will be overwritten.")
        with open(output_file, "wb") as fh:
            fh.write(output_res)
        fh.close()  
        
        # Call Dymola to generate the FMUs
        sp.call(["dymola", output_file]) 
        
        # Define name of the FMU
        fmuName = self.modelName + ".fmu"
        
        # Write scuccess.
        log.info("The FMU " + fmuName + " is successfully created.")
        log.info("The FMU " + fmuName  + " is in " + os.getcwd() + ".")
        
    
    def clean_temporary(self):
        temporary = ["buildlog.txt", "dsin.txt", "dslog.txt", "dymosim", 
                     "request.", "status.", "dsmodel.c", 
                     "dsmodel_fmuconf.h", "fmiModelIdentifier.h"]
        for fil in temporary:
            if path.isfile(fil):
                os.remove(fil)
        # FMU folders generated by Dymola.
        DymFMU_tmp= ["~FMUOutput", ".FMUOutput"]
        for fol in DymFMU_tmp:
            if path.isdir(fol):
                shutil.rmtree(fol)
                
             
    def rewrite_fmu(self):
        """Add needsExecutionTool to the CYMDIST FMU.
        
        This function unzips the FMU generated with generate_fmu(),
        reads the xml file and add needsExecutionTool to the FMU capabilities.
        The function completes the process by re-zipping the FMU.
        The new FMU contains the modified XML file as well as the binaries.
        
        """
        
        # Get the XML file
        
        dir = self.modelName + ".tmp"
        zipdir = dir + ".zip"
        fmuName=self.modelName + ".fmu"
        
        if path.exists(dir):
            shutil.rmtree(dir)
            
        if not path.exists(dir):
            os.makedirs(dir)
        
        # Copy file to temporary folder    
        shutil.copy2(fmuName, dir)
        
        # Get the current working directory
        cwd = os.getcwd()
        
        # Change to the temporary directory
        os.chdir(dir)
        
        # Unzip folder which contains he FMU
        zip_ref = zipfile.ZipFile(fmuName, 'r')
        zip_ref.extractall(".")
        zip_ref.close()
           
        log.info("The model description file will be rewritten" +
                 " to include the attribute " + NEEDSEXECUTIONTOOL + 
                 " set to true.")
        tree = ET.parse(MODELDESCRIPTION)
        # Get the root of the tree
        root = tree.getroot()  
        # Add the needsExecution tool attribute
        root.attrib[NEEDSEXECUTIONTOOL] = "true"
        tree.write(MODELDESCRIPTION, xml_declaration=True)
        if path.isfile(fmuName):
            os.remove(fmuName)
        
        # Switch back to the current working directory
        os.chdir(cwd)
        
        # Pass the directory which will be zipped
        # and call the zipper function.
        zip_fmu(dir, includeDirInZip=False)
        
        # Check if fmuName exists in current directory
        # If that is the case, delete it or rename to tmp?
        fmuNameOriginal = fmuName + ".original"
        if path.isfile(fmuName):
            log.info("The original CYMDIST FMU " + fmuName + 
                     " will be renamed to " + fmuName+".original.")
            log.info ("A modified version of the original will be created.")
            log.info("The difference between the original and the new FMU lies"
                     " in the model description file of the new FMU which has"
                     " the attribute " + NEEDSEXECUTIONTOOL + " set to true.")
            if path.isfile(fmuNameOriginal):
                os.remove(fmuNameOriginal)
            os.rename(fmuName, fmuNameOriginal)
        
        # Rename the FMU name to be the name of the FMU
        # which will be used for the simulation. This FMU
        # contains the needsExecutionTool flag.
        os.rename(zipdir, fmuName)
        
        # Delete temporary folder 
        shutil.rmtree(dir)
        
        # Write scuccess.
        log.info("The FMU " + fmuName + " is successfully re-created.")
        log.info("The FMU " + fmuName  + " is in " + os.getcwd() + ".")
        

if __name__ == '__main__':
    # Try running this module!
    main()
    
