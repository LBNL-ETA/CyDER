import pandas
import cympy

def open_study(modelfile):
    filename = "C:\\Users\\DRRC\\Desktop\\PGE_Models_DO_NOT_SHARE\\" + modelfile
    cympy.study.Open(filename)

def list_nodes():
    nodes = cympy.study.ListNodes()

    nodes = pandas.DataFrame(nodes, columns=['node_object'])
    nodes['node_id'] = nodes['node_object'].apply(lambda x: x.ID)
    nodes['longitude'] = nodes['node_object'].apply(lambda x: x.X / 100000)
    nodes['latitude'] = nodes['node_object'].apply(lambda x: x.Y / (1.26 * 100000))

    return nodes

def list_sections():
    sections = cympy.study.ListSections()

    sections = pandas.DataFrame(sections, columns=['section_object'])
    sections['section_id'] = sections['section_object'].apply(lambda x: x.ID)
    sections['from_node_id'] = sections['section_object'].apply(lambda x: x.FromNode.ID)
    sections['to_node_id'] = sections['section_object'].apply(lambda x: x.ToNode.ID)

    return sections

def list_devices(device_type=False):
    if device_type:
        devices = cympy.study.ListDevices(device_type)
    else:
        devices = cympy.study.ListDevices()

    devices = pandas.DataFrame(devices, columns=['device_object'])
    devices['device_type'] = devices['device_object'].apply(lambda x: x.DeviceType)
    devices['device_number'] = devices['device_object'].apply(lambda x: x.DeviceNumber)
    devices['section_id'] = devices['device_object'].apply(lambda x: x.SectionID)
    devices['longitude'] = devices['device_object'].apply(lambda x: float(cympy.study.QueryInfoDevice("CoordX", x.DeviceNumber, x.DeviceType)) / 100000)
    devices['latitude'] = devices['device_object'].apply(lambda x: float(cympy.study.QueryInfoDevice("CoordY", x.DeviceNumber, x.DeviceType)) / (1.26 * 100000))
    devices['distance'] = devices['device_object'].apply(lambda x: cympy.study.QueryInfoDevice("Distance", x.DeviceNumber, x.DeviceType))

    return devices
