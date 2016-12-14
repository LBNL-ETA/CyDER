from celery import shared_task
import datetime

@shared_task
def test():
    # Return a success
    return True
