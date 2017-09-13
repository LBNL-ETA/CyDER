import sim_worker.tasks
import pandas
from testapp.models import Model, Device, Node

def import_model(modelfile):
	try:
		model = Model.objects.get(filename=modelfile)
	except Model.DoesNotExist:
		model = None
	
	print("Get model from worker...")
	resultDevices = sim_worker.tasks.get_model_devices.delay(modelfile)
	resultNodes =  sim_worker.tasks.get_model_nodes.delay(modelfile)
	devices_df = resultDevices.get()
	nodes_df = resultNodes.get()
	
	if model != None:
		print("Updating model in DB...")
		Device.objects.filter(model=model).delete()
		Node.objects.filter(model=model).delete()
	else:
		print("Importing model in DB...")
		model = Model()
		model.filename = modelfile
		model.save()
	
	lenght = len(devices_df)
	for index in range(0, lenght):
		device_row = devices_df.iloc[index]
		device = Device()
		device.model = model
		device.device_number = device_row['device_number']
		device.device_type = device_row['device_type']
		device.device_type_id = device_row['device_type_id']
		device.section_id = device_row['section_id']
		device.distance = device_row['distance']
		device.latitude = device_row['latitude']
		device.longitude = device_row['longitude']
		device.save()
		print("\rImported devices: %d/%d" % (index+1, lenght), end="")
	print()
	
	lenght = len(nodes_df)
	for index in range(0, lenght):
		node_row = nodes_df.iloc[index]
		node = Node()
		node.model = model
		node.node_id = node_row['node_id']
		node.section_id = node_row['section_id']
		node.latitude = node_row['latitude']
		node.longitude = node_row['longitude']
		node.save()
		print("\rImported nodes: %d/%d" % (index+1, lenght), end="")
	print()
