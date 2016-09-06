#!/usr/bin/env python
#######################################################
# Script with unit tests for CyDER
#
# TSNouidui@lbl.gov                            2016-09-06
#######################################################
import unittest
import os, sys;
import logging
from subprocess import call

class Tester(unittest.TestCase):
    ''' Class that runs all regression tests.
    '''

    def test_fmucheker_cyder_fmus(self):
        '''  Detect the operating system,
        switch to the folder which contains FMUs
        with correct binaries, call the fmuChecker 
        to run the FMUs with default settings.
        To run the test, the user must make sure
        that the fmuChecker executables are in the 
        fmuChekcker folders. These executables
        can be obtained from the fmi-standard 
        svn repository.

        '''
        # Log file with logging messages.
        LOG_FILENAME = 'cyder_fmus.log'
        # Set basic configuration.
        logging.basicConfig(filename=LOG_FILENAME,level=logging.INFO)
        # To stream the logging messages to the standard output.
        logging.getLogger().addHandler(logging.StreamHandler())
        # Identify system.
        PLATFORM_NAME = sys.platform
        is_64bits = sys.maxsize > 2**32
        #
        if( PLATFORM_NAME.startswith('win') ):
            if(is_64bits):
                FMU_ARCH="win64"
            else:
                FMU_ARCH="win32"
        elif(PLATFORM_NAME.startswith('linux')):
            if(is_64bits):
                FMU_ARCH="linux64"
            else:
                FMU_ARCH="linux32"
        elif( PLATFORM_NAME.startswith('darwin') ):
            if(is_64bits):
                FMU_ARCH="darwin64"
            else:
                FMU_ARCH="darwin32"
        # Set working directory to the one containing this file.
        abspath = os.path.abspath(__file__);
        dname = os.path.dirname(abspath);
        os.chdir(dname);
        
        # Get the path to the FMUs.
        # This directory depends on the 
        # operating system architecture.
        fmus_dir = os.path.join("..", "fmus", FMU_ARCH)
        
        # define number of FMUs
        n_fmus=0
        
        # Set the path to the fmuChecker 
        fmu_checker = os.path.join("..", "fmuChecker", "fmuCheck." + FMU_ARCH)
        
        # Walk through the directories and run unit tests for all found FMUs.
        for root, dirs, files in os.walk(fmus_dir):
            for fil in files:
                if fil.endswith(".fmu"):
                    n_fmus=n_fmus+1;
                    logging.info("Found FMU: " + str(fil) + " in directory: " + str (root))
                    # Get the path to the FMU
                    fmu_path = os.path.join(root, fil)
                    # Call and execute the fmuChecker
                    logging.info("Run the fmuChecker for FMU: " + str(fil))
                    call([fmu_checker, fmu_path])
                    
        # Report the number of FMUs checked
        if (n_fmus!=0):           
            logging.info("Ran fmuChecker for " + str (n_fmus) + " FMU(s).")
        else:
            logging.warning ("There is no FMU to check in the FMU folder.")
        
        # Assert if the number of successful runs is less than one
        self.assertTrue(n_fmus > 0)

if __name__ == '__main__':
    unittest.main()
