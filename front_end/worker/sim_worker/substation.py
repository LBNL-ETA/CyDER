import cympy
import pandas

class Substation(object):
    """"""
    def __init__(self, model_filename):
        """"""
        # Open the model
        self.model_filename = model_filename
        cympy.study.Open(self.model_filename)

    def baseload_allocation(self, feeder_loads):
        """Allocate load with respect to the total demand recorded"""
        # Create Load Allocation object
        la = cympy.sim.LoadAllocation()

        for feeder in list(feeder_loads.keys()):
            # Create the Demand object
            demand = cympy.sim.Meter()
            demand.LoadValueType = cympy.enums.LoadValueType.KW_PF

            # Fill in the demand values
            demand.IsTotalDemand = False
            demand.DemandA = cympy.sim.LoadValue()
            demand.DemandA.Value1 = feeder_loads[feeder]['MW'] * 1000 / 3.0
            demand.DemandA.Value2 = 98
            demand.DemandB = cympy.sim.LoadValue()
            demand.DemandB.Value1 = feeder_loads[feeder]['MW'] * 1000 / 3.0
            demand.DemandB.Value2 = 98
            demand.DemandC = cympy.sim.LoadValue()
            demand.DemandC.Value1 = feeder_loads[feeder]['MW'] * 1000 / 3.0
            demand.DemandC.Value2 = 98

            # Set the first feeders demand
            la.SetDemand(feeder, demand)

        # Run the load allocation
        la.Run(list(feeder_loads.keys()))

    def add_power_devices(self, node_ids, network_ids, device_ids):
        """"""
        # Add section with spot loads
        for node, network, device in zip(node_ids, network_ids, device_ids):
            new_section = cympy.study.AddSection('MYSECTION' + device,  # Section ID
                                                 network,  # Network ID
                                                 device,  # Load ID
                                                 cympy.enums.DeviceType.SpotLoad,
                                                 node,  # Node ID
                                                 'NEW_NODE_from' + node)


    def set_power_devices(self, device_ids, values):
        """"""
        # Get active load model
        activeLoadModel = cympy.study.GetActiveLoadModel()

        for device_id, value in zip(device_ids, values):
            # Get device
            device = cympy.study.GetDevice(device_id, cympy.enums.DeviceType.SpotLoad)

            # Get the number of phases for the device
            section = cympy.study.GetSection(device.SectionID)
            nb_phases = int(len(section.GetValue("Phase")))

            # Add load value divided by the number of phases
            for phase in range(0, nb_phases):
                cympy.study.SetValueDevice(float(value) / nb_phases,  # Load value
                    'CustomerLoads[0].CustomerLoadModels.Get(' +
                    str(activeLoadModel.ID) + ').' +  # Active load model (August)
                    'CustomerLoadValues[' + str(phase) +  # Phase
                    '].LoadValue.KW',  # Parameter to set
                    device_id,  # Load ID
                    cympy.enums.DeviceType.SpotLoad)  # Load type

    def run_powerflow(self, feeders):
        """"""
        # Run the power flow
        lf = cympy.sim.LoadFlow()
        lf.Run(list(feeders))

    def list_nodes(self):
        """List all the nodes
        Return:
            a DataFrame with section_id, node_id, latitude and longitude
        """

        # Get all nodes
        nodes = cympy.study.ListNodes()

        # Create a frame
        nodes = pandas.DataFrame(nodes, columns=['node_object'])
        nodes['node_id'] = nodes['node_object'].apply(lambda x: x.ID)

        nodes['section_id'] = [0] * len(nodes)
        nodes['network_id'] = [0] * len(nodes)
        nodes['latitude'] = [0] * len(nodes)
        nodes['longitude'] = [0] * len(nodes)
        nodes['distance'] = [0] * len(nodes)

        for node in nodes.itertuples():
            nodes.loc[node.Index, 'section_id'] = cympy.study.QueryInfoNode("SectionId", node.node_id)
            nodes.loc[node.Index, 'latitude'] = cympy.study.QueryInfoNode("CoordY", node.node_id)
            nodes.loc[node.Index, 'longitude'] = cympy.study.QueryInfoNode("CoordX", node.node_id)
            nodes.loc[node.Index, 'distance'] = cympy.study.QueryInfoNode("Distance", node.node_id)
            nodes.loc[node.Index, 'network_id'] = cympy.study.QueryInfoNode("NetworkId", node.node_id)

        # Cast the right type
        for column in ['latitude']:
            nodes[column] = nodes[column].apply(lambda x: None if x is '' else float(x) / (1.26 * 100000))

        # Cast the right type
        for column in ['longitude']:
            nodes[column] = nodes[column].apply(lambda x: None if x is '' else float(x) / (100000))

        # Cast the right type
        for column in ['distance']:
            nodes[column] = nodes[column].apply(lambda x: None if x is '' else float(x))
        return nodes



    def get_voltage(self, frame):
        """
        Args:
            devices (DataFrame): list of all the devices or nodes to include
        Return:
            devices_voltage (DataFrame): devices and their corresponding voltage for
                each phase
        """
        # Create a new frame to hold the results
        voltage = frame.copy()

        # Reset or create new columns to hold the result
        voltage['voltage_A'] = [0] * len(voltage)
        voltage['voltage_B'] = [0] * len(voltage)
        voltage['voltage_C'] = [0] * len(voltage)

        for value in frame.itertuples():
            # Get the according voltage per phase in a pandas dataframe
            voltage.loc[value.Index, 'voltage_A'] = cympy.study.QueryInfoNode("VpuA", value.node_id)
            voltage.loc[value.Index, 'voltage_B'] = cympy.study.QueryInfoNode("VpuB", value.node_id)
            voltage.loc[value.Index, 'voltage_C'] = cympy.study.QueryInfoNode("VpuC", value.node_id)

        # Cast the right type
        for column in ['voltage_A', 'voltage_B', 'voltage_C']:
            voltage[column] = voltage[column].apply(lambda x: None if x is '' else float(x))
        return voltage

    def get_voltage_from_node_ids(self, node_ids):
        """
        Args:
            node_ids (List): node ids
        Return:
            node_voltage (List)
        """
        voltages = []
        for node_id in node_ids:
            voltages.append(cympy.study.QueryInfoNode("Vpu", node_id))
        return voltages

    def get_info_node(self, node, info):
        """"""
        return cympy.study.QueryInfoNode(info, node)
