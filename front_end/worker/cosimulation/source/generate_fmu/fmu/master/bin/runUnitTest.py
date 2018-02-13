#!/usr/bin/env python
#######################################################
# Script with unit tests for the master algorithm CyDER
#
# TSNouidui@lbl.gov                          2016-09-06
#######################################################
import unittest
import os
import sys
import logging
from subprocess import call
import os

# Get path to the bin folder
script_path = os.path.dirname(os.path.realpath(__file__))
master_path = os.path.abspath(os.path.join(script_path, '..', 'pyfmi'))
sys.path.append(master_path)

# Get the current working directory
cwd = os.getcwd()

# Change to the master/pyfmi directory
os.chdir(master_path)

import coupling as master

class Tester(unittest.TestCase):
    ''' Class that runs all regression tests.
    '''

    def test_simulate_algebraicloop_fmus(self):
        '''  Test the function simulate_algebraicloop_fmus().

        '''

        # Array does not contain duplicates variables.
        master.simulate_algebraicloop_fmus()
    
    def test_simulate_two_griddyn14bus_fmu(self):
        '''  Test the function check_duplicates().

        '''

        # Array does not contain duplicates variables.
        master.simulate_two_griddyn14bus_fmu()
        
    def test_simulate_one_cymdist_fmu(self):
        '''  Test the function simulate_one_cymdist_fmu().

        '''

        # Array does not contain duplicates variables.
        master.simulate_one_cymdist_fmu()

    def test_simulate_one_griddyn14bus_fmus(self):
        '''  Test the function simulate_one_griddyn14bus_fmus().

        '''

        # Array does not contain duplicates variables.
        master.simulate_one_griddyn14bus_fmus()
        
    def test_simulate_cymdist_griddyn14bus_fmus(self):
        '''  Test the function simulate_cymdist_griddyn14bus_fmus().

        '''

        # Array does not contain duplicates variables.
        master.simulate_cymdist_griddyn14bus_fmus()


if __name__ == '__main__':
    unittest.main()
    os.chdir(cwd)
