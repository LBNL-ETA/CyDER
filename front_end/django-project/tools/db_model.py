import sim_worker.tasks
import pandas
from testapp.models import Device

def update():
	print("Update model in DB...")
	modelfile = 'AT.sxst'
	result = sim_worker.tasks.get_model_devices.delay(modelfile)
	devices = result.get()
	
	Device.objects.all().delete()
	
	lenght = len(devices)
	for index in range(0, lenght):
		device = devices.iloc[index]
		d = Device()
		d.device_number = device['device_number']
		d.device_type = device['device_type']
		d.device_type_id = device['device_type_id']
		d.device_number = device['distance']
		d.distance = device['section_id']
		d.latitude = device['latitude']
		d.longitude = device['longitude']
		d.save()
		print("\rUpdated devices: %d/%d" % (index, lenght), end="")
	print()
