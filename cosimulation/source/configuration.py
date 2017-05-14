from __future__ import division
import json
import random
import datetime
import string
import source.ev_forecast.tool as ev
import source.pv_forecast.tool as pv
import source.load_forecast.tool as l
import matplotlib.pyplot as plt
import seaborn
import os
seaborn.set_style("whitegrid")
seaborn.despine()

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
        self.save = True
        self.to_save = None

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
        self.start = self.cyder_input_row.start

        # Do you want to save things to the file system?
        if self.save:
            self.save = self.directory + self.pk + '/'
            os.makedirs(self.save)
        else:
            self.save = 'False'

        # Upper structure of the configuration file
        configuration = {'times': self.times,
                         'interpolation_method': 'closest_time',
                         'models': []
                         }

        # Configuration file inside of models
        for time in self.times:
            model = {
               'filename': self.feeder_folder + self.feeder_name,
               'save': self.save + str(time) + '.csv',
               'to_save': [],
               'new_loads': [],
               'set_loads': [],
               'new_pvs': [],
               'set_pvs': [],
               }
            configuration['models'].append(model)

        # Initialize step of the calibration process
        if self.cyder_input_row.ev_forecast:
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

        # Launch pv forecast --> Update SET PV
        if self.pv_forecast is True:
            pv_gen = pv.PVForecast()
            pv_gen.initialize(self)
            self.configuration = pv_gen.forecast()

        # Launch load forecast --> Update SET LOAD
        if self.load_forecast is True:
            load_demand = l.LoadForecast()
            load_demand.initialize(self)
            self.configuration = load_demand.forecast()

        # Launch ev forecast --> Update SET LOAD
        if self.ev_forecast is True:
            ev_demand = ev.EVForecast()
            ev_demand.initialize(self)
            self.configuration = ev_demand.forecast()

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

    def visualize(self):
        """Create a plot with the loads and generation from the configuration"""
        # Create y and x vectors
        pv = [0] * len(self.configuration['times'])
        load = [0] * len(self.configuration['times'])
        dates = [datetime.datetime(2017, 6, 17, 6, 0, 0) +
                 datetime.timedelta(seconds=value)
                 for value in self.configuration['times']]

        # Get the y values (generation and load versus time)
        for index, model in enumerate(self.configuration['models']):
            for set_load in model['set_loads']:
                for phase in set_load['active_power']:
                    load[index] += phase['active_power']

            for set_pv in model['set_pvs']:
                pv[index] += set_pv['generation']

        # Plot results
        plt.figure(figsize=(10, 5), dpi=110)
        plt.plot(dates, load, label='Load demand')
        plt.plot(dates, pv, label='PV demand')
        plt.ylabel('Power output in [kW]')
        plt.xlabel('Time')
        plt.legend(loc=0)
        plt.show()
