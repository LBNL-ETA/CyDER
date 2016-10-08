'''
Created on Oct 7, 2016

@author: Thierry S. Nouidui
'''
from lxml import etree
import xml.etree.ElementTree as ET

# The Path to the xsd document. 
# This shouldn't be changed by the user.
XSD_PATH = "CYMDISTModelDescription.xsd"


      
def main():
        
    """Illustrate how to parse an XML file.
    
    
    """
    
    cymdist = CYMDISTWritter("CYMDISTModelDescription.xml")
    cymdist.xml_validator()
    cymdist.xml_parser()

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
                print self.xml_path + " is a Valid XML document."
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
                print 'filename: ' + error.filename  # '<string>' cos var is a string of xml
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
        assert (not(fmiVersion is '2.0')), "The FMI version 2.0 \
            is the only version currently supported."
  
        # Iterate through the XML file and get the ModelVariables.
        for child in root.iter('ModelVariables'):
            # print(child.tag, child.attrib)
            for element in child:
                # Iterate through ScalarVariables and get attributes
                (name, description, causality) = element.attrib.get('name'), \
                    element.attrib.get('description'), element.attrib.get('causality')
                # Iterate through children of ScalarVariables and get attributes
                for subelement in element:
                    vartype = subelement.tag
                    unit = subelement.attrib.get("unit")
                    start = subelement.attrib.get("start")
                    print (name, description, causality, vartype, unit, start)
        
        

    
if __name__ == '__main__':
    # Try running this module!
    main()