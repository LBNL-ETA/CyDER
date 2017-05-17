from __future__ import division
import source.cymdist_tool.tool as cymdist
import datetime
import progressbar
import pandas
import time as s
try:
    import cympy
except:
    pass


class PVForecast(object):
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
        """Forecast PV demand and return configuration file for CyDER"""
        # Save normalized generation with the right format
        pv_forecast = self._load_forecast()

        # Update the configuration file
        self._update_configuration(pv_forecast)
        return self.configuration

    def _update_configuration(self, pv_forecast):
        """Update all pvs within feeder with the pv_forecast timeserie"""
        # Open model and get the devices from the first model
        cympy.study.Open(self.feeder.feeder_folder + self.feeder.feeder_name)
        pvs = cymdist.list_pvs()

        # GET FIRST TIME PV FORECAST <----
        start = pv_forecast.index[0]

        for index, time in enumerate(self.configuration['times']):
            dt = start + datetime.timedelta(seconds=time)
            for pv in pvs.itertuples():
                self.configuration['models'][index]['set_pvs'].append(
                    {'device_number': pv.device_number,
                     'generation': pv.generation * pv_forecast.loc[dt, 'profile'],
                     'description': 'pv forecast'})

    def _load_forecast(self):
        """Load forecast from static file directly"""
        # Load prediction from file
        progress = progressbar.ProgressBar(widgets=['progress: ',
                                                    progressbar.Percentage(),
                                                    progressbar.Bar()],
                                           maxval=20).start()
        # Replace below with actual call to Rafael's module
        # For now place holder (sleep function)
        for it in range(0, 20):
            s.sleep(0.2)
            progress.update(it)
        progress.finish()
        return pandas.read_csv(
            'static/pv/profile.csv', index_col=0, parse_dates=[0])
