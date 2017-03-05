from __future__ import division
from pyfmi import load_fmu
from pyfmi.master import Master
from datetime import datetime
import string
import random
import pdb
import json
import cymdist
import matplotlib
import matplotlib.pyplot as plt
plt.switch_backend('Qt4Agg')
import numpy as np
import time
try:
    import cympy
except:
    # Only installed on the Cymdist server
    pass
import seaborn
seaborn.set_style("whitegrid")
seaborn.despine()
plt.close()


def initialize_configuration(times, model_names):
    configuration = {'times': times,
                     'interpolation_method': 'closest_time',
                     'models': []
                     }

    for time, model_name in zip(times, model_names):
        model = {
           'filename': 'D://Users//Jonathan//Documents//GitHub//PGE_Models_DO_NOT_SHARE//' + model_name,
           'new_loads': [],
           'set_loads': [],
           'new_pvs': [],
           'set_pvs': [],
           }
        configuration['models'].append(model)
    return configuration


def shift_load_and_pv(load_profile, pv_profile, configuration):
    """Extend the configuration file with load and pv shift"""
    # Open model and get the devices from the first model
    cympy.study.Open(configuration['models'][0]['filename'])
    loads = cymdist.list_loads()
    pvs = cymdist.list_pvs()

    for index, time in enumerate(configuration['times']):
        # Set new pv generation
        for pv in pvs.itertuples():
            configuration['models'][index]['set_pvs'].append({'device_number': pv.device_number,
                                                              'generation': pv.generation * pv_profile[index]})
        # Set new load demand
        for load in loads.iterrows():
            _, load = load
            configuration['models'][index]['set_loads'].append({'device_number': load['device_number'],
                                                                'active_power': []})
            for phase_index in ['0', '1', '2']:
                if load['activepower_' + phase_index]:
                    configuration['models'][index]['set_loads'][-1]['active_power'].append({'active_power': float(load['activepower_' + phase_index]) * load_profile[index],
                                                                                            'phase_index': phase_index,
                                                                                            'phase': str(load['phase_' + phase_index])})
    return configuration


def ev_consumption(ev_profile, configuration):
    """Extend the configuration file with load and pv shift"""
    # Open model and get the devices from the first model
    cympy.study.Open(configuration['models'][0]['filename'])
    loads = cymdist.list_loads()

    # randomnly pick ev_profile max(ev_profile) loads
    loads = loads.sample(n=max(ev_profile))

    for index, time in enumerate(configuration['times']):
        # randomnly pick a subset of loads that correspond to ev_profile(index)
        loads_2 = loads.sample(n=ev_profile[index])

        # Set new load demand
        for load in loads_2.iterrows():
            _, load = load
            configuration['models'][index]['set_loads'].append({'device_number': load['device_number'],
                                                                'active_power': []})
            # Dummy way to count the phases
            phase_count = 0
            for phase_index in ['0', '1', '2']:
                if load['activepower_' + phase_index]:
                    phase_count += 1

            power = 6.6 / phase_count
            for phase_index in ['0', '1', '2']:
                if load['activepower_' + phase_index]:
                    configuration['models'][index]['set_loads'][-1]['active_power'].append({'active_power': float(load['activepower_' + phase_index]) + power,
                                                                                            'phase_index': phase_index,
                                                                                            'phase': str(load['phase_' + phase_index])})
    return configuration


def create_configuration_file(configurations):
    """
    Input:
    configuration = {
                     'times': [0],
                     'interpolation_method': 'closest_time',
                     'models': [{
                        'filename': 'D://Users//Jonathan//Documents//GitHub//PGE_Models_DO_NOT_SHARE//BU0001.sxst',
                        'new_loads': [{
                                'section_id': '800033503',
                                'active_power': 100
                            }],
                        'set_loads': [{
                                'device_name': 'name',
                                'active_power': 100
                            }],
                        'new_pvs': [{
                                'section_id': '800033503',
                                'generation': 100
                            }],
                        'set_pvs': [{
                                'device_name': 'name',
                                'generation': 100
                            }]
                        }
                    ]}
    Return configuration filename
    """
    # Generate random filename
    parent_path = 'D://Users//Jonathan//Documents//GitHub//configuration_files//'
    random_string = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(10))
    random_string += '_config.json'
    filename = parent_path + random_string

    with open(filename, 'w') as outfile:
        json.dump(configurations, outfile)

    return filename


