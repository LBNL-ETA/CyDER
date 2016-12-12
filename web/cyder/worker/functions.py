# -*- coding: utf-8 -*-
from __future__ import division
import pandas
import lookup
import pickle
import numpy as np
try:
    import cympy
    import btrdb
except:
    # Only installed on the Cymdist server
    pass


def fmu_wrapper(model_filename, input_values, input_names,
                output_names, output_device_names, write_result):
    """Communicate with the FMU to launch a Cymdist simulation

    Args:
        model_filename (String): path to the cymdist grid model
        input_values (List): list of float with the same order as input_names
        input_names (List): list of String to describe the list of values
        output_names (List): list of String output names [voltage_A, voltage_B, ...]
        output_device_names (List): list of String output device name (same lenght as output_names)
        write_result (Boolean): if True the entire results are saved to the file system (add ~30secs)

    Example:
        >>> write_results = 0  # (or False)
        >>> model_filename = 'HL0004.sxst'
        >>> input_names = ['VMAG_A', 'VMAG_B', 'VMAG_C', 'P_A', 'P_B', 'P_C', 'Q_A', 'Q_B', 'Q_C']
        >>> input_values = [7287, 7299, 7318, 7272, 2118, 6719, -284, -7184, 3564]
        >>> output_names = ['voltage_A', 'voltage_B', 'voltage_C']
        >>> output_device_names = ['HOLLISTER_2104', 'HOLLISTER_2104', 'HOLLISTER_2104']

        >>> fmu_wrapper(model_filename, input_values, input_names,
                        output_names, output_device_names, write_result)
    """

    # Open the model
    cympy.study.Open(model_filename)

    # Create a dictionary from the input values and input names
    udata = {}
    for name, value in zip(input_names, input_values):
        udata[name] = value

    # Run load allocation function to set input values
    load_allocation(udata)

    # Run the power flow
    lf = cympy.sim.LoadFlow()
    lf.Run()

    # Get the full output data <--- optimize this part to gain time
    devices = list_devices()
    devices = get_voltage(devices)
    devices = get_overload(devices)
    devices = get_load(devices)
    devices = get_unbalanced_line(devices)
    devices = get_distance(devices)

    # Write full results?
    if write_result:
        # Get the full output data (time consuming)
        temp = list_devices()
        temp = get_voltage(temp)
        temp = get_overload(temp)
        temp = get_load(temp)
        temp = get_unbalanced_line(temp)
        temp = get_distance(temp)
        with open(model_filename + '_result_.pickle', 'wb') as output_file:
            pickle.dump(temp, output_file, protocol=2)

    # Filter the result for the right outputs value
    output = []
    DEFAULT_VALUE = 0  # value to output in case of a NaN value
    for device_name, category in zip(output_device_names, output_names):
        temp = devices[devices.device_number == device_name][category]

        if not temp.isnull().any():
            output.append(temp.iloc[0])
        else:
            output.append(DEFAULT_VALUE)

    return output


def list_devices(device_type=False, verbose=False):
    """List all devices and return a break down of their type

    Args:
        device_type (Device): if passed then list of device with the same type
        verbose (Boolean): if True print result (default True)

    Return:
        DataFrame <device, device_type, device_number, device_type_id>
    """

    # Get the list of devices
    if device_type:
        devices = cympy.study.ListDevices(device_type)
    else:
        # Get all devices
        devices = cympy.study.ListDevices()

    # Create a dataframe
    devices = pandas.DataFrame(devices, columns=['device'])
    devices['device_type_id'] = devices['device'].apply(lambda x: x.DeviceType)
    devices['device_number'] = devices['device'].apply(lambda x: x.DeviceNumber)
    devices['device_type'] = devices['device_type_id'].apply(lambda x: lookup.type_table[x])

    # Get the break down of each type
    if verbose:
        unique_type = devices['device_type'].unique().tolist()
        for device_type in unique_type:
            print('There are ' + str(devices[devices.device_type == device_type].count()[0]) +
                  ' ' + device_type)

    return devices


def _describe_object(device):
        for value in cympy.dm.Describe(device.GetObjType()):
            print(value.Name)


