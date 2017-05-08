from __future__ import division
from celery import shared_task
import datetime as dt
from . import calibration
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
        try:
            calibration.calibrate(model_id)
        except:
            # Log the error message
            print('Error')

    return True
