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
    input_model_filename = 0
    input_save_to_file = 0
    input_voltage_names = ['VMAG_A', 'VMAG_B', 'VMAG_C', 'VANG_A', 'VANG_B', 'VANG_C']
    input_voltage_values = [2520, 2520, 2520, 0, -120, 120]
    output_names = ['IA', 'IAngleA', 'IB', 'IAngleB', 'IC', 'IAngleC']
    outputs = exchange(input_model_filename, input_voltage_values, 
             input_voltage_names, output_names, input_save_to_file)
    print ("These are the output values " + str(outputs))
    
def exchange(input_model_filename, input_voltage_values, 
             input_voltage_names, output_names, input_save_to_file):
    """
    Args:
        input_model_filename (String): path to the cymdist grid model
        input_save_to_file (1 or 0): save all nodes results to a file
        input_voltage_names (Strings): voltage vector names
        input_voltage_values (Floats): voltage vector values (same length as voltage_names)
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
    output_values=functions.fmu_wrapper(int(input_model_filename), int(input_save_to_file),
                input_voltage_names, input_voltage_values, output_names)
    n_out_nam = len(output_names)
    n_out_val = len(output_values)
    if (n_out_nam!=n_out_val):
        print("The length of the output_names " + str(n_out_nam) + 
              "does not match the length of the output results " + 
              str(n_out_val) + ". This is not allowed. " +
              "Simulation will be terminated.")
        sys.exit(1)
    for cnt, elem in enumerate(output_names):
        try:
            # Forced the output to be a float
            results.append(1.0*float(output_values[cnt]))
        except ValueError:
            print('Cannot convert output ' + elem + ' to a float.')
    return (results)

if __name__ == '__main__':
    # Try running this module!
    main()

