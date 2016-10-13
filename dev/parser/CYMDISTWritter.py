'''
Created on Oct 7, 2016

@author: Thierry S. Nouidui
'''
from lxml import etree
import xml.etree.ElementTree as ET
import jinja2
import json
import os.path
import logging

logging.basicConfig(filename="CYMDIST.log",  filemode='w', level=logging.DEBUG, format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')
stderrLogger=logging.StreamHandler()
stderrLogger.setFormatter(logging.Formatter(logging.BASIC_FORMAT))
logging.getLogger().addHandler(stderrLogger)

# The Path to the xsd document. 
# This shouldn't be changed by the user.
XSD_PATH = "./CYMDISTModelDescription.xsd"

      
def main():
        
    """Illustrate how to write Modelica model for CYMDIST.
    
    
    """
    
    CYMDIST = CYMDISTWritter("CYMDISTModelDescription.xml")
    CYMDIST.print_mo()

class CYMDISTWritter(object):
    
    """CYMDIST FMU writer.
    
    This class contains various methods to
    read and XML file, validate it against 
    a pre-defined XML schema, extracting the
    variables attributes, writing a Modelica
    model of a CYMDIST model and exporting
    the model as an FMU for model exchange 2.0.
    
    """


    def __init__(self, xml_path):
        """Initialize the class.
        
        Args:
            xml_path (str): The path to the XML file.
        
        """
        
        self.xml_path = xml_path
              
             
    def xml_validator(self):
        """Validate the XML file.
        
        This function validates the XML file 
        against CYMDISTModelDescription.xsd.
        
        """
        
        try:
            # Get the XML schema to validate against
            xmlschema = etree.XMLSchema(file=XSD_PATH)
            # Parse string of XML
            xml_doc = etree.parse(self.xml_path)
            # Validate parsed XML against schema
            xmlschema.assertValid(xml_doc)
            # Validate parsed XML against schema returning 
            # boolean value indicating success/failure
            result = xmlschema.validate(xml_doc)
            if result:
                logging.info(self.xml_path + " is a Valid XML document.")
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
        inputVariables = []
        outputVariables = []
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
                        inputVariables.append(name)
                    if (causality=="output"):
                        outputVariables.append(name)
                    scalarVariable["vartype"] = vartype
                    scalarVariable["unit"] = unit
                    if not (start is None):
                        scalarVariable["start"] = start
                    # This assumes that we are only dealing with Integers
                    # This is because of the start value which is set to 0.0.
                    else:
                        if (causality=="input"):
                            print "Start value is not defined.\
                              The start value is set to 0.0"
                            scalarVariable["start"] = 0.0
                    scalarVariables.append(scalarVariable)
            # Print list with all scalar variables                
            return scalarVariables, inputVariables, outputVariables
        
        
    
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
        scalarVariables, inputVariables, outputVariables = self.xml_parser()

        loader = jinja2.FileSystemLoader('./CYMDISTModelicaTemplate.mot')
        env = jinja2.Environment(loader=loader)
        template = env.get_template('')
        # I needed to send two input(output)Variables because of Python formating of 
        # strings. Python uses single quotes rather than double quotes for strings. 
        # Using single quotes will generate an invalid Modelica model. So the json.dumps
        # is used to create a vector of strings which can be used in Modelica.
        # The second vector is used to write the equations in Modelica using jinja2.
        # A single vector cannot be used for both as a json.dumps convert a strings
        # to a set of single characters which can not longer be iterated over.
        output_res=template.render(modelName= self.modelName,
                        parent_dict=scalarVariables, 
                         modelicaInputVariables = json.dumps(inputVariables), 
                         inputVariables=inputVariables,
                         modelicaOutputVariables = json.dumps(outputVariables), 
                         outputVariables=outputVariables)
        # Write results in mo file which has the same name as the class name
        output_file = self.modelName+".mo"
        if os.path.isfile(output_file):
            logging.warning("The output file " + output_file 
                            + " exists and will be overwritten.")
        with open(output_file, "wb") as fh:
            fh.write(output_res)
        fh.close()    

        
if __name__ == '__main__':
    # Try running this module!
    main()
    
