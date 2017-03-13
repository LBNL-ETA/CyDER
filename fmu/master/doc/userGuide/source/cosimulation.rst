.. highlight:: rest

.. _cosimulation:


Co-simulation
=============

This section explains how to link a CYMDIST FMU with another FMU for co-simulation.
In this section, we used the GridDyn FMU for the simulation coupling.

The following code snippet shows how to import and link a CYMDIST FMU (``CYMDIST.FMU``) with a
GridDyn FMU (``GridDyn.fmu``).

Line 1 and 2 import the :term:`PyFMI` modules which are needed for the coupling.

Line 8 loads the CYMDIST FMU 

Line 9 loads the GridDyn FMU

Line 11 defines a vector with the CYMDIST and the GridDyn FMUs models.

Line 12 defines the connections between the CYMDIST and the GridDyn FMUs
``(gridyn, "VMAG_A", cymdist, "VMAG_A")`` means that the output ``VMAG_A``
of the GridDyn FMU is connected to the input ``VMAG_A`` of the CYMDIST FMU.

Line 25 passes the FMUs models and their connection to the master algorithm.

Line 27 gets the simulation option object.

Line 28 sets the communication step size.

Line 29 sets the logging to true.

Line 31 invokes the function which is used to simulate the coupled models.
 
.. literalinclude:: scripts/coupling.py
   :language: python
   :linenos:


