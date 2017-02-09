# Python module with test functions.
# These functions are used to test the Modelica Python interface.
# They are not meaningful, but rather kept simple to test whether
# the interface is correct.
#
# Make sure that the python path is set, such as by running
# export PYTHONPATH=`pwd`

from datetime import datetime
import functions
import os

def main():
    print (os.getcwd())
    input_names = ['VMAG_A', 'VMAG_B', 'VMAG_C', 'VANG_A', 'VANG_B', 'VANG_C']
    input_values = [2520, 2520, 2520, 0.0, -120.0, 120.0]
    output_names = ['KWA', 'KWB', 'KWC', 'KVARA', 'KVARB', 'KVARC']
    output_node_names = ['800032440', '800032440', '800032440', 
                         '800032440', '800032440', '800032440']
    exchange("BU0001.sxst", input_values, input_names,
             output_names, output_node_names, 0)

def exchange(input_file_name, input_values, input_names,
             output_names, output_node_names, write_results):
    """
     Args:
        input_file_name (str): Name of the CYMDIST grid model.
        input_values(dbl): Input values.
        input_names(str): Input names.
        output_names(str):  Output names.
        output_node_names(str): Outputs nodes names.
        write_results(int): Flag for writing results.


    """
    # Call the CYMDIST wrapper
    results = []
    n_exp_res = len(output_names)
    start = datetime.now()
    outputs = functions.fmu_wrapper(input_file_name, input_values, input_names,
                                   output_names, output_node_names, write_results)
    end = datetime.now()
    print('Ran a CYMDIST simulation in ' +
          str((end - start).total_seconds()) + ' seconds.')
    # Get the outputs.
    n_ret_res = len(outputs)
    # Check if the number of outputs is expected.
    # Do not assert but rather provide some debugging information.
    if (n_exp_res != n_ret_res):
        print('WARNING: The number of returned outputs ' + str(n_ret_res)
              + ' is different from the number of expected outputs '
              + str(n_exp_res) + '.')
        # If the number of returned outputs is bigger than the expected ones
        # we get the first returned values and inform the user with a message.
        if (n_ret_res > n_exp_res):
            print('WARNING: The first ' + str(n_exp_res) + ' will be retrieved.')
        else:
            print('WARNING: Incorrect number of outputs ' +
                  str(n_ret_res) + ' is returned.')
    # Get the outputs and convert to floats.
    # If the number of returned results is incorrect, then rely on 
    # the C-wrapper which will throw an exception with a meaningful message.
    for i in range(n_exp_res):
        try:
            results.append(float(outputs[i]))
        except ValueError:
            print('Cannot convert output ' + outputs[i] + ' to a float.')
    return results

if __name__ == '__main__':
    # Try running this module!
    main()

