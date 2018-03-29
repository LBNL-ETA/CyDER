import cympy

def open_study(modelfile):
    filename = "C:\\Users\\DRRC\\Desktop\\PGE_Models_DO_NOT_SHARE\\" + modelfile
    cympy.study.Open(filename)

def compute_loadflow():
    cympy.sim.LoadFlow().Run()

def model_info():
    model = {}
    model['longitude'] = 0
    model['latitude'] = 0
    return model

def list_nodes():
    list_nodes = cympy.study.ListNodes()
    nodes = []
    for node_object in list_nodes:
        node = {}
        node['node_object'] = node_object
        node['node_id'] = node_object.ID
        node['longitude'] = cympy.study.QueryInfoNode('Longitude', node_object.ID)
        node['latitude'] = cympy.study.QueryInfoNode('Latitude', node_object.ID)
        node['feeder'] = cympy.study.QueryInfoNode('FeederId', node_object.ID)

        #The following lines were used to import models accounting for the error in latitude in longitude values
        #This concerns model imports prior to 02/20/2018
        # node['longitude'] = node_object.X 
        # node['latitude'] = node_object.Y 
        # node['longitude'] = node_object.X / 100000
        # node['latitude'] = node_object.Y / (1.26 * 100000)
        nodes.append(node)
    return nodes

def list_sections():
    list_sections = cympy.study.ListSections()
    sections = []
    for section_object in list_sections:
        section = {}
        section['section_object'] = section_object
        section['section_id'] = section_object.ID
        section['from_node_id'] = section_object.FromNode.ID
        section['to_node_id'] = section_object.ToNode.ID
        sections.append(section)
    return sections

def list_devices(device_type=False):
    if device_type:
        list_devices = cympy.study.ListDevices(device_type)
    else:
        list_devices = cympy.study.ListDevices()
    devices = []
    for device_object in list_devices:
        device = {}
        device['device_object'] = device_object
        device['device_type'] = device_object.DeviceType
        device['device_number'] = device_object.DeviceNumber
        device['section_id'] = device_object.SectionID
        device['longitude'] = float(cympy.study.QueryInfoDevice("CoordX", device_object.DeviceNumber, device_object.DeviceType)) / 100000
        device['latitude'] = float(cympy.study.QueryInfoDevice("CoordY", device_object.DeviceNumber, device_object.DeviceType)) / (1.26 * 100000)
        device['distance'] = cympy.study.QueryInfoDevice("Distance", device_object.DeviceNumber, device_object.DeviceType)
        devices.append(device)

    return devices

def get_devices_details(devices):
    for device in devices:
        device_object = device['device_object']
        if device_object.DeviceType == 14: # Spot loads
            device['detail'] = {}
            for prop in ['SpotKWA', 'SpotKWB', 'SpotKWC']:
                x = cympy.study.QueryInfoDevice(prop, device_object.DeviceNumber, device_object.DeviceType)
                device['detail'][prop] = None if x is '' else float(x)
        elif device_object.DeviceType == 39: # PVs
            device['detail'] = {}
            for prop in ['PVActiveGeneration']:
                x = cympy.study.QueryInfoDevice(prop, device_object.DeviceNumber, device_object.DeviceType)
                device['detail'][prop] = None if x is '' else float(x)
    return devices

def get_voltages(nodes):
    # Require to call compute_loadflow() first
    for node in nodes:
        node_object = node['node_object']
        for prop in ['VA', 'VB', 'VC']:
            x = cympy.study.QueryInfoNode(prop, node_object.ID)
            node[prop] = None if x is '' else float(x)
    return nodes
