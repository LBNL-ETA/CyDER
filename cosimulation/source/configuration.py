from __future__ import division
import json
import random
import string
import source.ev_forecast.tool as ev


class FeederConfiguration(object):
    """Feeder configurations"""

    def __init__(self):
        # Basic parameters
        self.feeder_name = None
        self.pk = None
        self.start = None
        self.end = None
        self.timestep = None
        self.times = None
        self.feeder_folder = 'D://Users//Jonathan//Documents//GitHub//PGE_Models_DO_NOT_SHARE//'
        self.token = None
        self.directory = None
        self.cyder_input_row = None

        # Configuration processes
        self.ev_forecast = False
        self.pv_forecast = False
        self.load_forecast = False
        self.set_load = False
        self.set_pv = False
        self.add_load = False
        self.add_pv = False

        # Configuration
        self.configuration = None

    def _initialize(self):
        """Initialize configuration file"""
        self.feeder_name = self.cyder_input_row.feeder_name
        self.timestep = self.cyder_input_row.timestep
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

        # Initialize step of the calibration process
        if self.cyder_input_row.ev_forecast is not False:
            self.ev_forecast = True
        if self.cyder_input_row.pv_forecast is not False:
            self.pv_forecast = True
        if self.cyder_input_row.add_load is not False:
            self.add_load = True
            self.set_load = True
        if self.cyder_input_row.add_pv is not False:
            self.add_pv = True
            self.set_pv = True
        if self.cyder_input_row.load_forecast is not False:
            self.load_forecast = True
        return configuration

    def configure(self):
        """Launch configuration procedures"""
        # Create empty template
        self.configuration = self._initialize()

        # --> ADD LOAD

        # --> ADD PV

        # --> SET LOAD

        # --> SET PV

        # Launch ev forecast --> SET LOAD
        if self.ev_forecast is True:
            ev_demand = ev.EVForecast()
            ev_demand.initialize(self)
            self.configuration = ev_demand.forecast()

        # Launch pv forecast --> Update SET and ADD PV

        # Launch load forecast --> Update SET and ADD Load

    def save(self):
        """
        Input:
        configuration = {
                         'times': [0],
                         'interpolation_method': 'closest_time',
                         'models': [{
                            'filename': 'D://...//BU0001.sxst',
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
        filename = self.directory + self.feeder_name + '_#' + str(self.pk) + '_config.json'
        with open(filename, 'w') as outfile:
            json.dump(self.configuration, outfile)
        return filename
