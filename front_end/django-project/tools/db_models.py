import sim_worker.tasks
import pandas
from cyder.grid_models.models import Model, Device, Node, Section

def import_model(modelfile):
    try:
        model = Model.objects.get(filename=modelfile)
    except Model.DoesNotExist:
        model = None

    print("Get model from worker...")
    result = sim_worker.tasks.get_model.delay(modelfile)
    (nodes_df, sections_df, devices_df) = result.get()

    if model != None:
        print("Updating model in DB...")
        Node.objects.filter(model=model).delete()
        Section.objects.filter(model=model).delete()
        Device.objects.filter(model=model).delete()

    else:
        print("Importing model in DB...")
        model = Model()
        model.filename = modelfile
        model.save()

    lenght = len(nodes_df)
    for index in range(0, lenght):
        node_row = nodes_df.iloc[index]
        node = Node()
        node.model = model
        node.node_id = node_row['node_id']
        node.latitude = node_row['latitude']
        node.longitude = node_row['longitude']
        node.save()
        print("\rImported nodes: %d/%d" % (index+1, lenght), end="")
    print()

    lenght = len(sections_df)
    for index in range(0, lenght):
        section_row = sections_df.iloc[index]
        section = Section()
        section.model = model
        section.section_id = section_row['section_id']
        section.from_node = Node.objects.get(model=model, node_id=section_row['from_node_id'])
        if section_row['to_node_id'] == section_row['section_id']:
            section.to_node = None
        else:
            section.to_node = Node.objects.get(model=model, node_id=section_row['to_node_id'])
        section.save()
        print("\rImported sections: %d/%d" % (index+1, lenght), end="")
    print()

    lenght = len(devices_df)
    for index in range(0, lenght):
        device_row = devices_df.iloc[index]
        device = Device()
        device.model = model
        device.device_number = device_row['device_number']
        device.device_type = device_row['device_type']
        device.section = Section.objects.get(model=model, section_id=device_row['section_id'])
        device.distance = device_row['distance']
        device.latitude = device_row['latitude']
        device.longitude = device_row['longitude']
        device.save()
        print("\rImported devices: %d/%d" % (index+1, lenght), end="")
    print()
