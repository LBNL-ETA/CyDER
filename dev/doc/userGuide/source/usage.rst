.. highlight:: rest

.. _usage:

Usage of CYMDIST as an FMU
=============================

The following requirements must be met to import an run FMU that contains CYMDIST:

1. Python 3.4 must be installed.

2. CYME version 7.2 must be installed. CYME can be downloaded from `www.cyme.com <https://www.cyme.com>`_.

3. The CYMDIST Python API scripts directory must be added to the ``PYTHONPATH``.

.. note:: The CYMDIST Python API scripts are in the installation folder of CYME. It can typically be found in 

       ``pathCYME\CYME\cympy``, where ``pathCYME`` is the path to the installation folder of CYME 7.2.

To add the CYMDIST Python API scripts folder to the ``PYTHONPATH``:

     - In Search, search for and then select: System (Control Panel).
     
     - Click the Advanced system settings link.
     
     - Click Environment Variables. In the section System Variables, find a variable named ``PYTHONPATH`` environment variable and select it. If the variable does not exist, create it. Click Edit. 
     
     - In the Edit System Variable (or New System Variable) window, specify the value of the PYTHONPATH environment variable which should in our case be ``pathCYME\CYME``. Note that ``cympy`` is not included in the name of the variable. 
     

4. The ``cymdist`` utility folder must be added to the ``PYTHONPATH``. The ``cymdist`` utility folder can be found in the distribution of CYMDISTPy. It is in ``dev/cymdist``. 
To complete your set-up, add the folder ``dev\cymdist`` to the ``PYTHONPATH``.

5. The Python 3.4 installation folder (e.g. ``C:\Python34`` ) must be added to the ``PYTHONPATH``.






