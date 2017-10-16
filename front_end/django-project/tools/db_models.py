import sim_worker.tasks
import pandas
from cyder.grid_models.models import Model, Device, Node, Section

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
    (model_info, nodes_df, sections_df, devices_df) = result.get()

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

    lenght = len(nodes_df)
    for index in range(0, lenght):
        node_row = nodes_df.iloc[index]
        node = Node(model=model, **node_row)
        node.save()
        print("\rImported nodes: %d/%d" % (index+1, lenght), end="")
    print()

    lenght = len(sections_df)
    for index in range(0, lenght):
        section_row = sections_df.iloc[index]

        section = Section(model=model, **exclude(section_row, ['from_node_id', 'to_node_id']))
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
        device = Device(model=model, **exclude(device_row, ['section_id']))
        device.model = model
        device.section = Section.objects.get(model=model, section_id=device_row['section_id'])
        device.save()
        print("\rImported devices: %d/%d" % (index+1, lenght), end="")
    print()
