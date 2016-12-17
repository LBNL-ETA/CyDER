from __future__ import division
from celery import shared_task
import datetime
from . import tool
from .model import Model

@shared_task
def test():
    # Return a success
    return True

@shared_task
def calibrate_models():
    # Get all the latest models
    models = Model.objects.all()
    model_ids = [model.id for model in models]

    for model_id in model_ids:
        # Get the calibration data
        sim_result = tool.get_calibration_data(model_id)

        # Find the new impedances
        impedances = tool.get_calibrated_impedances(sim_result)

        # Save new impedances to the database
        pass
