from celery import Celery
from kombu import Exchange, Queue

app = Celery('sim_worker',
             broker='redis://128.3.144.76:6379/0',
             backend='redis://128.3.144.76:6379/0',
             include=['sim_worker.tasks'])

app.conf.update(
    CELERY_TASK_RESULT_EXPIRES=3600,
    CELERY_TRACK_STARTED=True,
    CELERY_ACCEPT_CONTENT = ['json'],
    CELERY_RESULT_SERIALIZER = 'json',
    CELERY_TASK_SERIALIZER = 'json',
    CELERY_DEFAULT_QUEUE = 'sim_worker',
    CELERY_QUEUES = (
        Queue('sim_worker', Exchange('sim_worker'), routing_key='sim_worker'),
    )
)

if __name__ == '__main__':
    app.start()
