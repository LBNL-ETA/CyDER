from celery import Celery
from kombu import Exchange, Queue

app = Celery('sim_worker',
             broker='redis://128.3.111.21', # <= redis IP goes here
             backend='redis://128.3.111.21', # <= redis IP goes here
             include=['sim_worker.tasks'])

# This configuration should be the same evrey where the sim_worker celery application is used
# /front-end/django-project/sim_worker/celery.py
# /front_end/worker/sim_worker/celery.py
# /front_end/dummy_worker/sim_worker/celery.py
# If you modify one, please copy/paste the modifications into the others
app.conf.update(
    CELERY_TASK_RESULT_EXPIRES=20,
    CELERY_TRACK_STARTED=True,
    CELERY_ACCEPT_CONTENT = ['json'],
    CELERY_RESULT_SERIALIZER = 'json',
    CELERY_TASK_SERIALIZER = 'json',
    CELERY_DEFAULT_QUEUE = 'sim_worker',
    CELERY_QUEUES = (
        Queue('sim_worker', Exchange('sim_worker'), routing_key='sim_worker'),
    )
    # The default queue is changed to sim_woker to be sure those task are execute by the simulation worker
    # (and not the worker that run the celery_beat on the wsgi container which use the same redis DB)
)

if __name__ == '__main__':
    app.start()