def get_device(id, device_type, verbose=False):
    """Return a device

    Args:
        id (String): unique identifier
        device_type (DeviceType): type of device
        verbose (Boolean): describe an object

    Return:
        Device (Device)
    """
    # Get object
    device = cympy.study.GetDevice(id, device_type)

    # Describe attributes
    if verbose:
        _describe_object(device)

    return device


def add_device(device_name, device_type, section_id):
    """Return a device

    Args:
        device_name (String): unique identifier
        device_type (DeviceType): type of device
        section_id (String): unique identifier

    Return:
        Device (Device)
    """
    return cympy.study.AddDevice(device_name, device_type, section_id)


def add_pv(device_name, section_id, ns=100, np=100, location="To"):
    """Return a device

    Args:
        device_name (String): unique identifier
        section_id (String): unique identifier
        ns (Int): number of pannel in serie (* 17.3 to find voltage)
        np (Int): number of pannel in parallel (ns * np * 0.08 to find kW)
        location (String): To or From

    Return:
        Device (Device)
    """
    my_pv = add_device(device_name, cympy.enums.DeviceType.Photovoltaic, section_id)
    my_pv.SetValue(location, "Location")
    return my_pv


def load_allocation(values):
    """Run a load allocation

    Args:
        values (dictionnary): value1 (KVA) and value2 (PF) for A, B and C
    """

    # Create Load Allocation object
    la = cympy.sim.LoadAllocation()

    # Create the Demand object
    demand = cympy.sim.Meter()

    # Fill in the demand values
    demand.IsTotalDemand = False
    demand.DemandA = cympy.sim.LoadValue()
    demand.DemandA.Value1 = values['P_A']
    demand.DemandA.Value2 = values['Q_A']
    demand.DemandB = cympy.sim.LoadValue()
    demand.DemandB.Value1 = values['P_B']
    demand.DemandB.Value2 = values['Q_B']
    demand.DemandC = cympy.sim.LoadValue()
    demand.DemandC.Value1 = values['P_C']
    demand.DemandC.Value2 = values['Q_C']
    demand.LoadValueType = cympy.enums.LoadValueType.KW_KVAR

    # Get a list of networks
    networks = cympy.study.ListNetworks()

    # Set the first feeders demand
    la.SetDemand(networks[0], demand)

    # Set up the right voltage [V to kV]
    cympy.study.SetValueTopo(values['VMAG_A'] / 1000,
        "Sources[0].EquivalentSourceModels[0].EquivalentSource.OperatingVoltage1", networks[0])
    cympy.study.SetValueTopo(values['VMAG_B'] / 1000,
        "Sources[0].EquivalentSourceModels[0].EquivalentSource.OperatingVoltage2", networks[0])
    cympy.study.SetValueTopo(values['VMAG_C'] / 1000,
        "Sources[0].EquivalentSourceModels[0].EquivalentSource.OperatingVoltage3", networks[0])

    # Run the load allocation
    la.Run([networks[0]])


def get_voltage(devices):
    """
    Args:
        devices (DataFrame): list of all the devices to include

    Return:
        devices_voltage (DataFrame): devices and their corresponding voltage for
            each phase
    """
    # Create a new frame to hold the results
    voltage = devices.copy()

    # Reset or create new columns to hold the result
    voltage['voltage_A'] = [0] * len(voltage)
    voltage['voltage_B'] = [0] * len(voltage)
    voltage['voltage_C'] = [0] * len(voltage)

    for device in devices.itertuples():
        # Get the according voltage per phase in a pandas dataframe
        voltage.loc[device.Index, 'voltage_A'] = cympy.study.QueryInfoDevice(
            "VpuA", device.device_number, int(device.device_type_id))
        voltage.loc[device.Index, 'voltage_B'] = cympy.study.QueryInfoDevice(
            "VpuB", device.device_number, int(device.device_type_id))
        voltage.loc[device.Index, 'voltage_C'] = cympy.study.QueryInfoDevice(
            "VpuC", device.device_number, int(device.device_type_id))

    # Cast the right type
    for column in ['voltage_A', 'voltage_B', 'voltage_C']:
        voltage[column] = voltage[column].apply(lambda x: None if x is '' else float(x))

    return voltage


