.. highlight:: rest

.. _installation:

Installation and Configuration
==============================

This chapter describes how to install, configure and uninstall CYMDISTToFMU.


Software requirements
^^^^^^^^^^^^^^^^^^^^^

To export CYMDIST as an FMU, CYMDISTToFMU needs:

1. Python and following dependencies:

   - jinja2 

   - lxml 

2. Modelica parser

3. C-Compiler

CYMDISTToFMU has been tested with:

  - Python 2.7.13 and 3.5.0 
  - Three Modelica parsers

    - Dymola 2017 FD01 on Windows and Linux
    - JModelica 2.0 on Windows, and JModelica trunk version 9899 on Linux
    - OpenModelica 1.11.0 on Windows

  - C-Compiler: Microsoft Visual Studio 10 Professional

.. note:: 

   CYMDISTToFMU can use OpenModelica and Dymola to export CYMDIST as an FMU. 
   However OpenModelica 1.11.0 (on Windows) and Dymola 2017 FD01 (on Linux) do not copy all required libraries dependencies to the FMU.
   As a workaround, CYMDISTToFMU checks if there are missing libraries dependencies and copies the dependencies to the FMU.

.. _installation directory:

Installation
^^^^^^^^^^^^

To install CYMDISTToFMU, proceed as follows:

1. Add following folders to your system path: 

 - Python installation folder (e.g. ``C:\Python34``)
 - Python scripts folder (e.g. ``C:\Python34\Scripts``), 
 - Dymola executable folder (e.g. ``C:\Program Files(x86)\Dymola2017 FD01\bin``)
 - JModelica installation folder (e.g. ``C:\JModelica.org-2.0``)
 - OpenModelica executable folder (e.g. ``C:\OpenModelica1.11.0-32bit\bin``)

   
 You can add folders to your system path by performing following steps on Windows 8 or 10:

 - In Search, search for and then select: System (Control Panel)
     
 - Click the Advanced system settings link.
     
 - Click Environment Variables. In the section System Variables, find the PATH environment variable and select it. Click Edit. 
     
 - In the Edit System Variable (or New System Variable) window, specify the value of the PATH environment variable (e.g. ``C:\Python34``, ``C:\Python34\Scripts``). Click OK. Close all remaining windows by clicking OK.
     
 - Reopen Command prompt window for your changes to be active.
    
 To check if the variables have been correctly added to the system path, type ``python``, ``dymola``, ``pylab``, or ``omc``
 into a command prompt to see if the right version of Python, Dymola, JModelica, or OpenModelica starts up.

.. note:: 

   To avoid adding Dymola, JModelica, or OpenModelica to the system path, provide the path
   to the executables to CYMDISTToFMU.py. See :ref:`build_cmd` for the lists of arguments 
   of CYMDISTToFMU.

2. To install CYMDISTToFMU, run 

  .. code-block:: none

    > pip install CYMDISTToFMU
 
  The installation directory should contain the following subdirectories:

    - ``bin/``
      (Python scripts for running unit tests)

    - ``doc/``
      (Documentation)

    - ``fmus/``
      (FMUs folder)

    - ``parser/``
      (Python scripts, Modelica templates and XML validator files)


Uninstallation
^^^^^^^^^^^^^^

To uninstall CYMDISTToFMU, run

.. code-block:: none

    > pip uninstall CYMDISTToFMU
