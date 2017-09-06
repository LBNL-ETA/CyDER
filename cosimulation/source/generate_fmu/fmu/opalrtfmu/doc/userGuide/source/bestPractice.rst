.. highlight:: rest

.. _bestPractice:


OPAL-RT FMU 
===========

This section explains how to export the OPAL-RT real-time simulator as an FMU.


To export the OPAL-RT real-time simulator as an FMU, 

1. edit the XML file provided by SimulatortoFMU which contains the list 
 of inputs, outputs of the FMU. The XML template named ``SimulatorModeldescritpion.xml`` 
 is provided in the ``opalrtfmu/utilities``. 
 
2. run the ``SimulatorToFMU.py`` to create the OPAL-RT FMU with

  .. code-block:: none

    # Windows:
    > python parser\\SimulatorToFMU.py -s opalrtfmu\\utilities\\simulator_wrapper.py

.. note::
	
   The configuration of the OPAL-RT FMU is a file with the extension ``.llp`` which specifies the location of the 
   the location of the  OPAL-RT simulink model as well. Examples of such files can be found in the Examples folders
   of RT-LAB. 
   The path to the configuration file will be either set by the master algorithm which imports the 
   OPAL-RT FMU, or provided as ``-c`` argument for SimulatorToFMU.py. See the user guide of SimulatorToFMU
   for a list of arguments of SimulatorToFMU.  

   To use the FMU, the content of the ``.binaries.zip`` and the ``.scripts.zip`` folders need to be 
   added to the PATH and the PYTHONPATH as described in the SimulatorToFMU user guide.
