from .celery import app

@app.task
def do_some_work(x, y):
    return x + y
