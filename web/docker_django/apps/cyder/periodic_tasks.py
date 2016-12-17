from __future__ import division
from celery import shared_task
import datetime as dt
from . import tool
import models as m

@shared_task
def test():
    # Return a success
    return True

@shared_task
def calibrate_models():
    # Get all the latest models
    models = m.Model.objects.all()
    model_ids = [model.id for model in models]

    for model_id in model_ids:
        # try:
        # Get the calibration data
        sim_result = tool.get_calibration_data(model_id)

        # Find the new impedances
        impedances = tool.get_calibrated_impedances(sim_result)

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
        # except:
        #     # Log the error message
        #     print('Error')

    return True
