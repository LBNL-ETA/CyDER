from __future__ import division
import models as m
import datetime as dt
import tool as t
import upmu as u
import numpy


def calibrate(model_id):
    """
    Launch individual calibration function and save to the DB
    """
    # Get the data necessary for the calibration
    upmu, upmu2, model, device = get_calibration_data(model_id)

    # Launch simulation
    sim_result = get_simulation_result(model, upmu, device)

    # Find the new impedances
    impedance_real, impedance_imag = get_calibrated_impedances(sim_result, upmu, upmu2)

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
        impedance_real=impedance_real,
        impedance_imag=impedance_imag)
    calibration_result.save()
    calibration_data = m.CalibrationData(
        calibration=history,
        p_a=upmu['P_A'],
        p_b=upmu['P_B'],
        p_c=upmu['P_C'],
        q_a=upmu['Q_A'],
        q_b=upmu['Q_B'],
        q_c=upmu['Q_C'],
        voltage_a=upmu['VMAG_A'],
        voltage_b=upmu['VMAG_B'],
        voltage_c=upmu['VMAG_C'])
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

    # Get the breaker data
    upmu = u.get('grizzly_bus1', date_from, date_to)
    try:
        upmu = upmu[0]
    except:
        raise Exception("Upmu data at breaker was empty")

    # Get further down the line data
    upmu2 = u.get('a6_bus1', date_from, date_to)
    try:
        upmu2 = upmu2[0]
    except:
        raise Exception("Upmu data further down the line was empty")

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

    return upmu, upmu2, model, device


def get_simulation_result(model, upmu, device):
    """
    Send and ssh request and parse the results.
    CMD launch a python script on the host computer.
    """
    # Launch SSH request to the server and grab the stdout
    timeout = 30
    arg = [str(model.filename), str(device.device_number), str(device.device_type_id)]
    upmu_arg_names = ['P_A', 'P_B', 'P_C', 'Q_A', 'Q_B', 'Q_C', 'VMAG_A', 'VMAG_B', 'VMAG_C']
    arg.extend([str(upmu[name]) for name in upmu_arg_names])
    cmd = ('project_cyder/web/docker_django/worker/calibration.py')
    output, status = t.run_ssh_command(cmd, timeout=timeout, arg=arg)

    # Parse ssh output
    if output is not False:
        keys = ['current']
        result = t.parse_ssh_dict(output, keys, status)
    else:
        raise Exception('SSH request to the server took more than ' +
                        str(timeout) + ' seconds')

    # Return the value from the calibration
    return result


def get_calibrated_impedances(sim_result, upmu, upmu2):
    """
    From simulation results get the equivalent impedance of the grid model
    sim_result format is expected to be:
    {'umpu': ..., 'voltages': ..., 'currents': ...}
    """
    # Get all values as a complex
    # raise Exception(str(sim_result))
    i1 = sim_result['current']['i1mag'] * numpy.exp(1j * numpy.deg2rad(sim_result['current']['i1angle']))
    va_breaker = upmu['L1Mag'] * numpy.exp(1j * numpy.deg2rad(upmu['L1Ang']))
    vb_breaker = upmu['L2Mag'] * numpy.exp(1j * numpy.deg2rad(upmu['L2Ang']))
    vc_breaker = upmu['L3Mag'] * numpy.exp(1j * numpy.deg2rad(upmu['L3Ang']))
    va_downstream = upmu2['L1Mag'] * numpy.exp(1j * numpy.deg2rad(upmu2['L1Ang']))
    vb_downstream = upmu2['L2Mag'] * numpy.exp(1j * numpy.deg2rad(upmu2['L2Ang']))
    vc_downstream = upmu2['L3Mag'] * numpy.exp(1j * numpy.deg2rad(upmu2['L3Ang']))

    # Get the positive sequence for breaker and downstream
    a = 1 * numpy.exp(1j * numpy.deg2rad(120))
    v1_breaker = (va_breaker + a * vb_breaker + a * a * vc_breaker) / 3
    v1_downstream = (va_downstream + a * vb_downstream + a * a * vc_downstream) / 3

    # Simple equation
    result = (v1_breaker - v1_downstream) / i1
    return result.real, result.imag
