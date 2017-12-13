import sim_worker.tasks
from cyder.models.models import *

# Return a copy of dict, without the keys list in exclude_keys
def exclude(dict, exclude_keys):
    new_dict = {}
    for key in dict.keys():
        if key not in exclude_keys:
            new_dict[key] = dict[key]
    return new_dict

def import_model(modelname):
    try:
        model = Model.objects.get(name=modelname)
    except Model.DoesNotExist:
        model = None

    print("Get model from worker...")
    result = sim_worker.tasks.get_model.delay(modelname)
    (model_info, nodes, sections, devices) = result.get()

    if model != None:
        print("Updating model in DB...")
        Node.objects.filter(model=model).delete()
        Section.objects.filter(model=model).delete()
        Device.objects.filter(model=model).delete()
        model = Model(id=model.id, name=modelname, **model_info)
        model.save()

    else:
        print("Importing model in DB...")
        model = Model(name=modelname, **model_info)
        model.save()

    lenght = len(nodes)
    for index in range(0, lenght):
        node_row = nodes[index]
        node = Node(model=model, **node_row)
        node.save()
        print("\rImported nodes: %d/%d" % (index+1, lenght), end="")
    print()

    lenght = len(sections)
    for index in range(0, lenght):
        section_row = sections[index]

        section = Section(model=model, **exclude(section_row, ['from_node_id', 'to_node_id']))
        section.from_node = Node.objects.get(model=model, node_id=section_row['from_node_id'])
        try:
            section.to_node = Node.objects.get(model=model, node_id=section_row['to_node_id'])
        except:
            section.to_node = None
        section.save()
        print("\rImported sections: %d/%d" % (index+1, lenght), end="")
    print()

    lenght = len(devices)
    for index in range(0, lenght):
        device_row = devices[index]
        device = Device(model=model, **exclude(device_row, ['section_id', 'detail']))
        device.model = model
        if device.device_type != 35: # Source
            device.section = Section.objects.get(model=model, section_id=device_row['section_id'])
        device.save()

        if device.device_type == 14: # Spot loads
            load = Load(device=device, **(device_row['detail']))
            load.save()
        elif device.device_type == 39: # PVs
            pv = PV(device=device, **(device_row['detail']))
            pv.save()

        print("\rImported devices: %d/%d" % (index+1, lenght), end="")
    print()
