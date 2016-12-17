from __future__ import division
from .models import Model
import time
import ast


def get_calibration_data(model_id):
    """
    Send and ssh request and parse the results.
    CMD launch a python script on the host computer.
    """
    # Query the model information
    try:
        model = Model.objects.get(id=model_id)
    except:
        raise Exception('Model id does not exist in the database')

    # Launch SSH request to the server and grab the stdout
    timeout = 10
    model_parent_path = ''
    cmd = ('project_cyder/web/docker_django/worker/calibration.py ' +
           model_parent_path + str(model.filename) + ' ' + str(model.upmu_location))
    output = run_ssh_command(cmd, timeout=timeout)

    # Parse ssh output
    if output is not False:
        keys = ['upmu', 'voltages', 'currents']
        result = parse_ssh_output(output, keys)
    else:
        raise Exception('SSH request to the server took more than ' +
                        str(timeout) + ' seconds')

    # Return the value from the calibration
    return result


def get_calibrated_impedances(sim_result):
    """
    From simulation results get the equivalent impedance of the grid model
    sim_result format is expected to be:
    {'umpu': ..., 'voltages': ..., 'currents': ...}
    """
    result = {'impedances':{}}
    phases = ['A', 'B', 'C']
    for phase in phases:
        result['impedances'][phase] = (sim_result['voltages'][phase] /
                                       sim_result['currents'][phase])

    return result


def run_ssh_command(cmd, timeout=10):
    """
    Send a ssh request and check if the request is not hanging.
    timeout [seconds]
    """
    # Launch ssh query
    ssh = subprocess.Popen(["ssh","Jonathan@128.3.12.69", "python", cmd],
                           shell=False, stdout=subprocess.PIPE,
                           stderr=subprocess.PIPE)

    # Test for output every second
    for step in range(0, timeout):
        time.sleep(1)
        if ssh.poll() is not None:
            return ssh.stdout.readlines()

    # The ssh query was longer than timeout duration
    ssh.kill()
    return False


def parse_ssh_output(output, keys):
    """
    Parse the output of an ssh request.
    Output lenght must be the same as keys lenght.
    """
    # Check if the lenght is the same
    if len(ouput) != len(keys):
        print('#####')
        print(output)
        print('#####')
        raise Exception('The output from the ssh request was not the right lenght')

    # Parse the string
    result = {}
    for key, string in zip(keys, output):
        dict_string = '{' + string.split('{', 1)[1].split('}')[0] + '}'
        result[key] = ast.literal_eval(dict_string)

    return result
