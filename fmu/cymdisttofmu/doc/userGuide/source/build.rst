.. highlight:: rest

.. _build:

Creating an FMU
===============

This chapter describes how to create a Functional Mockup Unit, starting from a CYMDIST XML input file.
It assumes you have followed the :doc:`installation` instructions, and that you have created the CYMDIST 
model description file  following the :doc:`bestPractice` guidelines.


Command-line use
^^^^^^^^^^^^^^^^

.. automodule:: parser.CYMDISTToFMU

Output of CYMDISTToFMU
^^^^^^^^^^^^^^^^^^^^^^

The main output from running ``CYMDISTToFMU.py`` consists of an FMU, named after the ``modelName`` specified in the input file.
The FMU is written to the current working directory, that is, in the directory from which you entered the command.

The FMU is complete and self-contained.
Any secondary output from running the CYMDISTToFMU tools can be deleted safely.

Note that the FMU is a zip file.
This means you can open and inspect its contents.
To do so, it may help to change the "``.fmu``" extension to "``.zip``".
