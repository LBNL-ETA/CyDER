.. highlight:: rest

.. _bestPractice:


Best Practice
=============

This section explains to users the best practice in configuring a CYMDIST XML input file 
for an FMU. 

To export CYMDIST as an FMU, the user needs to write an XML file which contains the list 
of inputs, outputs and parameters of the FMU. The XML snippet below shows how a user has to write such an input file.
A template named ``CYMDISTModeldescritpion.xml`` which shows such a file is provided in the ``parser\utilities`` installation folder of CYMDISTPy. 
This template should be used and modify to create new XML input file.

The following snippet shows an input file where the user defines one input and one output variable.

.. literalinclude:: models/example.xml
   :language: xml
   :linenos:

To create such an input file, the user needs to specify the name of the FMU (Line 5). 
This is the ``modelName`` which should be unique.
The user then needs to define the inputs and outputs of the FMUs. 
This is done by adding ``ScalarVariable`` into the list of ``ModelVariables``.

To parametrize the ``ScalarVariable`` as an input variable, the user needs to

  - define the name of the variable (Line 10), 
  - give a brief description of the variable (Line 11)
  - give the causality of the variable (``input`` for inputs, ``output`` for outputs) (Line 12)
  - define the type of variable (Currently only ``Real`` variables are supported) (Line 13)
  - give the unit of the variable (Currently only valid Modelica units are supported) (Line 14)
  - give a start value for the input variable (This is optional) (Line 15)

To parametrize the ``ScalarVariable`` as an output variable, the user needs to

  - define the name of the variable (Line 18), 
  - give a brief description of the variable (Line 19)
  - give the causality of the variable (``input`` for inputs, ``output`` for outputs) (Line 20)
  - define the type of variable (Currently only ``Real`` variables are supported) (Line 21)
  - give the unit of the variable (Currently only valid Modelica units are supported) (Line 22)
  - give the name of the output device (Line 24)
   
.. note:: 
   
     To avoid name-clash, CYMDISTPy concatenates the name of the output with the name of 
     the device to make it unique. The new output name will have the form ``outputName_DeviceName``.
