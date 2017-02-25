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
    input_model_filename = 'BU0001.sxst'
    input_save_to_file = 1
    input_voltage_names = ['VMAG_A', 'VMAG_B', 'VMAG_C', 'VANG_A', 'VANG_B', 'VANG_C']
    input_voltage_values = [2520, 2520, 2520, 0, -120, 120]
    output_names = ['IA', 'IAngleA', 'IB', 'IAngleB', 'IC', 'IAngleC']
    output_node_names = ['800032440', '800032440', '800032440', 
                         '800032440', '800032440', '800032440']
    exchange(input_model_filename, input_voltage_values, 
             input_voltage_names, output_names, input_save_to_file)

def exchange(input_model_filename, input_voltage_values, 
             input_voltage_names, output_names, input_save_to_file):
    """
    Args:
        input_model_filename (String): path to the cymdist grid model
        input_save_to_file (1 or 0): save all nodes results to a file
        input_voltage_names (Strings): voltage vector names
        input_voltage_values (Floats): voltage vector values (same lenght as voltage_names)
        output_names (Strings): vector of name matching CymDIST nomenclature
    Example:
        >>> input_model_filename = 'BU0001.sxst'
        >>> input_save_to_file = 1
        >>> input_voltage_names = ['VMAG_A', 'VMAG_B', 'VMAG_C', 'VANG_A', 'VANG_B', 'VANG_C']
        >>> input_voltage_values = [2520, 2520, 2520, 0, -120, 120]
        >>> output_names = ['IA', 'IAngleA', 'IB', 'IAngleB', 'IC', 'IAngleC']
        >>> fmu_wrapper(input_model_filename, input_save_to_file,
                input_voltage_names, input_voltage_values, output_names)
    Note:
        output_names can be: ['KWA', 'KWB', 'KWC', 'KVARA', 'KVARB', 'KVARC',
        'IA', 'IAngleA', 'IB', 'IAngleB', 'IC', 'IAngleC', 'PFA', 'PFB', 'PFC']
        for a greater list see CymDIST > customize > keywords > powerflow
        (output unit is directly given by output name)
    """
    # Call the CYMDIST wrapper
    results = []
    n_exp_res = len(output_names)
    start = datetime.now()
    outputs = functions.fmu_wrapper(input_model_filename, 
                                    input_save_to_file, 
                                    input_voltage_names,
                                    input_voltage_values, 
                                    output_names)
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

