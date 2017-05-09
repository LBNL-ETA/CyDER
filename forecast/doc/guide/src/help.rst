
.. highlight:: rest

.. _help:

Help
====

Data File Format
----------------
For many of the operations within the forecasting module, a data file is required.
This section outlines how the module expects the file to be formated.

Training And Testing File
~~~~~~~~~~~~~~~~~~~~~~~~~
The training and testing files contain at the first line three comma
numbers: number_of_entries, number_of_inputs, number_of_outputs. This is followed
by an interleaved lines of comma seperated inputs and comma separated outputs.

An example is shown below:

::

  NUM_ENTRIES, NUM_INPUTS, NUM_OUTPUTS
  input_1, input_2 # Entry 1
  output_1, output_2, output_3 # Entry 1
  ...
  ...
  input_1, input_2 # Entry NUM_ENTRIES
  output_1, output_2, output_3 # Entry NUM_ENTRIES

A concrete example is shown below:

::

  1000 2 3
  1.000000 0.000000
  1.000000 0.000000 1.000000
  0.999950 0.010000
  0.999900 0.009999 0.999900
  0.999800 0.019999
  0.999600 0.019995 0.999600
  0.999550 0.029996
  0.999100 0.029982 0.999100

Prediction File
~~~~~~~~~~~~~~~
This type of file is identical to the training and testing files but in this case
num_outputs must be set to zero and only lines representing the input are used.
During prediction, the real outputs aren't available so it isn't necessary to pass
these to the module.

A concrete example is shown below:

::

  300 2 0
  -0.171866 0.985120
  -0.181708 0.983352
  -0.191533 0.981486
  -0.201338 0.979522
  -0.211123 0.977460
  -0.220887 0.975300
  -0.230628 0.973042
