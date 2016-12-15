from __future__ import division
from celery import shared_task
import datetime
from . import tool

@shared_task
def test():
    # Return a success
    return True

@shared_task
def calibrate_models():
    # Launch the calibration function on each model
    pass
