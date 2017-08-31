from .celery import app

@app.task
def start_sim(x, y):
    return x + y
