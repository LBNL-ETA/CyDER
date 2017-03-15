.. highlight:: rest

.. _cosimulation:


Co-simulation
=============

This section explains how to link a CYMDIST FMU with another FMU for co-simulation.
We used the GridDyn FMU for the simulation coupling and explain the problematic caused
by coupling the two tools with the solution implemented in CyDER. 

Coupling GridDyn FMU to CYMDIST creates an algebraic loop that requires an iterative solution. 
Solving this nonlinear system of equations is not likely to be robust, 
because GridDyn and CYMDIST both contain iterative solvers. 
Therefore, the residual function of this algebraic loop will have 
numerical noise which is caused by the embedded iterative solvers. 
To avoid this problem, LLNL proposes to approximate CYMDIST by a polynomial 
and then solve the coupled system of equations that is formed by this polynomial and GridDyn. 
Details about approximating CYMDIST with a polynomial are discussed in the next sections. 
On occasion, this will require that CYMDIST to be called multiple times with varying input, 
but the same state variables, in order to compute its polynomial approximation.

Next, we describe how the system model needs to be configured to allow GridDyn 
to approximate CYMDIST as a polynomial. We consider the case where CYMDIST is coupled to GridDyn. 
For the discussion, we use :math:`p` for parameters (which do not change in time), :math:`u` for inputs, 
which may change in time, :math:`y` for outputs and :math:`t` for time. We will denote with subscript :math:`g` quantities of GridDyn, 
and with subscript :math:`c` quantities of CYMDIST.  We will use :math:`f(·)` to denote a function with unassigned variables. 

Hence, the GridDyn model is of the form

:math:`y_g = f_g(p_g , u_g , t)`,

while the CYMDIST model is of the form

:math:`y_c = f_c(p_c , u_c , t)`.

Note that we make the assumption that both models only take voltage or current as inputs, 
that is, we assume :math:`u_g  = y_c` and :math:`u_c  = y_g`, and the CYMDIST model has no state. 
These models are connected as shown in 
:num:`Figure #fig-couplingwloop`.

.. _fig-couplingwloop:

.. figure:: _img/coupling_w_loop.*
   :scale: 50 %

   Coupling of CYMDIST with GridDyn with algebraic loop.

To implement the computation, these models are encapsulated as FMUs. 
To  approximate CYMDIST as a polynomial, we will need to also propagate parameters :math:`p_g` 
and a connection list that declares the connection between :math:`y_g` and :math:`u_c` and 
between :math:`y_c` and :math:`u_g`. We will call this connection list :math:`p_l`. 
Hence, the CYMDIST FMU needs to be a function of the form

:math:`yc = f_c(p_c , u_c  , t)`,

while the GridDyn FMU is of the form

:math:`yg = f_g(p_g , p_c , p_l , u_g , t)`.

Hence, the GridDyn model needs to take additional parameters the parameters :math:`p_c`  
to parameterize the CYMDIST model, and :math:`p_l` to connect the outputs to the inputs. 
The CYMDIST FMU is an FMU-ME 2.0, because it needs to be evaluated by GridDyn 
without advancing time when approximating it as a polynomial, which is not allowed for FMI-CS 2.0.

As CYMDIST obtains from GridDyn the input :math:`u_c` that corresponds to the solution of the closed loop, 
the FMUs are connected as in :num:`Figure #fig-couplingwoloop`.

.. _fig-couplingwoloop:

.. figure:: _img/coupling_wo_loop.*
   :scale: 70 %

   Coupling of CYMDIST with GridDyn without algebraic loop.

The sequence of evaluations will be as follows: During instantiation, 
both FMUs get their parameters assigned. The GridDyn parameters 
include the parameters for CYMDIST :math:`p_c`  and the output-input 
connection list :math:`p_l`. Then, GridDyn will instantiate a CYMDIST FMU, 
and connect :math:`u_c` to :math:`y_g`. This CYMDIST FMU, which we call :math:`f*_c(·, ·, ·)`, 
will not be visible to the outside. When GridDyn is invoked, it will approximate :math:`f*_c(·, ·, ·)`, 
compute a converged solution using this approximation, and compute the output :math:`y_g`. 
The master algorithm will then assign :math:`u_g  := y_c` and evaluate the FMU :math:`f_g(p_g , p_c , p_l , u_g , t)`, 
which completes the time step.

Next, we showed a snippet of the master algorithm which is used to 
couple a CYMDIST FMU (``CYMDIST.FMU``) with a GridDyn FMU (``GridDyn.fmu``).

Line imports the :term:`PyFMI` modules which is needed for the coupling.

Line 25 loads the CYMDIST FMU 

Line 26 loads the GridDyn FMU. We used in this example a GridDyn FMU which models the IEEE 14-Bus System.

Line 28 and 29 set-up the parameters for the simulation.

Line 32 - 37 create the vector of input and output names for both FMUs.

Line 45 - 53 get the value references of the CYMDIST and GridDyn variables

Line 69 and 70 initialize the FMUs.

Line 73 calls event update for the CYMDIST FMU. This is required by CYMDIST which is 
a model exchange FMU and hence needs to call this function prior to entering
the continous time mode.

Line 74 CYMDIST enters in continuous time mode.

Line 77 In the loop, CYMDIST and GridDyn are evaluated.

First, The outputs of GridDyn are retrieved. these outputs must be the coverged solution between
CYMDIST and GridDyn at the time when GridDyn is invoked.
 
Second, The outputs of GridDyn are set as inputs of CYMDIST at the same time instant.
CYMDIST computes the outputs at that time instant and send the updated outputs. 

Line 88 and 89 complete the simulation and terminate both FMUs.
 
.. literalinclude:: scripts/coupling.py
   :language: python
   :linenos:


