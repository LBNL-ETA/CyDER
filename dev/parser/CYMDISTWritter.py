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
# CYMDISTModelicaTemplate_MOT: Template used to write Modelica model
# CYMDISTModelicaTemplate_MOS: Template used to write mos script
XSD_SCHEMA = "./CYMDISTModelDescription.xsd"
CYMDISTModelicaTemplate_MOT="CYMDISTModelicaTemplate.mot"
CYMDISTModelicaTemplate_MOS="CYMDISTModelicaTemplate.mos"
#########################################
## TEST FILES TO BE PROVIDED BY THE USER
if platform.system()=='Linux':
    BUILDINGS_PATH="/home/thierry/Desktop/vmWareLinux/proj/buildings_library/models/modelica/git/buildings/modelica-buildings"
else:
    BUILDINGS_PATH="Z:\\Ubuntu\proj\\buildings_library\\models\\modelica\\git\\buildings\\modelica-buildings"
XML_INPUT_PATH="CYMDISTModelDescription.xml"
######################################### 
      
def main():
        
    """Illustrate how to write Modelica model for CYMDIST.
    
    
    """
    
    CYMDIST = CYMDISTWritter(XML_INPUT_PATH, BUILDINGS_PATH)
    CYMDIST.print_mo()
    CYMDIST.generate_fmu()

class CYMDISTWritter(object):
    
    """CYMDIST FMU writer.
    
    This class contains various methods to
    read and XML file, validate it against 
    a pre-defined XML schema, extracting the
    variables attributes, writing a Modelica
    model of a CYMDIST model and exporting
    the model as an FMU for model exchange 2.0.
    
    """


    def __init__(self, xml_path, buildings_path):
        """Initialize the class.
        
        Args:
            xml_path (str): The path to the XML file.
            buildings_path (str): The path to the folder
            which contains the Buildings library excluding 
            the ending FILE SEPARATOR.
        
        """
        
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
                log.info(self.xml_path + " is a Valid XML document.")
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
        
        This function parses the XML file and extract 
        the variables attributes needed to write the 
        Modelica model.
        
        """
        
        # Get the XML file
        tree = ET.parse(self.xml_path)
        # Get the root of the tree
        root = tree.getroot()  
        
        # Get the FMI Version for checking
        fmiVersion = root.attrib.get("fmiVersion")
        # Get the model name to write the .mo file 
        self.modelName = root.attrib.get("modelName")
        
        assert (not(fmiVersion is "2.0")), "The FMI version 2.0 \
            is the only version currently supported."
  
        # Iterate through the XML file and get the ModelVariables.
        inputVariableNames = []
        outputVariableNames = []
        parameterVariableValues = []
        parameterVariableNames = []
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
                        print "Start value of variable " + name + \
                        " with causality" + causality + " not defined.\
                        The start value will be set to 0.0 by default."
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
                    if (causality=="output"):
                        outputVariableNames.append(name)
                    if (causality=="parameter"):
                        parameterVariableNames.append(name)
                        parameterVariableValues.append(start)
                    scalarVariable["vartype"] = vartype
                    scalarVariable["unit"] = unit
                    if not (start is None):
                        scalarVariable["start"] = start
                    scalarVariables.append(scalarVariable)
            # Print list with all scalar variables                
            return scalarVariables, inputVariableNames, \
                outputVariableNames, parameterVariableNames, \
                parameterVariableValues
            
    
    def print_mo(self):
        """Print the Modelica model of CYMDIST from the XML file.
        
        This function parses the XML file and extract 
        the variables attributes needed to write the 
        Modelica model. It then writes the Modelica model.
        The name of the Modelica model is the modelName in the 
        model description file. This is used to avoid
        name conflicts when generating multiple CYMDIST models.
        
        """
        
        self.xml_validator()
        scalarVariables, inputVariableNames, \
        outputVariableNames, parameterVariableNames, \
        parameterVariableValues = self.xml_parser()

        loader = jja2.FileSystemLoader(CYMDISTModelicaTemplate_MOT)
        env = jja2.Environment(loader=loader)
        template = env.get_template('')
        
        output_res=template.render(modelName= self.modelName,
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
        
    
    def generate_fmu(self):
        """Generate the CYMDIST FMU.
        
        This function writes the mos file which is used to create the 
        CYMDIST FMU. It requires the path to the Buildings 
        library which will be set to the MODELICAPATH.
        The function calls Dymola, runs the mos file and 
        writes an FMU according to the parameters set in the mos template.
        
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
      
        
        
if __name__ == '__main__':
    # Try running this module!
    main()
    
