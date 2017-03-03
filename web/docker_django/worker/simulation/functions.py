from __future__ import division
from pyfmi import load_fmu
from pyfmi.master import Master
from datetime import datetime
import string
import random
import pdb
import json
import cymdist
try:
    import cympy
except:
    # Only installed on the Cymdist server
    pass

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
    """Simulate one CYMDIST FMU coupled to a dummy GridDyn FMU.
    """
    # Wire the Master
    cymdist = load_fmu("D:/Users/Jonathan/Documents/GitHub/cyder_tsn/NO_SHARING/CYMDIST/CYMDIST.fmu", log_level=7)
    gridyn = load_fmu("D:/Users/Jonathan/Documents/GitHub/cyder_tsn/NO_SHARING/GridDyn/GridDyn.fmu", log_level=7)
    models = [cymdist, gridyn]
    connections = [(gridyn, "VMAG_A", cymdist, "VMAG_A"),
                   (gridyn, "VMAG_B", cymdist, "VMAG_B"),
                   (gridyn, "VMAG_C", cymdist, "VMAG_C"),
                   (gridyn, "VANG_A", cymdist, "VANG_A"),
                   (gridyn, "VANG_B", cymdist, "VANG_B"),
                   (gridyn, "VANG_C", cymdist, "VANG_C"),
                   (cymdist, "IA", gridyn, "IA"),
                   (cymdist, "IB", gridyn, "IB"),
                   (cymdist, "IC", gridyn, "IC"),
                   (cymdist, "IAngleA", gridyn, "IAngleA"),
                   (cymdist, "IAngleB", gridyn, "IAngleB"),
                   (cymdist, "IAngleC", gridyn, "IAngleC"),]
    coupled_simulation = Master(models, connections)
    opts = coupled_simulation.simulate_options()
    opts['step_size'] = 0.1

    # Set the configuration file
    cymdist.set("save_to_file", save_to_file)
    con_val_str = bytes(configuration_filename, 'utf-8')
    con_val_ref = cymdist.get_variable_valueref("conFilNam")
    cymdist.set_string([con_val_ref], [con_val_str])

    # Launch simulation
    start = datetime.now()
    res = coupled_simulation.simulate(options=opts,
                                      start_time=start_time,
                                      final_time=end_time)
    end = datetime.now()
    print('Ran a coupled CYMDIST/GridDyn simulation in ' +
          str((end - start).total_seconds()) + ' seconds.')

    # Create a normal result object (need to use Assimulo object?)
    result = {'cymdist': {}, 'griddyn': {}}
    for model_key, model in zip(['cymdist', 'griddyn'], [cymdist, gridyn]):
        for key in ['IA', 'IAngleA', 'IB', 'IAngleB', 'IC', 'IAngleC',
                    'VMAG_A', 'VMAG_B', 'VMAG_C', 'VANG_A', 'VANG_B', 'VANG_C']:
            result[model_key][key] = res[model][key]
    return result

# configuration_filename = "D://Users//Jonathan//Documents//GitHub//PGE_Models_DO_NOT_SHARE//config.json"
# start_time = 0.0
# end_time = 0.1
# result = simulate_cymdist_gridyn_fmus(configuration_filename, start_time, end_time)
# print(result)
# pdb.set_trace()
