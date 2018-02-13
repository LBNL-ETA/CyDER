.. highlight:: rest

.. _bestPractice:


OPAL-RT FMU 
===========

This section explains how to export the RT-LAB API of OPAL-RT as an FMU.


To export the Python RT-LAB API, 

1. edit the XML template ``SimulatorModeldescritpion.xml`` provided 
   in the ``utilities`` of the distribution of ``SimulatorToFMU`` 
    to specify the inputs, and outputs of the FMU. 
 
2. run ``SimulatorToFMU.py`` to create the RT-LAB API FMU with

  .. code-block:: none

    # Windows:
    > python parser\\SimulatorToFMU.py -s opalrtfmu\\utilities\\simulator_wrapper.py

.. note::
	
   To use the FMU, the path to the configuration file of OPAL-RT will be set in the FMU.
   This file has the extension ``.llp`` and specifies the location of the  
   OPAL-RT simulink grid model. Examples of such files can be found in the xamples folders
   of RT-LAB. 
   The path to the configuration file will be either set by the master algorithm which imports the 
   RT-LAB API FMU, or provided as ``-c`` argument for SimulatorToFMU.py. See the user guide of SimulatorToFMU
   for a list of arguments of SimulatorToFMU.  

   To use the FMU, the content of the ``.binaries.zip`` and the ``.scripts.zip`` folders need to be 
   added to the PATH and the PYTHONPATH as described in the SimulatorToFMU user guide.
