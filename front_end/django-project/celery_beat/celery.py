import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.dev')

from celery import Celery
from datetime import timedelta

app = Celery('celery_beat',
             broker='redis://128.3.144.76:6379/0',
             backend='redis://128.3.144.76:6379/0',
             include=[
                'cyder.projects.tasks',
             ])

# Optional configuration, see the application user guide.
app.conf.update(
    CELERY_TASK_RESULT_EXPIRES=1,
    CELERY_TRACK_STARTED=True,
    CELERY_ACCEPT_CONTENT = ['json'],
    CELERY_RESULT_SERIALIZER = 'json',
    CELERY_TASK_SERIALIZER = 'json',
    CELERYBEAT_SCHEDULE = {
        'retrieve_projects_result': {
            'task': 'cyder.projects.tasks.retrieve_projects_result',
            'schedule': timedelta(seconds=2),
        },
    },
)

if __name__ == '__main__':
    app.start()
