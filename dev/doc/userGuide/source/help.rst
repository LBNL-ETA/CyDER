Help
====

Installing PyFMI for Python 3.4 32 bit
--------------------------------------
:term:`PyFMI` is a python package which can be used to import and run a CYMDIST FMU. In :term:`PyFMI` version 2.3.1, a master algorithm was added to import and 
link multiple FMUs for co-simulation. At time of writing, there was no :term:`PyFMI` 2.3.1 executable available for Python 3.4 on Windows 32bit (See `PyPyi <https://pypi.python.org/pypi/PyFMI>`_.).
The next steps describe requirments and steps to perform to compile :term:`PyFMI` version 2.3.1 from source.

.. note::
  
  To avoid having to recompile :term:`PyFMI` dependent libraries from source, 
  we recommend to use pre-compiled Windows binaries whenever available.

Requirements
++++++++++++

**Python 3.4** 

.. note::
  
  The 32 bit Windows version of Python 3.4 must be used.

**FMI Library**

.. note::
  
  We tested version 2.0.2 which had a 32 bit Windows version at `JModelica.org <http://www.jmodelica.org/FMILibrary>`_.

**Cython**

.. note::

  We tested the version currently available at `PyPyi <https://pypi.python.org/pypi>`_. 

**Numpy**

.. note::

  We tested the version currently available at `PyPyi <https://pypi.python.org/pypi>`_. 

**Scipy**

.. note::
  
  We tested version 0.16.1 which had a 32 bit Windows installer for Python 3.4 at `sourceforge <https://sourceforge.net/projects/scipy/files/scipy/0.16.1/>`_. 

**lxml**

.. note::
  
  We tested version 3.4.4 which had a 32 bit Windows installer for Python 3.4 at `PyPyi <https://pypi.python.org/pypi/lxml/3.4.4>`_. 

**Assimulo**

.. note::
  
  We tested version 2.7b1 which had a 32 bit Windows installer for Python 3.4 at `PyPyi <https://pypi.python.org/pypi/Assimulo/2.7b1>`_. 

**matplotlib**

.. note::
  
  We tested version 1.4.3 which had a 32 bit Windows installer for Python 3.4 at `PyPyi <https://pypi.python.org/pypi/matplotlib/1.4.3>`_. 

**pyparsing**

.. note::

  We tested the version currently available on PyPi.

**C-Compiler**

.. note::

  We tested the C-compiler provided in Visual Studio 2010 Professional.

:term:`PyFMI` **source**

.. note::

  We used version 2.3.1 which includes a master algorithm for FMUs.

Compilation
+++++++++++

To compile :term:`PyFMI` from source, run

.. code-block:: none

  python setup.py install –fmil-home=/path/to/FMI_Library/

where ``/path/to/FMI_Library/`` is the path to the FMI library.



