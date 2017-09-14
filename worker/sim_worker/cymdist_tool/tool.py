# -*- coding: utf-8 -*-
from __future__ import division
import pandas
from . import type_lookup as lookup
import pickle
import numpy as np
import json
try:
    import cympy
except:
    # Only installed on the Cymdist server
    pass


def list_loads():
    """List all the loads and their demand on each phase"""
    # Get a list of all the loads
    devices = list_devices(device_type=14)

    # Get their active power on each phase
    devices['phase_0'] = [0] * len(devices)
    devices['phase_1'] = [0] * len(devices)
    devices['phase_2'] = [0] * len(devices)
    devices['activepower_0'] = [0] * len(devices)
    devices['activepower_1'] = [0] * len(devices)
    devices['activepower_2'] = [0] * len(devices)

    for value in devices.itertuples():
        for index in [0, 1, 2]:
            try:
                devices.loc[value.Index, 'activepower_' + str(index)] = cympy.study.GetValueDevice(
                    'CustomerLoads[0].CustomerLoadModels[0].CustomerLoadValues[' + str(index) + '].LoadValue.KW',
                    value.device_number, int(value.device_type_id))
            except:
                devices.loc[value.Index, 'activepower_' + str(index)] = False

            try:
                devices.loc[value.Index, 'phase_' + str(index)] = cympy.study.GetValueDevice(
                    'CustomerLoads[0].CustomerLoadModels[0].CustomerLoadValues[' + str(index) + '].Phase',
                    value.device_number, int(value.device_type_id))
            except:
                devices.loc[value.Index, 'phase_' + str(index)] = False
    return devices


def list_pvs():
    """List all the PVs and their demand"""
    # Get a list of all the loads
    devices = list_devices(device_type=39)

    # Get their generation on each phase
    devices['generation'] = [0] * len(devices)

    for value in devices.itertuples():
        # Get the according voltage per phase in a pandas dataframe
        devices.loc[value.Index, 'generation'] = cympy.study.QueryInfoDevice(
            'PVActiveGeneration', value.device_number, int(value.device_type_id))

    # Cast the right type
    for column in ['generation']:
        devices[column] = devices[column].apply(lambda x: 0 if x is '' else float(x))
    return devices


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


def list_nodes():
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
    nodes['latitude'] = [0] * len(nodes)
    nodes['longitude'] = [0] * len(nodes)
    nodes['distance'] = [0] * len(nodes)

    for node in nodes.itertuples():
        nodes.loc[node.Index, 'section_id'] = cympy.study.QueryInfoNode("SectionId", node.node_id)
        nodes.loc[node.Index, 'latitude'] = cympy.study.QueryInfoNode("CoordY", node.node_id)
        nodes.loc[node.Index, 'longitude'] = cympy.study.QueryInfoNode("CoordX", node.node_id)
        nodes.loc[node.Index, 'distance'] = cympy.study.QueryInfoNode("Distance", node.node_id)

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


def get_voltage(frame, is_node=False):
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
        if not is_node:
            # Get the according voltage per phase in a pandas dataframe
            voltage.loc[value.Index, 'voltage_A'] = cympy.study.QueryInfoDevice(
                "VpuA", value.device_number, int(value.device_type_id))
            voltage.loc[value.Index, 'voltage_B'] = cympy.study.QueryInfoDevice(
                "VpuB", value.device_number, int(value.device_type_id))
            voltage.loc[value.Index, 'voltage_C'] = cympy.study.QueryInfoDevice(
                "VpuC", value.device_number, int(value.device_type_id))
        else:
            # Get the according voltage per phase in a pandas dataframe
            voltage.loc[value.Index, 'voltage_A'] = cympy.study.QueryInfoNode("VpuA", value.node_id)
            voltage.loc[value.Index, 'voltage_B'] = cympy.study.QueryInfoNode("VpuB", value.node_id)
            voltage.loc[value.Index, 'voltage_C'] = cympy.study.QueryInfoNode("VpuC", value.node_id)

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


def get_coordinates(devices):
    """
    Args:
        devices (DataFrame): list of all the devices to include

    Return:
        devices_distance (DataFrame): devices and their corresponding latitude
        and longitude from the substation
    """
    coordinates = devices.copy()

    # Reset or create new columns to hold the result
    coordinates['latitude'] = [0] * len(coordinates)
    coordinates['longitude'] = [0] * len(coordinates)
    coordinates['section_id'] = [0] * len(coordinates)

    for device in devices.itertuples():
        # Get the according latitude in a pandas dataframe
        coordinates.loc[device.Index, 'latitude'] = cympy.study.QueryInfoDevice(
            "CoordY", device.device_number, int(device.device_type_id))

        # Get the according longitude in a pandas dataframe
        coordinates.loc[device.Index, 'longitude'] = cympy.study.QueryInfoDevice(
            "CoordX", device.device_number, int(device.device_type_id))

        # Get the section id in a pandas dataframe
        coordinates.loc[device.Index, 'section_id'] = cympy.study.QueryInfoDevice(
            "SectionId", device.device_number, int(device.device_type_id))

    # Cast the right type
    for column in ['latitude']:
        coordinates[column] = coordinates[column].apply(lambda x: None if x is '' else float(x) / (1.26 * 100000))

    # Cast the right type
    for column in ['longitude']:
        coordinates[column] = coordinates[column].apply(lambda x: None if x is '' else float(x) / (100000))

    return coordinates


def get_unbalanced_line(devices):
    """This function requires the get_voltage function has been called before.

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

def get_sections(devices):
    """
    Args:
        devices (DataFrame): list of all the devices to include

    Return:
        devices_section (DataFrame): devices and their section info (from node and to node)
    """
    sections = devices.copy()

    # Reset or create new columns to hold the result
    sections['from'] = [0] * len(sections)
    sections['to'] = [0] * len(sections)

    for device in devices.itertuples():
        # Get the according latitude in a pandas dataframe
        sections.loc[device.Index, 'from'] = cympy.study.QueryInfoDevice(
            "FromNodeId", device.device_number, int(device.device_type_id))

        # Get the according longitude in a pandas dataframe
        sections.loc[device.Index, 'to'] = cympy.study.QueryInfoDevice(
            "ToNodeId", device.device_number, int(device.device_type_id))
    
    return sections
