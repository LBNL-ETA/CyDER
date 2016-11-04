.. highlight:: rest

.. _usage:

Usage of CYMDIST as an FMU
=============================

The following items need to be observed when importing an FMU that contains CYMDIST:

1. The Python 3.4 interpreter must be installed.

2. A ``PYTHONPATH`` variable must be created in the System environment variables.

3. Following folders must be added to the ``PYTHONPATH``:

   - ``dev/cymdist``: This folder contains the python functions which allows to communicate with CYMDIST. The folder is available in the distribution of CYMDISTPy.
   - ``path-to-cympy``: This folder contains the CYMDIST API functions and are installed with the distribution of CYMDIST (e.g. ``C:\Program Files (x86)\CYME\CYME)``.





