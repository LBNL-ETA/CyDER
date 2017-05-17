from __future__ import division
import json
import random
import datetime
import string
import source.ev_forecast.tool as ev
import source.pv_forecast.tool as pv
import source.load_forecast.tool as l
import source.monitor as m
import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter
import os


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
        self.save_results = True
        self.result_to_save = None

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
        if self.save_results:
            self.save_results = self.directory + str(self.pk) + '/'
            os.makedirs(self.save_results)
        else:
            self.save_results = 'False'

        # Upper structure of the configuration file
        configuration = {'times': self.times,
                         'interpolation_method': 'closest_time',
                         'models': []
                         }

        # Configuration file inside of models
        for time in self.times:
            model = {
               'filename': self.feeder_folder + self.feeder_name,
               'save': self.save_results + str(time) + '.json',
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
            print('')
            print('Forecasting PV generation...')
            pv_gen = pv.PVForecast()
            pv_gen.initialize(self)
            self.configuration = pv_gen.forecast()

        # Launch load forecast --> Update SET LOAD
        if self.load_forecast is True:
            print('')
            print('Forecasting load demand...')
            load_demand = l.LoadForecast()
            load_demand.initialize(self)
            self.configuration = load_demand.forecast()

        # Launch ev forecast --> Update SET LOAD
        if self.ev_forecast is True:
            print('')
            print('Forecasting EV demand...')
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
        # Get data
        x, data = m.format_configuration_to_plot(self.start, self.configuration)

        # Plot results
        fig = plt.figure(figsize=(10, 5), dpi=110)
        ax1 = fig.add_subplot(111)
        for value in data:
            ax1.plot(x, value['y'], label=value['label'])
        formatter = DateFormatter('%H:%M')
        ax1.xaxis.set_major_formatter(formatter)
        ax1.set_ylabel('Power output in [kW]')
        ax1.set_xlabel('Time')
        ax1.legend(loc=0)
        plt.show()