def get_overload(devices):
    """
    Args:
        devices (DataFrame): list of all the devices to include
        first_n_devices (Int): number of row to return

    Return:
        overload_device (DataFrame): return the n devices with the highest load
    """
    # Create a new frame to hold the results
    overload = devices.copy()

    # Reset or create new columns to hold the result
    overload['overload_A'] = [0] * len(overload)
    overload['overload_B'] = [0] * len(overload)
    overload['overload_C'] = [0] * len(overload)

    for device in devices.itertuples():
        # Get the according overload per phase in a pandas dataframe
        overload.loc[device.Index, 'overload_A'] = cympy.study.QueryInfoDevice(
            "OverloadAmpsA", device.device_number, int(device.device_type_id))
        overload.loc[device.Index, 'overload_B'] = cympy.study.QueryInfoDevice(
            "OverloadAmpsB", device.device_number, int(device.device_type_id))
        overload.loc[device.Index, 'overload_C'] = cympy.study.QueryInfoDevice(
            "OverloadAmpsC", device.device_number, int(device.device_type_id))

    # Cast the right type
    for column in ['overload_A', 'overload_B', 'overload_C']:
        overload[column] = overload[column].apply(lambda x: None if x is '' else float(x))

    return overload


def get_load(devices):
    """
    Args:
        devices (DataFrame): list of all the devices to include

    Return:
        devices_voltage (DataFrame): devices and their corresponding load for
            each phase
    """
    # Create a new frame to hold the results
    load = devices.copy()

    # Reset or create new columns to hold the result
    load['MWA'] = [0] * len(load)
    load['MWB'] = [0] * len(load)
    load['MWC'] = [0] * len(load)
    load['MWTOT'] = [0] * len(load)
    load['MVARA'] = [0] * len(load)
    load['MVARB'] = [0] * len(load)
    load['MVARC'] = [0] * len(load)
    load['MVARTOT'] = [0] * len(load)

    for device in devices.itertuples():
        # Get the according load per phase in a pandas dataframe
        load.loc[device.Index, 'MWA'] = cympy.study.QueryInfoDevice(
            "MWA", device.device_number, int(device.device_type_id))
        load.loc[device.Index, 'MWB'] = cympy.study.QueryInfoDevice(
            "MWB", device.device_number, int(device.device_type_id))
        load.loc[device.Index, 'MWC'] = cympy.study.QueryInfoDevice(
            "MWC", device.device_number, int(device.device_type_id))
        load.loc[device.Index, 'MWTOT'] = cympy.study.QueryInfoDevice(
            "MWTOT", device.device_number, int(device.device_type_id))
        load.loc[device.Index, 'MVARA'] = cympy.study.QueryInfoDevice(
            "MVARA", device.device_number, int(device.device_type_id))
        load.loc[device.Index, 'MVARB'] = cympy.study.QueryInfoDevice(
            "MVARB", device.device_number, int(device.device_type_id))
        load.loc[device.Index, 'MVARC'] = cympy.study.QueryInfoDevice(
            "MVARC", device.device_number, int(device.device_type_id))
        load.loc[device.Index, 'MVARTOT'] = cympy.study.QueryInfoDevice(
            "MVARTOT", device.device_number, int(device.device_type_id))

    # Cast the right type
    for column in ['MWA', 'MWB', 'MWC', 'MWTOT', 'MVARA', 'MVARB', 'MVARC', 'MVARTOT']:
        load[column] = load[column].apply(lambda x: None if x is '' else float(x))

    return load


def get_distance(devices):
    """
    Args:
        devices (DataFrame): list of all the devices to include

    Return:
        devices_distance (DataFrame): devices and their corresponding distance from the substation
    """
    distance = devices.copy()

    # Reset or create new columns to hold the result
    distance['distance'] = [0] * len(distance)

    for device in devices.itertuples():
        # Get the according distance in a pandas dataframe
        distance.loc[device.Index, 'distance'] = cympy.study.QueryInfoDevice(
            "Distance", device.device_number, int(device.device_type_id))

    # Cast the right type
    for column in ['distance']:
        distance[column] = distance[column].apply(lambda x: None if x is '' else float(x))

    return distance


