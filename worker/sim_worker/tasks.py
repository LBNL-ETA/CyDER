from .celery import app
import pandas
#import cympy
#from cymdist_tool import tool as cymdist

@app.task
def get_model_devices(modelfile):
	# Open a study
	#filename = "C:\\Users\\DRRC\\Desktop\\PGE_Models_DO_NOT_SHARE\\" + model_filename
	#cympy.study.Open(filename)

	# Get all the node informations
	#devices = cymdist.list_devices()
	#devices = cymdist.get_distance(devices)
	#devices = cymdist.get_coordinates(devices)

	# Remove cympy onbect to be able to serialize
	#devices = devices.drop('device', axis=1)
	
	# For test
	#devices.to_pickle("./data.bin")
	devices = pandas.read_pickle("./data.bin")
	
	return devices
