from __future__ import division
import models as m
import subprocess
import time
import datetime as dt
import ast
import pdb


def update_model_nodes(model_id):
    """
    Update the nodes for a model, return the number of nodes.
    """
    # Query the model information
    try:
        model_instance = m.Model.objects.get(id=model_id)
    except:
        raise Exception('Model id does not exist in the database')

    # Get the node data
    nodes = get_nodes_data(model_instance.filename)

    # Update the database
    for node in nodes:
        temp = m.Node(model=model_instance, **node)
        temp.save()

    return len(nodes)


def get_nodes_data(filename):
    """
    Launch ssh command and retrieve outputs
    """
    # Launch SSH request to the server and grab the stdout
    timeout = 20
    cmd = 'project_cyder/web/docker_django/worker/model_content.py ' + str(filename)
    output, status = run_ssh_command(cmd, timeout=timeout)

    # Parse ssh output
    if output is not False:
        result = parse_dataframe_ssh_output(output, status)
    else:
        raise Exception('SSH request to the server took more than ' +
                        str(timeout) + ' seconds')

    # Return the value from the calibration
    return result


def calibration_process(model_id):
    """
    Launch individual calibration function and save to the DB
    """
    # Get the calibration data
    sim_result = get_calibration_data(model_id)

    # Find the new impedances
    impedances = get_calibrated_impedances(sim_result)

    # Update the database
    temp_model = m.Model.objects.get(id=model_id)
    history = m.CalibrationHistory(
        model=temp_model,
        date=dt.datetime.now() - dt.timedelta(hours=1),
        updated=False,
        calibration_algorithm="Basic")
    history.save()
    calibration_result = m.CalibrationResult(
        calibration=history,
        impedance_a=impedances['impedances']['A'],
        impedance_b=impedances['impedances']['B'],
        impedance_c=impedances['impedances']['C'])
    calibration_result.save()
    calibration_data = m.CalibrationData(
        calibration=history,
        p_a=sim_result['upmu']['P_A'],
        p_b=sim_result['upmu']['P_B'],
        p_c=sim_result['upmu']['P_C'],
        q_a=sim_result['upmu']['Q_A'],
        q_b=sim_result['upmu']['Q_B'],
        q_c=sim_result['upmu']['Q_C'],
        voltage_a=sim_result['upmu']['VMAG_A'],
        voltage_b=sim_result['upmu']['VMAG_B'],
        voltage_c=sim_result['upmu']['VMAG_C'])
    calibration_data.save()

    return True


def get_calibration_data(model_id):
    """
    Send and ssh request and parse the results.
    CMD launch a python script on the host computer.
    """
    # Query the model information
    try:
        model = m.Model.objects.get(id=model_id)
    except:
        raise Exception('Model id does not exist in the database')

    # Launch SSH request to the server and grab the stdout
    timeout = 10
    model_parent_path = ''
    cmd = ('project_cyder/web/docker_django/worker/calibration.py ' +
           model_parent_path + str(model.filename) + ' ' + str(model.upmu_location))
    output, status = run_ssh_command(cmd, timeout=timeout)

    # Parse ssh output
    if output is not False:
        keys = ['upmu', 'voltages', 'currents']
        result = parse_ssh_output(output, keys, status)
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
                           shell=False, stdout=subprocess.PIPE, bufsize=10000,
                           stderr=subprocess.PIPE)

    # Test for output every second
    for step in range(0, timeout):
        time.sleep(1)
        if ssh.poll() is not None:
            return ssh.stdout.readlines(), 'Success'

    # The ssh query was longer than timeout duration
    ssh.kill()
    return False, ssh.stderr.readlines()


def parse_ssh_output(output, keys, status):
    """
    Parse the output of an ssh request.
    Output lenght must be the same as keys lenght.
    """
    # Check if the lenght is the same
    if len(output) != len(keys):
        print('#####')
        print('output:' + str(output))
        print('status:' + str(status))
        print('#####')
        raise Exception('The output from the ssh request was not the right lenght')

    # Parse the string
    result = {}
    for key, string in zip(keys, output):
        dict_string = '{' + string.split('{', 1)[1].split('}')[0] + '}'
        result[key] = ast.literal_eval(dict_string)

    return result


def parse_dataframe_ssh_output(output, status):
    """
    Parse the output from a dataframe where every row is a different line
    """
    result = []
    for string in output:
        dict_string = '{' + string.split('{', 1)[1].split('}')[0] + '}'
        result.append(ast.literal_eval(dict_string))

    return result
