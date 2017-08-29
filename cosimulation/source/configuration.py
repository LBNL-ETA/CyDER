from __future__ import division
import json
import random
import datetime
import pandas
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
        self.do_ev_forecast = False
        self.do_pv_forecast = False
        self.do_load_forecast = False
        self.do_set_load = False
        self.do_set_pv = False
        self.do_add_load = False
        self.do_add_pv = False

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
            self.do_ev_forecast = True
        if self.cyder_input_row.pv_forecast is not False:
            self.do_pv_forecast = True
        if self.cyder_input_row.add_load:
            self.do_add_load = True
            self.do_set_load = True
        if self.cyder_input_row.add_pv:
            self.do_add_pv = True
            self.do_set_pv = True
        if self.cyder_input_row.load_forecast is not False:
            self.do_load_forecast = True
        return configuration

    def configure(self):
        """Launch configuration procedures"""
        # Create empty template
        self.configuration = self._initialize()

        # Launch pv forecast --> Update SET PV
        if self.do_pv_forecast is True:
            print('')
            print('Forecasting PV generation...')
            pv_gen = pv.PVForecast()
            pv_gen.initialize(self)
            pv_profile, self.configuration = pv_gen.forecast()

        # Launch load forecast --> Update SET LOAD
        if self.do_load_forecast is True:
            print('')
            print('Forecasting load demand...')
            load_demand = l.LoadForecast()
            load_demand.initialize(self)
            load_profile, self.configuration = load_demand.forecast()

        # Launch ev forecast --> Update SET LOAD
        if self.do_ev_forecast is True:
            print('')
            print('Forecasting EV demand...')
            ev_demand = ev.EVForecast()
            ev_demand.initialize(self)
            self.configuration = ev_demand.forecast()

        # Update configuration with additional loads--> SET LOAD
        if self.do_set_load:
            self.set_load(load_profile)

        # Update configuration with additional pvs --> SET PV
        if self.do_set_pv:
            self.set_pv(pv_profile)

    def set_load(self, load_profile):
        """Set load in the configuration file using existing set points"""
        # Read input file
        set_load_input = pandas.read_excel(self.cyder_input_row.add_load)

        # GET FIRST TIME load FORECAST <----
        start = datetime.datetime(2014, 2, 1, 6, 0, 0)

        # For times in the simulation
        for index, time in enumerate(self.configuration['times']):

            # Current time in date format
            dt = start + datetime.timedelta(seconds=time)

            # For rows in input file
            for row in set_load_input.itertuples():
                found_device_in_configuration = False

                # Look in the configuration file for existing set point
                for index2, device in enumerate(self.configuration['models'][index]['set_loads']):
                    if device['device_number'] == str(row.device_number):

                        # Count phases index
                        phase_count = len(self.configuration['models'][index]['set_loads'][index2]['active_power'])

                        # Add the additional power demand at the device
                        for index3, phase in enumerate(self.configuration['models'][index]['set_loads'][index2]['active_power']):
                            # additional
                            temp = row.added_power_kw * load_profile.loc[dt, 'profile'] / phase_count
                            self.configuration['models'][index]['set_loads'][index2]['active_power'][index3]['active_power'] += temp

                        # Go to the next device in the input file
                        found_device_in_configuration = True
                        break

                # If device not found we could add an entry
                if not found_device_in_configuration:
                    raise Exception('Setting load with an unauthorized device number')

    def set_pv(self, pv_profile):
        """Set load in the configuration file using existing set points"""
        # Read input file
        set_pv_input = pandas.read_excel(self.cyder_input_row.add_pv)

        # GET FIRST TIME load FORECAST <----
        start = pv_profile.index[0]

        # For times in the simulation
        for index, time in enumerate(self.configuration['times']):

            # Current time in date format
            dt = start + datetime.timedelta(seconds=time)

            # For rows in input file
            for row in set_pv_input.itertuples():
                found_device_in_configuration = False

                # Look in the configuration file for existing set point
                for index2, device in enumerate(self.configuration['models'][index]['set_pvs']):
                    if device['device_number'] == str(row.device_number):

                        # Additional generation
                        temp = row.added_power_kw * pv_profile.loc[dt, 'profile']
                        self.configuration['models'][index]['set_pvs'][index2]['generation'] += temp

                        # Go to the next device in the input file
                        found_device_in_configuration = True
                        break

                # If device not found we could add an entry
                if not found_device_in_configuration:
                    raise Exception('Setting load with an unauthorized device number')

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
