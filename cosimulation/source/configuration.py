from __future__ import division
import cympy
import cymdist_tool.tool as cymdist
import json
import random
import string


def initialize_configuration(times, parent_folder, model_names):
    """Initialize configuration file"""
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
