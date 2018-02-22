import datetime
import json
import pandas
import cympy


def cymdist(configuration_filename, time, input_names,
            input_values, scada, output_names, save_to_file):

    """Communicate with the FMU to launch a Cymdist simulation

    Args:
        configuration_filename (String): filename for the model configurations
        time (Integer): simulation time
        input_names (Strings): vector of input names
        input_values (Floats): vector of input values
        output_names (Strings): vector of output names
        save_to_file (1 or 0): save all nodes results to a file

    Example:
        >>> time = 0
        >>> save_to_file = 1
        >>> input_names = ['VMAG_A', 'VMAG_B', 'VMAG_C']
        >>> input_values = [2520, 2520, 2520]
        >>> configuration_filename = 'config.json'
        >>> output_names = ['IA', 'IAngleA', 'IB', 'IAngleB', 'IC', 'IAngleC']

    TODO:
        Create a test suite
        Create a version where substation model is open outside of this func
    """
    def _set_voltages(inputs, network):
        """Set the voltage at the source node from transmission grid"""
        # Set up the right voltage in [kV] (input must be [V])
        cympy.study.SetValueTopo(inputs['VMAG_A'] / 1000,
            "Sources[0].EquivalentSourceModels[0]" +
            ".EquivalentSource.OperatingVoltage1", network)
        cympy.study.SetValueTopo(inputs['VMAG_B'] / 1000,
            "Sources[0].EquivalentSourceModels[0]" +
            ".EquivalentSource.OperatingVoltage2", network)
        cympy.study.SetValueTopo(inputs['VMAG_C'] / 1000,
            "Sources[0].EquivalentSourceModels[0]" +
            ".EquivalentSource.OperatingVoltage3", network)

    def _run_load_allocation(feeder_loads, networks):
        """Allocate load with respect to the total demand recorded"""
        # Create Load Allocation object
        la = cympy.sim.LoadAllocation()

        for network in networks:
            # Create the Demand object
            demand = cympy.sim.Meter()
            demand.LoadValueType = cympy.enums.LoadValueType.KW_PF

            # Fill in the demand values
            demand.IsTotalDemand = False
            demand.DemandA = cympy.sim.LoadValue()
            demand.DemandA.Value1 = feeder_loads[network]['MW'] * 1000 / 3.0
            demand.DemandA.Value2 = 98
            demand.DemandB = cympy.sim.LoadValue()
            demand.DemandB.Value1 = feeder_loads[network]['MW'] * 1000 / 3.0
            demand.DemandB.Value2 = 98
            demand.DemandC = cympy.sim.LoadValue()
            demand.DemandC.Value1 = feeder_loads[network]['MW'] * 1000 / 3.0
            demand.DemandC.Value2 = 98

            # Set the first feeders demand
            la.SetDemand(network, demand)

        # Run the load allocation
        la.Run(networks)

    def _add_loads(loads):
        """Set active power load or production"""
        # Add load
        for index, (name, value) in enumerate(loads.items()):
            index = str(index)
            network_id = name.split('#')[0]
            node_id = name.split('#')[1]
            new_section = cympy.study.AddSection('MYSECTION' + index,  # Section ID
                                                 network_id,  # Network ID
                                                 'LOAD' + index,  # Load ID
                                                 cympy.enums.DeviceType.SpotLoad,
                                                 node_id,  # Node ID
                                                 'NEW_NODE' + index)

            # Get the number of phases on the section
            nb_phases = int(len(new_section.GetValue("Phase")))

            # Add load value divided by the number of phases
            for phase in range(0, nb_phases):
                cympy.study.SetValueDevice(float(value) / nb_phases,  # Load value
                    'CustomerLoads[0].CustomerLoadModels[0].' +
                    'CustomerLoadValues[' + str(phase) +
                    '].LoadValue.KW',  # Parameter to set
                    'LOAD' + index,  # Load ID
                    cympy.enums.DeviceType.SpotLoad)  # Load type

    def _output_values(output_names):
        """Query the right output name at the source node"""
        output = []
        for name in output_names:
            category = name.split('#')[1]
            node = name.split('#')[0]
            temp = cympy.study.QueryInfoNode(category, node)
            output.append(float(temp))
        return output

    # #########################################################################
    # Parse inputs
    # -------------------------------------------------------------------------
    # Open the configuration file and read the configurations
    with open(configuration_filename, 'r') as configuration_file:
        configuration = json.load(configuration_file)

    # Parse data from configuration file
    model_filename = configuration["model_filename"]  # 'BU0006.sxst'
    scada_filename = configuration["scada_filename"]  # 'scada.csv'
    substation_network = configuration["substation"]  # '2405'
    run_all_feeders = configuration['run_all_feeders']  # false/true
    feeders = configuration["feeders"]  # ['feeder1', 'feeder2', ...]

    # Do we need to open the SCADA file?
    if scada is None:
        scada = pandas.read_csv(scada_filename)

    # Create a dictionnary of inputs
    inputs = {}
    assert len(input_names) == len(input_values), "input name need to match value"
    for name, value in zip(input_names, input_values):
        inputs[name] = value

    # Parse inputs
    voltages = {}
    loads = {}
    for name, value in inputs.items():
        if 'VMAG' in name:
            voltages[name] = value
        elif 'VANG' in name:
            pass
        elif 'LOAD' in name or 'PV' in name:
            loads[name] = value
        else:
            raise Exception("Wrong input " + str(name))

    # Open/edit model and run power flow
    # -------------------------------------------------------------------------
    # Open the model
    cympy.study.Open(model_filename)

    # List all networks and remove substation
    if run_all_feeders:
        feeders = cympy.study.ListNetworks()
        feeders.remove(substation_network)

    # Set voltage at the substation head
    # Voltages are expected in V and converted to kV
    _set_voltages(voltages, substation_network)

    # Select load from SCADA and allocate to the feeder
    # Load are expected in MW and converted to kW
    feeder_loads = {}
    index = scada.index[scada.index.get_loc(time, method='nearest')]
    for feeder in feeders:
        feeder_loads[feeder] = {'MW': scada.loc[index, feeder + '_MW'],
                              'MVAR': scada.loc[index, feeder + '_MVAR']}
    _run_load_allocation(feeder_loads, feeders)

    # Set PVs
    _add_loads(loads)

    # Run the power flow
    lf = cympy.sim.LoadFlow()
    feeders_and_substation = list(feeders)
    feeders_and_substation.append(substation_network)
    lf.Run(feeders_and_substation)

    # Return the right values
    return _output_values(output_names)
