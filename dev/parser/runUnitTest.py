#!/usr/bin/env python
#######################################################
# Script with unit tests for CyDER
#
# TSNouidui@lbl.gov                            2016-09-06
#######################################################
import unittest
import platform
import CYMDISTWritter as cymwritter

#########################################
# # TEST FILES TO BE PROVIDED BY THE USER
if platform.system() == 'Linux':
    # Buildings path on the Linux Desktop 
    BUILDINGS_PATH = "/home/thierry/Desktop/vmWareLinux/proj/buildings_library/models/modelica/git/buildings/modelica-buildings"
else:
    # Buildings path on the Windows Notebook 
    BUILDINGS_PATH = "Z:\\thierry\\proj\\buildings_library\\models\\modelica\\git\master\\modelica-buildings"
    # Buildings path on the Windows Desktop 
    # BUILDINGS_PATH="Z:\\Ubuntu\proj\\buildings_library\\models\\modelica\\git\\buildings\\modelica-buildings"

XML_INPUT_PATH = "./CYMDISTModelDescription.xml"
INPUT_FILE_PATH = "./CYMDIST.inp"

REF_DATA_CYMDIST_MO = '''  Real yR[nDblOut]={
  y_dev1,
  y1_dev1 
  }"Variable used to collect values received from CYMDIST";
'''  

CYMDIST_T = cymwritter.CYMDISTWritter(INPUT_FILE_PATH, XML_INPUT_PATH, BUILDINGS_PATH, 0)

class Tester(unittest.TestCase):
    ''' Class that runs all regression tests.
    '''

    def test_check_duplicates(self):
        '''  Test the function check_duplicates().
        
        '''
        
        # Array does not contain duplicates variables.
        cymwritter.check_duplicates(["x1", "x2", "x3", "x4"])
        
        # Array contain duplicates variables.
        with self.assertRaises(AssertionError):
            cymwritter.check_duplicates(["x1", "x1", "x3", "x4"])

    def test_sanitize_name(self):
        '''  Test the function sanitize_name().
        
        '''
        
        # Testing name conversions.
        name=cymwritter.sanitize_name("test+name")
        self.assertEquals(name, "test_name", "Names are not matching.")
        
        name=cymwritter.sanitize_name("0test+*.name")
        self.assertEquals(name, "f_0test___name", "Names are not matching.")


    def test_xml_validator(self):
        '''  Test the function xml_validator().
        
        '''
        
        # Testing validation of xml file
        CYMDIST_T.xml_validator()
        
    def test_xml_parser(self):
        '''  Test the function xml_validator().
        
        '''
        
        # Testing validation of xml file
        CYMDIST_T.xml_parser()


    def test_print_mo(self):
        '''  Test the function print_mo().
        
        '''
        
        # Testing function to print Modelica model.
        CYMDIST_T.print_mo()
        
        # load Modelica generated file
        output_file = "CYMDIST.mo"
        with open(output_file, "r") as fh:
            read_data=fh.read()
            ncount = read_data.count(REF_DATA_CYMDIST_MO)                    
        fh.close()  
        assert(ncount==1), "The number of reference data is different from 1."
         

if __name__ == '__main__':
    unittest.main()