def simulate_cymdist_gridyn_fmus(configuration_filename, start_time, end_time, save_to_file=0):
    """Simulate one CYMDIST FMU.

    """
    # Parameters which will be arguments of the function
    start_time = start_time
    stop_time  = end_time
    step_size = 1

    # Path to configuration file
    path_config=configuration_filename
    cymdist_con_val_str = bytes(path_config, 'utf-8')

    griddyn_input_valref=[]
    griddyn_output_valref=[]
    griddyn_output_values=[]

    cymdist_input_valref=[]
    cymdist_output_valref=[]
    cymdist_output_values=[]

    cymdist = load_fmu("C:/cygwin64/home/Jonathan/project_cyder/web/docker_django/worker/simulation/fmu_code/CYMDIST.fmu", log_level=7)
    griddyn=load_fmu("C:/cygwin64/home/Jonathan/project_cyder/web/docker_django/worker/simulation/fmu_code/griddyn14bus.fmu", log_level=7)

    cymdist.setup_experiment(start_time=start_time, stop_time=stop_time)
    griddyn.setup_experiment(start_time=start_time, stop_time=stop_time)

    # Define the inputs
    cymdist_input_names = ['VMAG_A', 'VMAG_B', 'VMAG_C', 'VANG_A', 'VANG_B', 'VANG_C']
    #cymdist_input_values = [2520, 2520, 2520, 0, -120, 120]
    cymdist_output_names = ['IA', 'IB', 'IC', 'IAngleA', 'IAngleB', 'IAngleC']

    griddyn_input_names = ['Bus11_IA', 'Bus11_IB', 'Bus11_IC',
                       'Bus11_IAngleA', 'Bus11_IAngleB', 'Bus11_IAngleC']
    #griddyn_input_values = [277.6, 200.1, 173.1, -13.7, -130.51, 111.93]
    griddyn_output_names = ['Bus11_VA', 'Bus11_VB', 'Bus11_VC',
                'Bus11_VAngleA', 'Bus11_VAngleB', 'Bus11_VAngleC']

    # Get the value references of griddyn inputs
    for elem in griddyn_input_names:
        griddyn_input_valref.append(griddyn.get_variable_valueref(elem))

    # Get the value references of griddyn outputs
    for elem in griddyn_output_names:
        griddyn_output_valref.append(griddyn.get_variable_valueref(elem))

    # Get the value references of cymdist inputs
    for elem in cymdist_input_names:
        cymdist_input_valref.append(cymdist.get_variable_valueref(elem))

    # Get the value references of cymdist outputs
    for elem in cymdist_output_names:
        cymdist_output_valref.append(cymdist.get_variable_valueref(elem))

    # Set the flag to save the results
    cymdist.set("save_to_file", save_to_file)
    # Get the initial outputs from griddyn
    # griddyn_output_values = (griddyn.get_real(griddyn_output_valref))
    # Set the initial outputs of GridDyn in cymdist
    # cymdist.set_real (cymdist_input_valref, griddyn_output_values)
    # Get value reference of the configuration file
    cymdist_con_val_ref = cymdist.get_variable_valueref("conFilNam")

    # Set the configuration file
    cymdist.set_string([cymdist_con_val_ref], [cymdist_con_val_str])

    # Verify that the multiplier is set
    print ("This is the multiplier before it is set " + str(griddyn.get('multiplier')))

    # Set the value of the multiplier
    griddyn.set('multiplier', 3.0)

    # Verify that the multiplier is set
    print ("This is the multiplier after it is set " + str(griddyn.get('multiplier')))

    # Initialize the FMUs
    cymdist.initialize()
    griddyn.initialize()

    # Create vector to store time
    simTim=[]
    CYMDIST_IA = []
    GRIDDYN_VA = []

    # Interactive mode on
    plt.ion()

    # Create the plot
    fig = plt.figure()
    ax1 = fig.add_subplot(211)
    ax2 = fig.add_subplot(212)
    ax1.set_ylabel('IA (cymDist) [A]')
    ax2.set_ylabel('Bus_11 VA (GridDyn) [V]')
    ax2.set_xlabel('Time (seconds)')
    line1, = ax1.plot(simTim, CYMDIST_IA, 'b-')
    line2, = ax2.plot(simTim, GRIDDYN_VA, 'r-')

    # Co-simulation loop
    for index, tim in enumerate(np.arange(start_time, stop_time, step_size)):

        # Get the outputs from griddyn
        griddyn_output_values = (griddyn.get_real(griddyn_output_valref))

        cymdist.set_real(cymdist_input_valref, griddyn_output_values)
        cymdist.do_step(current_t=tim, step_size=step_size, new_step=0)
        cymdist_output_values = (cymdist.get_real(cymdist_output_valref))

        griddyn.set_real(griddyn_input_valref, cymdist_output_values)
        griddyn.do_step(current_t=tim, step_size=step_size, new_step=0)

        CYMDIST_IA.append(cymdist.get_real(cymdist.get_variable_valueref('IA')))
        GRIDDYN_VA.append(griddyn.get_real(griddyn.get_variable_valueref('Bus11_VA')))
        simTim.append(tim)

        line1.set_xdata(simTim)
        line1.set_ydata(CYMDIST_IA)
        line2.set_xdata(simTim)
        line2.set_ydata(GRIDDYN_VA)
        ax1.relim()
        ax1.autoscale_view(True,True,True)
        ax2.relim()
        ax2.autoscale_view(True,True,True)
        fig.canvas.draw()
        plt.pause(0.01)

    pdb.set_trace()
    # close figure automatically
    plt.close()

    # Terminate FMUs
    cymdist.terminate()
    griddyn.terminate()
    return {'result': 'some stuff'}