def get_unbalanced_line(devices):
    """This function requires the get_voltage function has been called before

    Args:
        devices (DataFrame): list of all the devices to include
        first_n_devices (Int): number of row to return

    Return:
        overload_device (DataFrame): return the n devices with the highest load
    """
    # Get all the voltage
    voltage = get_voltage(devices)

    # Get the mean voltage accross phase
    voltage['mean_voltage_ABC'] = voltage[['voltage_A', 'voltage_B', 'voltage_C']].mean(axis=1)

    # Get the max difference of the three phase voltage with the mean
    def _diff(value):
        diff = []
        for phase in ['voltage_A', 'voltage_B', 'voltage_C']:
            diff.append(abs(value[phase] - value['mean_voltage_ABC']) * 100 / value['mean_voltage_ABC'])
        return max(diff)
    voltage['diff_with_mean'] = voltage[['mean_voltage_ABC', 'voltage_A', 'voltage_B', 'voltage_C']].apply(_diff, axis=1)

    return voltage


def get_upmu_data(inputdt, upmu_path):
    """ Retrieves instantaneous P, Q, and voltage magnitude for specified datetime.

    Args:
        inputdt (datetime): timezone aware datetime object
        upmu_path (str): e.g., '/LBNL/grizzly_bus1/'
    Returns:
        {'P_A': , 'Q_A': , 'P_B': , 'Q_B': , 'P_C': , 'Q_C': ,
         'units': ('kW', 'kVAR'),
         'VMAG_A': , 'VMAG_B': , 'VMAG_C': }
    """

    bc = btrdb.HTTPConnection("miranda.cs.berkeley.edu")
    ur = btrdb.UUIDResolver("miranda.cs.berkeley.edu", "uuidresolver", "uuidpass", "upmu")

    # convert dt to nanoseconds since epoch
    epochns = btrdb.date(inputdt.strftime('%Y-%m-%dT%H:%M:%S'))

    # retrieve raw data from btrdb
    upmu_data = {}
    streams = ['L1MAG', 'L2MAG', 'L3MAG', 'C1MAG', 'C2MAG', 'C3MAG', 'L1ANG', 'L2ANG', 'L3ANG', 'C1ANG', 'C2ANG', 'C3ANG']
    for s in streams:
        pt = bc.get_stat(ur.resolve(upmu_path + s), epochns, epochns + int(9e6))
        upmu_data[s] = pt[0][2]

    output_dict = {}

    output_dict['P_A'] = (upmu_data['L1MAG']*upmu_data['C1MAG']*np.cos(upmu_data['L1ANG'] - upmu_data['C1ANG']))*1e-3
    output_dict['Q_A'] = (upmu_data['L1MAG']*upmu_data['C1MAG']*np.sin(upmu_data['L1ANG'] - upmu_data['C1ANG']))*1e-3

    output_dict['P_B'] = (upmu_data['L2MAG']*upmu_data['C2MAG']*np.cos(upmu_data['L2ANG'] - upmu_data['C2ANG']))*1e-3
    output_dict['Q_B'] = (upmu_data['L2MAG']*upmu_data['C2MAG']*np.sin(upmu_data['L2ANG'] - upmu_data['C2ANG']))*1e-3

    output_dict['P_C'] = (upmu_data['L3MAG']*upmu_data['C3MAG']*np.cos(upmu_data['L3ANG'] - upmu_data['C3ANG']))*1e-3
    output_dict['Q_C'] = (upmu_data['L3MAG']*upmu_data['C3MAG']*np.sin(upmu_data['L3ANG'] - upmu_data['C3ANG']))*1e-3

    output_dict['units'] = ('kW', 'kVAR', 'V')

    output_dict['VMAG_A'] = upmu_data['L1MAG']
    output_dict['VMAG_B'] = upmu_data['L2MAG']
    output_dict['VMAG_C'] = upmu_data['L3MAG']
    return output_dict
