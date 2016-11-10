Help
====

Running PyFMI with Python 3.4 on Windows 32 bit
-----------------------------------------------
:term:`PyFMI` is a python package which can be used to import and run a CYMDIST FMU. In :term:`PyFMI` version 2.3.1, a master algorithm was added to import and 
link multiple FMUs for co-simulation. At time of writing, there was no :term:`PyFMI` 2.3.1 executable available for Python 3.4 for Windows 32bit (See `PyPyi <https://pypi.python.org/pypi/PyFMI>`_.).
The next steps describe requirments and steps to perform to compile :term:`PyFMI` version 2.3.1 from source.

.. note::
  
  To avoid having to recompile :term:`PyFMI` dependent libraries from source, 
  we recommend to use pre-compiled Windows binaries whenever available.

Requirements
++++++++++++

The next table shows the list of Python modules and softwares used to compile version 2.3.1 of PyFMI from source
so it can run with Python 3.4 on Windows 32 bit.

+---------------+---------------------------------------------+-----------------------------------------------------------+
| Modules       | Version                                     | Link                                                      |
+===============+=============================================+===========================================================+
| Python 3.4    | Windows 32 bit                              | https://www.python.org/ftp/python/3.4.3/python-3.4.3.msi  |
+---------------+---------------------------------------------+-----------------------------------------------------------+
| FMI Library   | 2.0.2                                       | http://www.jmodelica.org/FMILibrary                       |
+---------------+---------------------------------------------+-----------------------------------------------------------+
| Cython        | 0.25.1                                      | https://pypi.python.org/pypi/Cython/0.25.1                |
+---------------+---------------------------------------------+-----------------------------------------------------------+
| Numpy         | 1.11.2                                      | https://pypi.python.org/pypi/numpy/1.11.2                 |
+---------------+---------------------------------------------+-----------------------------------------------------------+
| Scipy         |  0.16.1                                     | https://sourceforge.net/projects/scipy/files/scipy/0.16.1 |
+---------------+---------------------------------------------+-----------------------------------------------------------+
| lxml          | 3.4.4                                       | https://pypi.python.org/pypi/lxml/3.4.4                   |
+---------------+---------------------------------------------+-----------------------------------------------------------+
| Assimulo      | 2.7b1                                       | https://pypi.python.org/pypi/Assimulo/2.7b1               |
+---------------+---------------------------------------------+-----------------------------------------------------------+
| pyparsing     | 2.1.10                                      | https://pypi.python.org/pypi/pyparsing/2.1.10             |
+---------------+---------------------------------------------+-----------------------------------------------------------+
| matplotlib    | 1.4.3                                       | https://pypi.python.org/pypi/matplotlib/1.4.3             |
+---------------+---------------------------------------------+-----------------------------------------------------------+
| C-Compiler    | Microsoft Visual Studio 2010 Pro            |                                                           |
+---------------+---------------------------------------------+-----------------------------------------------------------+
| PyFMI         | 2.3.1 (source)                              | https://pypi.python.org/pypi/PyFMI                        |
+---------------+---------------------------------------------+-----------------------------------------------------------+

Compilation
+++++++++++

To compile :term:`PyFMI` from source, run

.. code-block:: none

  python setup.py install –fmil-home=path_to_FMI_Library/

where ``path_to_FMI_Library/`` is the path to the FMI library.



