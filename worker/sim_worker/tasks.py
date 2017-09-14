# Every task defined in this file should be declared in /front-end/django-project/sim_worker/task.py

from .celery import app
import pandas

@app.task
def get_model(modelfile):
	# Import cympy from the function to prevent multiple import caused by celery importing this module at launch
	import cympy
	from .cymdist_tool import tool as cymdist

	# Open a study
	filename = "C:\\Users\\DRRC\\Desktop\\PGE_Models_DO_NOT_SHARE\\" + modelfile
	cympy.study.Open(filename)

	# Get all the devices informations
	devices = cymdist.list_devices()
	devices = cymdist.get_distance(devices)
	devices = cymdist.get_coordinates(devices)
	devices = cymdist.get_sections(devices)
	# Get all the node informations
	nodes = cymdist.list_nodes()

	# Remove cympy object to be able to serialize
	devices = devices.drop('device', axis=1)
	nodes = nodes.drop('node_object', axis=1)

	# Return result and exit the worker to "free" cympy
	app.backend.mark_as_done(get_model.request.id, (devices, nodes))
	exit(0)
