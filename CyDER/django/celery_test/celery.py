from celery import Celery

app = Celery('celery_test',
             broker='redis://128.3.146.130:6379/0',
             backend='redis://128.3.146.130:6379/0',
             include=['celery_test.tasks'])

# Optional configuration, see the application user guide.
app.conf.update(
    result_expires=3600,
    task_track_started=True,
)

if __name__ == '__main__':
    app.start()
