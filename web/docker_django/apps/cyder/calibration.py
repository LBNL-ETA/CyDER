from __future__ import division
import models as m
import datetime as dt
import tool as t
import upmu


def calibrate(model_id):
    """
    Launch individual calibration function and save to the DB
    """
    # Get the data necessary for the calibration
    upmu, model, device = get_calibration_data(model_id)

    # Launch simulation
    sim_result = get_simulation_result(model, upmu, device)

    # Find the new impedances
    impedances = get_calibrated_impedances(sim_result)

    # Update the database
    temp_model = m.Model.objects.get(id=model_id)
    history = m.CalibrationHistory(
        model=temp_model,
        date=dt.datetime.now() - dt.timedelta(minutes=10),
        updated=False,
        calibration_algorithm="Basic")
    history.save()
    calibration_result = m.CalibrationResult(
        calibration=history,
        impedance=impedances['impedances']['A'])
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
    Return all the data to launch a calibration.
    It includes model filename, breaker number and type id as well as uPMU data.
    """
    # Get the upmu data 10 minute in the past to avoid problem?
    date_from = dt.datetime.now() - dt.timedelta(minutes=10)
    date_to = False
    upmu = upmu.get('not in use so far', date_from, date_to)
    try:
        upmu = upmu['data'][0]
    except:
        raise Exception("Upmu data was empty")

    # Get the model's filename
    try:
        model = m.Model.objects.get(id=model_id)
    except:
        raise Exception('Model id does not exist in the database')

    # Get the breaker number and type_id
    try:
        devices = m.Devices.objects.filter(model_id=model_id, device_type="Breaker type.")
        device = devices[0]
    except:
        raise Exception("No breaker available for this model")

    return upmu, model, device


def get_simulation_result(model, upmu, device):
    """
    Send and ssh request and parse the results.
    CMD launch a python script on the host computer.
    """
    # Launch SSH request to the server and grab the stdout
    timeout = 10
    arg = [str(model.filename), str(device.device_number), str(device.device_type)]
    upmu_arg_names = ['P_A', 'P_B', 'P_C', 'Q_A', 'Q_B', 'Q_C', 'VMAG_A', 'VMAG_B', 'VMAG_C']
    arg.extend([upmu[name] for name in upmu_arg_names])
    cmd = ('project_cyder/web/docker_django/worker/calibration.py')
    output, status = t.run_ssh_command(cmd, timeout=timeout, arg=arg)

    # Parse ssh output
    if output is not False:
        keys = ['upmu' ,'voltage_mag', 'voltage_angle', 'current_mag', 'current_angle']
        result = t.parse_ssh_dict(output, keys, status)
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

    result = ((sim_result['upmu']['VMAG_A'] - sim_result['voltage_mag']['A']) / sim_result['current_mag']['A'])
    return result
