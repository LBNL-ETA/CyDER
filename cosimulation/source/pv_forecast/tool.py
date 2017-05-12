from __future__ import division

class PVForecast(object):
    """Forecast EV demand at a feeder"""
    def __init__(self):
        self.configuration = None

    def initialize(self, feeder):
        """Initialize feeder inputs"""
        pass

    def forecast(self):
        """Forecast EV demand and return configuration file for CyDER"""
        # Save normalized generation with the right format
        formatted_generation = self._save_power_demand(power_demand)

        # Update the configuration file
        self._update_configuration(formatted_generation)

        # Read power demand and plot
        (formatted_generation).plot()
        plt.ylabel('Normalized generation')
        plt.xlabel('Time')
        plt.show()
        return self.configuration
