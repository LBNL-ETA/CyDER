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
from matplotlib.ticker import FormatStrFormatter
import matplotlib.pyplot as plt
plt.switch_backend('Qt4Agg')
import numpy as np
import time
import pandas
try:
    import cympy
except:
    # Only installed on the Cymdist server
    pass
import seaborn
seaborn.set_style("whitegrid")
seaborn.despine()
plt.close()


def initialize_configuration(times, parent_folder, model_names):
    configuration = {'times': times,
                     'interpolation_method': 'closest_time',
                     'models': []
                     }

    for time, model_name in zip(times, model_names):
        model = {
           'filename': parent_folder + model_name,
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


def create_configuration_file(configurations, output_folder):
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
    random_string = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(10))
    random_string += '_config.json'
    filename = output_folder + random_string

    with open(filename, 'w') as outfile:
        json.dump(configurations, outfile)

    return filename


def simulate_cymdist_gridyn_fmus(configuration_filename, start_time, end_time, step_size, _saveToFile=0, input_profiles=False, x_axis_labels=False):
    """Simulate one CYMDIST FMU.

    """
    # Parameters which will be arguments of the function
    start_time = start_time
    stop_time  = end_time
    step_size = step_size

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
    cymdist.set("_saveToFile", _saveToFile)
    #cymdist.set("_communicationStepSize", step_size)
    # Get the initial outputs from griddyn
    # griddyn_output_values = (griddyn.get_real(griddyn_output_valref))
    # Set the initial outputs of GridDyn in cymdist
    # cymdist.set_real (cymdist_input_valref, griddyn_output_values)
    # Get value reference of the configuration file
    cymdist_con_val_ref = cymdist.get_variable_valueref("_configurationFileName")

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
    
    # Call event update prior to entering continuous mode.
    cymdist.event_update()
    cymdist.enter_continuous_time_mode()

    # Create vector to store time
    simTim=[]
    CYMDIST_IA = []
    CYMDIST_IB = []
    CYMDIST_IC = []
    GRIDDYN_VA = []
    GRIDDYN_VB = []
    GRIDDYN_VC = []

    # Interactive mode on
    plt.ion()

    # Create the plot
    fig = plt.figure()
    ax = fig.add_subplot(311)
    ax1 = fig.add_subplot(312)
    ax2 = fig.add_subplot(313)
    ax.set_ylabel('Inputs')
    ax1.set_ylabel('Feeder currents\n(cymDist) [A]')
    ax2.set_ylabel('Feeder voltages\n(GridDyn) [V]')
    ax2.yaxis.set_major_formatter(FormatStrFormatter('%.3f'))
    ax2.set_xlabel('Time (minutes)')
    if input_profiles:
        for input_profile in input_profiles:
            line, = ax.plot(input_profile['x'], input_profile['y'], label=input_profile['label'])
    line1A, = ax1.plot(simTim, CYMDIST_IA, label='Phase A')
    line1B, = ax1.plot(simTim, CYMDIST_IB, label='Phase B')
    line1C, = ax1.plot(simTim, CYMDIST_IC, label='Phase C')
    line2A, = ax2.plot(simTim, GRIDDYN_VA, label='Phase A')
    line2B, = ax2.plot(simTim, GRIDDYN_VB, label='Phase B')
    line2C, = ax2.plot(simTim, GRIDDYN_VC, label='Phase C')
    ax.legend(loc=0)
    ax1.legend(loc=1)
    ax2.legend(loc=1)
    fig.tight_layout()

    # # Save all the result to a pandas dataframe
    # cymdist_column_names = ['IA', 'IB', 'IC', 'IAngleA', 'IAngleB', 'IAngleC']
    # griddyn_column_names = ['Bus11_VA', 'Bus11_VB', 'Bus11_VC',
    #                         'Bus11_VAngleA', 'Bus11_VAngleB', 'Bus11_VAngleC']
    # column_names = ['IA', 'IB', 'IC', 'IAngleA', 'IAngleB', 'IAngleC']
    # column_names.extend(griddyn_column_names)
    # df = pandas.DataFrame(index=np.arange(start_time, stop_time, step_size) * 10, columns=column_names)

    # Co-simulation loop
    for tim in np.arange(start_time, stop_time, step_size):

        # Get the outputs from griddyn
        griddyn_output_values = (griddyn.get_real(griddyn_output_valref))
        # set time in cymdist
        cymdist.time = tim
        # Set the inputs of cymdist
        cymdist.set_real(cymdist_input_valref, griddyn_output_values)
        
        #cymdist.do_step(current_t=tim, step_size=step_size, new_step=0)
        cymdist_output_values = (cymdist.get_real(cymdist_output_valref))

        # print(cymdist_output_values)
        # cymdist_output_values = [value * 10 if index < 3 else value for index, value in enumerate(cymdist_output_values)]
        # print(cymdist_output_values)

        griddyn.set_real(griddyn_input_valref, cymdist_output_values)
        griddyn.do_step(current_t=tim, step_size=step_size, new_step=0)

        CYMDIST_IA.append(cymdist.get_real(cymdist.get_variable_valueref('IA'))[0])
        CYMDIST_IB.append(cymdist.get_real(cymdist.get_variable_valueref('IB'))[0])
        CYMDIST_IC.append(cymdist.get_real(cymdist.get_variable_valueref('IC'))[0])
        GRIDDYN_VA.append(griddyn.get_real(griddyn.get_variable_valueref('Bus11_VA'))[0])
        GRIDDYN_VB.append(griddyn.get_real(griddyn.get_variable_valueref('Bus11_VB'))[0])
        GRIDDYN_VC.append(griddyn.get_real(griddyn.get_variable_valueref('Bus11_VC'))[0])
        simTim.append(tim / 60)

        # for name in cymdist_column_names:
        #     df.loc[simTim[-1], name] = cymdist.get_real(cymdist.get_variable_valueref(name))[0]
        #
        # for name in griddyn_column_names:
        #     df.loc[simTim[-1], name] = griddyn.get_real(griddyn.get_variable_valueref(name))[0]

        line1A.set_xdata(simTim)
        line1A.set_ydata(CYMDIST_IA)
        line1B.set_xdata(simTim)
        line1B.set_ydata(CYMDIST_IB)
        line1C.set_xdata(simTim)
        line1C.set_ydata(CYMDIST_IC)

        line2A.set_xdata(simTim)
        line2A.set_ydata(GRIDDYN_VA)
        line2B.set_xdata(simTim)
        line2B.set_ydata(GRIDDYN_VB)
        line2C.set_xdata(simTim)
        line2C.set_ydata(GRIDDYN_VC)

        ax1.relim()
        ax1.autoscale_view(True,True,True)
        ax2.relim()
        ax2.autoscale_view(True,True,True)
        fig.canvas.draw()
        plt.pause(0.01)

    pdb.set_trace()
    # df.to_csv('~/project_cyder/web/docker_django/worker/simulation/cosimulation_result.csv')
    # close figure automatically
    plt.close()

    # Terminate FMUs
    cymdist.terminate()
    griddyn.terminate()
    return {'result': 'some stuff'}


