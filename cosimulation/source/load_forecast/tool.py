from __future__ import division
import source.cymdist_tool.tool as cymdist
import datetime
import pandas
try:
    import cympy
except:
    pass


class LoadForecast(object):
    """Forecast EV demand at a feeder"""
    def __init__(self):
        self.configuration = None
        self.feeder = None
        self.configuration = None

    def initialize(self, feeder):
        """Initialize feeder inputs"""
        self.feeder = feeder
        self.configuration = feeder.configuration

    def forecast(self):
        """Forecast load demand and return configuration file for CyDER"""
        # Save normalized generation with the right format
        load_forecast = self._load_forecast()

        # Update the configuration file
        self._update_configuration(load_forecast)
        return load_forecast, self.configuration

    def _update_configuration(self, load_forecast):
        """Update all pvs within feeder with the pv_forecast timeserie"""
        # Open model and get the devices from the first model
        cympy.study.Open(self.feeder.feeder_folder + self.feeder.feeder_name)
        loads = cymdist.list_loads()

        # GET FIRST TIME PV FORECAST <----
        start = load_forecast.index[0]

        for index, time in enumerate(self.configuration['times']):
            dt = start + datetime.timedelta(seconds=time)
            for load in loads.iterrows():
                _, load = load
                self.configuration['models'][index]['set_loads'].append(
                    {'device_number': load['device_number'],
                     'active_power': [],
                     'description': 'load forecast'})
                for phase_index in ['0', '1', '2']:
                    if load['activepower_' + phase_index]:
                        self.configuration['models'][index]['set_loads'][-1]['active_power'].append(
                            {'active_power': (float(load['activepower_' + phase_index])
                                * load_forecast.loc[dt, 'profile']),
                             'phase_index': phase_index,
                             'phase': str(load['phase_' + phase_index])})

    def _load_forecast(self):
        """Load forecast from static file directly"""
        # Load prediction from file
        return pandas.read_csv(
            'static/load/profile.csv', index_col=0, parse_dates=[0])
