# Every task defined in this file should be declared in /front-end/django-project/sim_worker/task.py

from .celery import app
import pandas

@app.task
def get_model_devices(modelfile):
	# Import cympy from the function to prevent multiple import caused by celery importing this module at launch
	import cympy
	from .cymdist_tool import tool as cymdist

	# Open a study
	filename = "C:\\Users\\DRRC\\Desktop\\PGE_Models_DO_NOT_SHARE\\" + modelfile
	cympy.study.Open(filename)

	# Get all the node informations
	devices = cymdist.list_devices()
	devices = cymdist.get_distance(devices)
	devices = cymdist.get_coordinates(devices)

	# Remove cympy onbect to be able to serialize
	devices = devices.drop('device', axis=1)

	# For test
	#devices.to_pickle("./data.bin")
	#devices = pandas.read_pickle("./data.bin")

	return devices