def simulate_2cymdist_gridyn_fmus(configuration_filename, configuration_filename2, start_time, end_time, step_size, _saveToFile=0, input_profiles=False, x_axis_labels=False):
    """Simulate one CYMDIST FMU.
    """
    # Parameters which will be arguments of the function
    start_time = start_time
    stop_time  = end_time
    step_size = step_size

    # Path to configuration file
    path_config1 = configuration_filename
    path_config2 = configuration_filename2
    cymdist_con_val_str1 = bytes(path_config1, 'utf-8')
    cymdist_con_val_str2 = bytes(path_config2, 'utf-8')

    griddyn_input_valref = []
    griddyn_output_valref = []

    cymdist_input_valref = []
    cymdist_output_valref = []
    cymdist_input_valref2 = []
    cymdist_output_valref2 = []

    cymdist1 = load_fmu("C:/cygwin64/home/Jonathan/project_cyder/web/docker_django/worker/simulation/fmu_code/CYMDIST.fmu", log_level=7)
    cymdist2 = load_fmu("C:/cygwin64/home/Jonathan/project_cyder/web/docker_django/worker/simulation/fmu_code/CYMDIST.fmu", log_level=7)
    griddyn=load_fmu("C:/cygwin64/home/Jonathan/project_cyder/web/docker_django/worker/simulation/fmu_code/14bus2input.fmu", log_level=7)

    cymdist1.setup_experiment(start_time=start_time, stop_time=stop_time)
    cymdist2.setup_experiment(start_time=start_time, stop_time=stop_time)
    griddyn.setup_experiment(start_time=start_time, stop_time=stop_time)

    # Define the inputs
    cymdist_input_names = ['VMAG_A', 'VMAG_B', 'VMAG_C', 'VANG_A', 'VANG_B', 'VANG_C']
    #cymdist_input_values = [2520, 2520, 2520, 0, -120, 120]
    cymdist_output_names = ['IA', 'IB', 'IC', 'IAngleA', 'IAngleB', 'IAngleC']

    griddyn_input_names = ['Bus10_IA', 'Bus10_IB', 'Bus10_IC',
                           'Bus10_IAngleA', 'Bus10_IAngleB', 'Bus10_IAngleC',
                           'Bus11_IA', 'Bus11_IB', 'Bus11_IC',
                           'Bus11_IAngleA', 'Bus11_IAngleB', 'Bus11_IAngleC']
    #griddyn_input_values = [277.6, 200.1, 173.1, -13.7, -130.51, 111.93]
    griddyn_output_names = ['Bus10_VA', 'Bus10_VB', 'Bus10_VC',
                            'Bus10_VAngleA', 'Bus10_VAngleB', 'Bus10_VAngleC',
                            'Bus11_VA', 'Bus11_VB', 'Bus11_VC',
                            'Bus11_VAngleA', 'Bus11_VAngleB', 'Bus11_VAngleC']

    # Get the value references of griddyn inputs
    for elem in griddyn_input_names:
        griddyn_input_valref.append(griddyn.get_variable_valueref(elem))

    # Get the value references of griddyn outputs
    for elem in griddyn_output_names:
        griddyn_output_valref.append(griddyn.get_variable_valueref(elem))

    # Get the value references of cymdist inputs
    for elem in cymdist_input_names:
        cymdist_input_valref.append(cymdist1.get_variable_valueref(elem))

    # Get the value references of cymdist outputs
    for elem in cymdist_output_names:
        cymdist_output_valref.append(cymdist1.get_variable_valueref(elem))

    # Get the value references of cymdist inputs
    for elem in cymdist_input_names:
        cymdist_input_valref2.append(cymdist2.get_variable_valueref(elem))

    # Get the value references of cymdist outputs
    for elem in cymdist_output_names:
        cymdist_output_valref2.append(cymdist2.get_variable_valueref(elem))

    # Set the flag to save the results
    cymdist1.set("_saveToFile", _saveToFile)
    # cymdist1.set("_communicationStepSize", step_size)
    cymdist2.set("_saveToFile", _saveToFile)
    # cymdist2.set("_communicationStepSize", step_size)
    # Get the initial outputs from griddyn
    # griddyn_output_values = (griddyn.get_real(griddyn_output_valref))
    # Set the initial outputs of GridDyn in cymdist
    # cymdist.set_real (cymdist_input_valref, griddyn_output_values)
    # Get value reference of the configuration file
    cymdist_con_val_ref1 = cymdist1.get_variable_valueref("_configurationFileName")
    cymdist_con_val_ref2 = cymdist2.get_variable_valueref("_configurationFileName")

    # Set the configuration file
    cymdist1.set_string([cymdist_con_val_ref1], [cymdist_con_val_str1])
    cymdist2.set_string([cymdist_con_val_ref2], [cymdist_con_val_str2])

    # # Verify that the multiplier is set
    # print ("This is the multiplier before it is set " + str(griddyn.get('multiplier')))
    #
    # # Set the value of the multiplier
    # griddyn.set('multiplier', 3.0)
    #
    # # Verify that the multiplier is set
    # print ("This is the multiplier after it is set " + str(griddyn.get('multiplier')))

    # Initialize the FMUs
    cymdist1.initialize()
    cymdist2.initialize()
    
    # Call event update prior to entering continuous mode.
    cymdist1.event_update()
    cymdist1.enter_continuous_time_mode()
    
    cymdist2.event_update()
    cymdist2.enter_continuous_time_mode()
    
    griddyn.initialize()

    # Create vector to store time
    simTim=[]
    CYMDIST_IA1 = []
    CYMDIST_IB1 = []
    CYMDIST_IC1 = []
    CYMDIST_IA2 = []
    CYMDIST_IB2 = []
    CYMDIST_IC2 = []

    # Interactive mode on
    plt.ion()

    # Create the plot
    fig = plt.figure()
    ax = fig.add_subplot(311)
    ax1 = fig.add_subplot(312)
    ax2 = fig.add_subplot(313)
    ax.set_ylabel('Inputs')
    ax1.set_ylabel('Feeder currents\n(cymDist 1) [A]')
    ax2.set_ylabel('Feeder currents\n(cymDist 2) [V]')
    ax2.yaxis.set_major_formatter(FormatStrFormatter('%.3f'))
    ax2.set_xlabel('Time (minutes)')
    if input_profiles:
        for input_profile in input_profiles:
            line, = ax.plot(input_profile['x'], input_profile['y'], label=input_profile['label'])
    line1A, = ax1.plot(simTim, CYMDIST_IA1, label='Phase A')
    line1B, = ax1.plot(simTim, CYMDIST_IB1, label='Phase B')
    line1C, = ax1.plot(simTim, CYMDIST_IC1, label='Phase C')
    line2A, = ax2.plot(simTim, CYMDIST_IA2, label='Phase A')
    line2B, = ax2.plot(simTim, CYMDIST_IB2, label='Phase B')
    line2C, = ax2.plot(simTim, CYMDIST_IC2, label='Phase C')
    ax.legend(loc=0)
    ax1.legend(loc=1)
    ax2.legend(loc=1)
    fig.tight_layout()

    # # Save all the result to a pandas dataframe
    # cymdist_column_names = ['IA', 'IB', 'IC', 'IAngleA', 'IAngleB', 'IAngleC']
    # griddyn_column_names = ['Bus11_VA', 'Bus11_VB', 'Bus11_VC',
    #                         'Bus11_VAngleA', 'Bus11_VAngleB', 'Bus11_VAngleC']
    # column_names = ['IA', 'IB', 'IC', 'IAngleA', 'IAngleB', 'IAngleC']
    # column_names.extend(griddyn_column_names)
    # df = pandas.DataFrame(index=np.arange(start_time, stop_time, step_size) * 10, columns=column_names)

    # Co-simulation loop
    for tim in np.arange(start_time, stop_time, step_size):

        # # Get the outputs from griddyn
        # griddyn_output_values = (griddyn.get_real(griddyn_output_valref))
        griddyn_output_values1 = [2520, 2520, 2520, 0, -120, 120]
        griddyn_output_values2 = [7270, 7270, 7270, 0, -120, 120]
        
        # set time in cymdist
        cymdist1.time = tim
        # set time in cymdist
        cymdist2.time = tim
        
        cymdist1.set_real(cymdist_input_valref, griddyn_output_values1)
        cymdist2.set_real(cymdist_input_valref, griddyn_output_values2)
        # cymdist1.do_step(current_t=tim, step_size=step_size, new_step=0)
        # cymdist2.do_step(current_t=tim, step_size=step_size, new_step=0)

        # cymdist_output_values = (cymdist.get_real(cymdist_output_valref))
        # griddyn.set_real(griddyn_input_valref, cymdist_output_values)
        # griddyn.do_step(current_t=tim, step_size=step_size, new_step=0)

        CYMDIST_IA1.append(cymdist1.get_real(cymdist1.get_variable_valueref('IA'))[0])
        CYMDIST_IB1.append(cymdist1.get_real(cymdist1.get_variable_valueref('IB'))[0])
        CYMDIST_IC1.append(cymdist1.get_real(cymdist1.get_variable_valueref('IC'))[0])
        CYMDIST_IA2.append(cymdist2.get_real(cymdist2.get_variable_valueref('IA'))[0])
        CYMDIST_IB2.append(cymdist2.get_real(cymdist2.get_variable_valueref('IB'))[0])
        CYMDIST_IC2.append(cymdist2.get_real(cymdist2.get_variable_valueref('IC'))[0])
        simTim.append(tim / 60)

        # for name in cymdist_column_names:
        #     df.loc[simTim[-1], name] = cymdist.get_real(cymdist.get_variable_valueref(name))[0]
        #
        # for name in griddyn_column_names:
        #     df.loc[simTim[-1], name] = griddyn.get_real(griddyn.get_variable_valueref(name))[0]

        line1A.set_xdata(simTim)
        line1A.set_ydata(CYMDIST_IA1)
        line1B.set_xdata(simTim)
        line1B.set_ydata(CYMDIST_IB1)
        line1C.set_xdata(simTim)
        line1C.set_ydata(CYMDIST_IC1)

        line2A.set_xdata(simTim)
        line2A.set_ydata(CYMDIST_IA2)
        line2B.set_xdata(simTim)
        line2B.set_ydata(CYMDIST_IB2)
        line2C.set_xdata(simTim)
        line2C.set_ydata(CYMDIST_IC2)

        ax1.relim()
        ax1.autoscale_view(True,True,True)
        ax2.relim()
        ax2.autoscale_view(True,True,True)
        fig.canvas.draw()
        plt.pause(0.01)

    pdb.set_trace()
    # df.to_csv('~/project_cyder/web/docker_django/worker/simulation/cosimulation_result.csv')
    # close figure automatically
    plt.close()

    # Terminate FMUs
    cymdist1.terminate()
    cymdist2.terminate()
    griddyn.terminate()
    return {'result': 'some stuff'}
