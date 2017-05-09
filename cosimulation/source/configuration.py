from __future__ import division
import cympy
import cymdist_tool.tool as cymdist
import json
import random
import string


class FeederConfiguration(object):
    """Feeder configurations"""

    def __init__(self, times, feeder_name):
        # Basic parameters
        self.feeder_name = None
        self.pk = 0
        self.start = None
        self.end = None
        self.timestep = None
        self.times = None
        self.feeder_folder = '~/Jonathan/GitHub/PGE/'
        self.directory = None

        # Configuration processes
        self.ev_forecast = False
        self.pv_forecast = False
        self.set_load = False
        # self.set_pv = False
        # self.add_load = False
        self.add_pv = False

        # Create empty template
        self.configuration = self._initialize()

    def _initialize(self):
        """Initialize configuration file"""
        configuration = {'times': self.times,
                         'interpolation_method': 'closest_time',
                         'models': []
                         }

        for time in self.times:
            model = {
               'filename': self.feeder_folder + self.feeder_name,
               'new_loads': [],
               'set_loads': [],
               'new_pvs': [],
               'set_pvs': [],
               }
            configuration['models'].append(model)
        return configuration

    def save(self):
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
        # Save
        filename = self.directory + '_' + self.feeder_name + '_#' + str(self.pk) + '_congig.json'
        with open(filename, 'w') as outfile:
            json.dump(configuration, outfile)
        return filename
