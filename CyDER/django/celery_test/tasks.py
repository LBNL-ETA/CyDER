from .celery import app
from time import sleep

@app.task
def start_sim(x, y):
	sleep(10)
	return x / y
