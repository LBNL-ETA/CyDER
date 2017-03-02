from __future__ import division
from pyfmi import load_fmu
from pyfmi.master import Master
from datetime import datetime
import pdb
import json
from ... import cymdist
try:
    import cympy
except:
    # Only installed on the Cymdist server
    pass


# def set_pv(data):
#     """
#     Input: [{'device_name': ..., 'generation': ...}]
#     Return {'set_pvs': [{'device_name': , 'generation': }]}
#     """
#     # Create dictionnary
#     return_dict = {'set_pvs': []}
#     for value in data:
#         return_dict['set_pvs'].append({'device_name': value['device_name'],
#                                        'generation': value['generation']})
#     return return_dict
#
#
# def set_load(data):
#     """
#     Input: [{'device_name': ..., 'active_power': ...}]
#     Return {'set_loads': [{'device_name': , 'active_power': }]}
#     """
#     # Create dictionnary
#     return_dict = {'set_loads': []}
#     for value in data:
#         return_dict['set_loads'].append({'device_name': value['device_name'],
#                                          'active_power': value['active_power']})
#     return return_dict
#
#
# def add_pv(data):
#     """
#     Input: [{'section_id': , 'generation': }, ...]
#     Return: {'new_pvs': [{'section_id': , 'generation': }, ...]}
#     """
#     return_dict = {'new_pvs': []}
#     for value in data:
#         return_dict['new_pvs'].append({'section_id': value['section_id'],
#                                        'generation': value['generation']})
#     return return_dict
#
#
# def add_load(data):
#     """
#     Input: [{'section_id': , 'active_power': }, ...]
#     Return: {'new_loads': [{'section_id': , 'active_power': }, ...]}
#     """
#     return_dict = {'new_loads': []}
#     for value in data:
#         return_dict['new_loads'].append({'section_id': value['section_id'],
#                                          'active_power': value['active_power']})
#     return return_dict


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
    # # Create config file
    # configuration_file = {'times': times,
    #                       'interpolation_method': 'closest_time',
    #                       'models': []
    #                      }
    #
    # for time, model_name in zip(times, model_names):
    #     model = {
    #        'filename': 'D://Users//Jonathan//Documents//GitHub//PGE_Models_DO_NOT_SHARE//' + model_name,
    #        'new_loads': [],
    #        'set_loads': [],
    #        'new_pvs': [],
    #        'set_pvs': [],
    #        }
    #     for configuration in configurations[time]:
    #         temp = configuration['function'](configuration['input'])
    #         model[temp['type']].extend(temp['data'])
    #     configuration_file['models'].append(model)

    # Generate random filename
    filename = ''

    with open(filename, 'w') as outfile:
        json.dump(configuration_file, outfile)

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

configuration_filename = "D://Users//Jonathan//Documents//GitHub//PGE_Models_DO_NOT_SHARE//config.json"
start_time = 0.0
end_time = 0.1
result = simulate_cymdist_gridyn_fmus(configuration_filename, start_time, end_time)
print(result)
pdb.set_trace()
